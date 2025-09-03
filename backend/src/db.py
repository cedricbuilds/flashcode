import logging

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_DATABASE"),
    "port": os.getenv("DB_PORT")
}
logging.warning(config)

def test_db():
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        logging.warning("Connected to MySQL!")

        cursor.execute("SELECT * FROM flashcode.card;")
        card = cursor.fetchall()
        for c in card:
            print(c)

    except mysql.connector.Error as err:
        logging.warning(f"Error: {err}")

    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

    logging.warning("Connection closed.")

def add_card(front_text=None, front_code=None, front_images=None, back_text=None, back_code=None, back_images=None):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        query = "Insert Into card (front_text, front_code, front_images, back_text, back_code, back_images) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (front_text, front_code, front_images, back_text, back_code, back_images)
        cursor.execute(query, values)
        conn.commit()

    except mysql.connector.Error as err:
        logging.warning(f"Error: {err}")

    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

def get_cards():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM card;")
        card = cursor.fetchall()
        if len(card) < 1:
            return ""
        else:
            return card

    except mysql.connector.Error as err:
        logging.warning(f"Error: {err}")

    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

def delete_card(card_id: str):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM card WHERE id = %s;", (card_id,))
        conn.commit()
        logging.info("Deleted card with id %s", card_id)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

def cli():
    while True:
        cmd = input("Command (add/get/delete/exit): ").strip().lower()
        if cmd == "add":
            front = input("Front text: ")
            back = input("Back text: ")
            add_card(front_text=front, back_text=back)
        elif cmd == "get":
            cards = get_cards()
            for c in cards:
                logging.info(c)
        elif cmd == "delete":
            cid = input("Card ID: ")
            delete_card(cid)
        elif cmd == "exit":
            break
        else:
            logging.info("Unknown command")




if __name__ == "__main__":
    cli()

#get_cards()
#delete_card(card_id="1")
#add_card()
#test_db()

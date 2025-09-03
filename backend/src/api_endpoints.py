from flask import Flask, request, jsonify
from db import add_card, get_cards, delete_card  # import your methods

app = Flask(__name__)

@app.route("/cards", methods=["GET"])
def api_get_cards():
    cards = get_cards()
    return jsonify(cards)

@app.route("/cards", methods=["POST"])
def api_add_card():
    data = request.json
    card_id = add_card(
        front_text=data.get("front_text"),
        back_text=data.get("back_text")
    )
    return jsonify({"id": card_id}), 201

@app.route("/cards/<int:card_id>", methods=["DELETE"])
def api_delete_card(card_id):
    delete_card(card_id)
    return jsonify({"status": "deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
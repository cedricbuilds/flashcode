import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
    const [cards, setCards] = useState([]);
    const [front, setFront] = useState("");
    const [back, setBack] = useState("");

    useEffect(() => {
        fetchCards();
    }, []);

    const fetchCards = async () => {
        const res = await axios.get("http://127.0.0.1:5000/cards");
        setCards(res.data);
    };

    const addCard = async () => {
        await axios.post("http://127.0.0.1:5000/cards", { front_text: front, back_text: back });
        setFront("");
        setBack("");
        fetchCards();
    };

    const deleteCard = async (id) => {
        await axios.delete(`http://127.0:5000/cards/${id}`);
        fetchCards();
    };

    return (
        <div>
            <h1>Flashcards</h1>
            <input value={front} onChange={e => setFront(e.target.value)} placeholder="Front" />
            <input value={back} onChange={e => setBack(e.target.value)} placeholder="Back" />
            <button onClick={addCard}>Add Card</button>
            <ul>
                {cards.map(card => (
                    <li key={card.id}>
                        <strong>{card.front_text}</strong> / {card.back_text}
                        <button onClick={() => deleteCard(card.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
import React, { useEffect, useState } from "react";
import styles from './Account.module.css';
import { Navbar } from './Navbar'
import axios from "axios";

export const Account = () => {
    const [cards, setCards] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchCards = async () => {
            try {
                const response = await axios.get('/verifyCard');
                if (response.data && Array.isArray(response.data)) {
                    setCards(response.data);
                    setError('');
                } else {
                    setError('Invalid response format. Please try again later.');
                }
            } catch (error) {
                console.error("Error fetching cards", error);
                setError("Error fetching cards. Please try again later.");
            }
        };
        fetchCards();
    }, []);

    const handleVerifyCards = async () => {
        const selectedCards = cards.filter(card => card.checked)
        if (selectedCards.length === 0) {
            window.alert('Please select a card to verify.');
            return;
        }

        const cardNum = String(selectedCards[0].cardNumber);
        console.log(cardNum);
        try {
            const response = await axios.post('/verifyCard',
                {
                    cardNumber: cardNum
                });
            console.log("Response data:", response.data);
            window.alert('Validation successful!');
            window.location.reload();
        } catch (error) {
            console.error("Error verifying card", error);
        }
    };

    const handleCheckboxChange = (index) => {
        setCards(prevCards => {
            const updatedCards = prevCards.map((card, i) => ({
                ...card,
                checked: i === index ? !card.checked : false
            }));
            return updatedCards;
        });
    };


    return (
        <div>
            <Navbar />
            <div className={styles.homeContainer}>
                <table className={styles.productTable}>
                    <thead>
                        <tr>
                            <th>Card number</th>
                            <th>Username</th>
                            <th>Expiration Date</th>
                            <th>Cvv</th>
                            <th>Amount</th>
                            <th>Bank account number</th>
                            <th>Verify</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cards.map((card, index) => (
                            <tr key={index}>
                                <td>{card.cardNumber}</td>
                                <td>{card.userName}</td>
                                <td>{card.expirationDate}</td>
                                <td>{card.cvv}</td>
                                <td>{card.amount}</td>
                                <td>{card.bankAccountNumber}</td>
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={card.checked || false}
                                        onChange={() => handleCheckboxChange(index)}
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className={styles.divHomeButtons}>
                    <button className={styles.homeButton} onClick={handleVerifyCards}>Submit</button>
                    {error && <p style={{ color: 'red', marginBottom: 20 }}>{error}</p>}
                </div>
            </div>
        </div>
    );
};
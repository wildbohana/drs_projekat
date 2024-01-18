import React, { useState } from "react";
import styles from './Card.module.css';
import { Navbar } from './Navbar'
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const AddBalance = () => {
    const [errorMessage, setErrorMessage] = useState('');
    const [currency, setCurrency] = useState('');
    const [amount, setAmount] = useState('');

    const navigate = useNavigate();

    const handleAddBalance = async () => {
        try {
            const token = localStorage.getItem('userToken');
            

            
            
            const response = await axios.post(`/accountBalance/${token}`, {
                amount,
                currency
            }
            );
            
            console.log(amount);
            console.log(currency);


            if (response.status === 200) {
                alert('Balance successfully added!');
            }
        } catch (error) {
            console.error('Error adding balance:', error);
            setErrorMessage('Error adding balance. Please try again.');
        }
    }

    const handleSubmitClick = () => {
        if (currency.trim() === '' || (isNaN(+amount) || +amount <= 0)) {
            setErrorMessage('Please fill input fields or correct the card number!');
        } else {
            handleAddBalance();
            setErrorMessage('');
            navigate('/home');
        }
    };

    return (
        <div>
            <Navbar />
            <div className={styles.container}>
                <div className={styles.form}>
                    <h1>Add Balance</h1>
                    <form>
                        <input type="number" className={styles['form-input']} placeholder='Enter the amount' value={amount} onChange={(e) => setAmount(e.target.value)} />
                        <br />
                        <input type="text" className={styles['form-input']} placeholder='Enter the currency' value={currency} onChange={(e) => setCurrency(e.target.value)} />
                        <br />                        
                        
                        <button className={styles.button} onClick={(e) => {
                            e.preventDefault();
                            handleSubmitClick();
                        }}>Submit</button>
                        {errorMessage && <p style={{ color: 'red', textAlign: 'center', marginBottom: 20 }} > {errorMessage}</p>}
                    </form>
                </div>
            </div>
        </div>
    );
};

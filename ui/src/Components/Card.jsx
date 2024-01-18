import React, { useState } from "react";
import styles from './Card.module.css';
import { Navbar } from './Navbar'
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const Card = () => {
    const [cardNumber, setCardNumber] = useState('');
    const [expirationDate, setExpirationDate] = useState('');
    const [cvv, setCvv] = useState('');
    const [amount, setAmount] = useState('');
    const [userName, setUserName] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const isFormSubmitted = localStorage.getItem("formSubmitted");


    
    


    const navigate = useNavigate();





    const handleValidationCard = async () => {
        try {
            const token = localStorage.getItem('userToken');
            const response = await axios.post(`/card/${token}`, {
                userName,
                cardNumber,
                expirationDate,
                cvv,
                amount,
            }
            );

            if (response.status === 200) {
                alert('Card successfully added!');
            }
        } catch (error) {
            console.error('Error adding card:', error);
            setErrorMessage('Error adding card. Please try again.');
        }
    }
    
    

    const handleSubmitClick = () => {
        if (userName.trim() === '' || cardNumber.trim() === '' || cardNumber.trim().startsWith('0') || expirationDate.trim() === '' || cvv.trim() === '' || (isNaN(+amount) || +amount <= 0)) {
            setErrorMessage('Please fill input fields or correct the card number!');
            
        } else {
            handleValidationCard();
        
            setErrorMessage('');
            navigate('/home');
        }
    };



    const [formSubmitted, setFormSubmitted] = useState(false);

    const handleFormSubmit = () => {
      // Check if the form has already been submitted
      //const isFormSubmitted = localStorage.getItem("formSubmitted");
  
      if (isFormSubmitted) {
        // Display a message indicating the form has already been filled out
        alert("An existing card is already in use");
      } else {
        // Process the form submission logic
        // ... (your form submission logic here)
  
        // Set the flag in local storage
        localStorage.setItem("formSubmitted", "true");
  
        // Update the state to reflect the form submission
        setFormSubmitted(true);
      }
    }

    if(isFormSubmitted){
        return (
            <div>
                <Navbar />
                <div className={styles.container}>
                    <div className={styles.form}>
                        <h1>Validation card</h1>
                        <form>
                        <h1>Credit Card is already filled out</h1>
                        </form>
                    </div>
                </div>
            </div>
        );
        
    }
    else
    return (
        <div>
            <Navbar />
            <div className={styles.container}>
                <div className={styles.form}>
                    <h1>Validation card</h1>
                    <form>
                        <input type="text" className={styles['form-input']} placeholder='Enter your username' value={userName} onChange={(e) => setUserName(e.target.value)} />
                        <br />
                        <input type="number" className={styles['form-input']} placeholder='Enter your card number' value={cardNumber} onChange={(e) => setCardNumber(e.target.value)} />
                        <br />
                        <input type="text" className={styles['form-input']} placeholder='Enter expiration date' value={expirationDate} onChange={(e) => setExpirationDate(e.target.value)} />
                        <br />
                        <input type="number" className={styles['form-input']} placeholder='Enter your cvv code' value={cvv} onChange={(e) => setCvv(e.target.value)} />
                        <br />
                        <input type="number" className={styles['form-input']} placeholder='Enter amount' value={amount} onChange={(e) => setAmount(e.target.value)} />
                        <br />
                        <button className={styles.button} onClick={(e) => {
                            
                            e.preventDefault();
                            handleSubmitClick();
                            handleFormSubmit();
                        }}>Submit</button>
                        {errorMessage && <p style={{ color: 'red', textAlign: 'center', marginBottom: 20 }} > {errorMessage}</p>}
                    </form>
                </div>
            </div>
        </div>
    );
};

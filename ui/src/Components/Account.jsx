import React, { useEffect, useState } from "react";
import styles from './Account.module.css';
import { Navbar } from './Navbar'
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const Account = () => {
    const [userName, setUserName] = useState('');
    const [cardNumber, setCardNumber] = useState('');
    const [expirationDate, setExpirationDate] = useState('');
    const [cvv, setCvv] = useState('');
    const [amount, setAmount] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [token,setToken] = useState(localStorage.getItem('userToken'));

    const navigate = useNavigate();

   /* const fetchUserProfile = async () => {
        try {
            const token = localStorage.getItem('userToken');
            const response = await axios.get(`/card/${token}`);
            const userProfile = response.data;

            setUserName(userName);
            setCardNumber(userProfile.creditCard.cardNumber);
            setExpirationDate(userProfile.creditCard.expirationDate);
            setCvv(userProfile.creditCard.cvv);
            setCardAmount(userProfile.creditCard.amount);
        } catch (error) {
            console.error('Error fetching user profile:', error);
        }
    };
*/



    


    const handleEditClick = async () => {
        try {
           
            const response = await axios.post(`/card/${token}`, {
                
                    userName,
                    cardNumber,
                    expirationDate,
                    cvv,
                    
                
            });

            console.log(response.data);

            
        } catch (error) {
            console.error('Error editing profile:', error);
            setErrorMessage('Error editing profile. Please try again.');
        }
    }




    return (
        <div>
            <Navbar />
            <div className={styles.container}>
                <div className={styles.form}>
                    <h1>User Profile</h1>
                    <form>
                        <label>User Name:</label>
                        <input type="text" value={userName} onChange={(e) => setUserName(e.target.value)} />

                        <label>Card Number:</label>
                        <input type="text" value={cardNumber} onChange={(e) => setCardNumber(e.target.value)} />

                        <label>Expiration Date:</label>
                        <input type="text" value={expirationDate} onChange={(e) => setExpirationDate(e.target.value)} />

                        <label>CVV:</label>
                        <input type="text" value={cvv} onChange={(e) => setCvv(e.target.value)} />

                        <label>Card Amount:</label>
                        <span>{amount}</span>

                        <button className={styles.button} onClick={(e) => {
                            e.preventDefault();
                            if (userName.trim() === '' || cardNumber.trim() === '' || expirationDate.trim() === '' || cvv.trim() === '') {
                                setErrorMessage('Please fill input fields!');
                            }else{
                            handleEditClick();
                            setErrorMessage('');
                            }
                        }}>
                            Save Changes
                        </button>
                        {errorMessage && <p className={styles['error-message']}>{errorMessage}</p>}
                    </form>
                </div>
            </div>
        </div>
    );
};

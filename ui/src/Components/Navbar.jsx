// Navbar.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Navbar.module.css';
import axios from 'axios';

export const Navbar = () => {
    const [navConst]
    const [error, setError] = useState('');
    const [adminToken, setAdminToken] = useState(localStorage.getItem('userToken'));
    const [componentDisabled, setComponentsDisabled] = useState(true);
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const userToken = localStorage.getItem('userToken');

            if (!userToken) {
                console.log('User token not found!');
                return;
            }

            await axios.post(`/logout/${userToken}`);
            localStorage.removeItem('userToken');
            navigate('/');
        } catch (error) {
            console.error('Error during logout: ', error.response ? error.response.data : error.message);
            setError('ErrorDuring logout. Please try again later');
        }
    }

    const handleCard = async () => {
        
        try {
            const userToken = localStorage.getItem('userToken');
    
            if (!userToken) {
                console.log('User token not found!');
                return;
            }
    
            const response = await axios.get(`/getUserCard/${userToken}`);
            
            if (response.data.message && response.data.message === 'Card not verified') {
                // Handle the case where the card is not verified
                console.log('Card not verified');
                konstanta = '/card'
            } else {
                
                const creditCardData = response.data;
                console.log('Verified Credit Card:', creditCardData);
                navigate('/verifiedCard');
            }
        } catch (error) {
            console.error('Error while fetching user card:', error);
            
    };
    useEffect(() => {
        if (!adminToken) {
            setComponentsDisabled(false);
        }
    }, [adminToken]);
    }
    return (
        <header>
            <nav>
                <ul className={styles.nav_links}>
                    <li>
                        <a href='/home'>Home</a>
                    </li>
                    {!componentDisabled ? (
                        <li>
                            <a href="/account">Verification</a>
                        </li>
                    ) : null}
                    {componentDisabled ? (
                        <li>
                            <a href={navConst}>Credit card</a>
                        </li>
                    ) : null}
                    
                    <li>
                        <a href="/transactionHistory">History</a>
                    </li>
                    {componentDisabled ? (
                        <li>
                            <a href="/editProfile">Edit profile</a>
                        </li>
                    ) : null}
                </ul>
            </nav>
            <a href="/">
                <button onClick={handleLogout}>Logout</button>
                {error}
            </a>
        </header>
    );
};

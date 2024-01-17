// Navbar.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Navbar.module.css';
import axios from 'axios';

export const Navbar = () => {
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
    useEffect(() => {
        if (!adminToken) {
            setComponentsDisabled(false);
        }
    }, [adminToken]);

    return (
        <header>
            <nav>
                <ul className={styles.nav_links}>
                    <li>
                        <a href='/home'>Home</a>
                    </li>
                    <li>
                        <a href="/account">Account</a>
                    </li>
                    {componentDisabled ? (
                        <li>
                            <a href="/card">Credit card</a>
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

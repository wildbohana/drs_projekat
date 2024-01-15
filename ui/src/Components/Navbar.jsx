// Navbar.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Navbar.module.css';
import axios from 'axios';

export const Navbar = () => {
    const [error, setError] = useState('');
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
                    <li>
                        <a href="/history">History</a>
                    </li>
                    <li>
                        <a href="/editProfile">Edit profile</a>
                    </li>
                </ul>
            </nav>
            <a href="/">
                <button onClick={handleLogout}>Logout</button>
                {error}
            </a>
        </header>
    );
};

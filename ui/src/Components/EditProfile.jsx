import React, { useState, useEffect } from "react";
import styles from './EditProfile.module.css';
import { Navbar } from './Navbar'
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const EditProfile = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');
    const [city, setCity] = useState('');
    const [state, setState] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const fetchUserProfile = async () => {
        try {
            const token = localStorage.getItem('userToken');
            const response = await axios.get(`/userProfile/${token}`);
            const userProfile = response.data;

            setFirstName(userProfile.firstName);
            setLastName(userProfile.lastName);
            setEmail(userProfile.email);
            setAddress(userProfile.address);
            setCity(userProfile.city);
            setState(userProfile.state);
            setPhoneNumber(userProfile.phoneNumber);
            setPassword(userProfile.password);
        } catch (error) {
            console.error('Error fetching user profile:', error);
        }
    };

    useEffect(() => {
        fetchUserProfile();
    }, []);

    const handleEditClick = async () => {
        try {
            const token = localStorage.getItem('userToken');
            const response = await axios.patch(`/userProfile/${token}`, {
                firstName,
                lastName,
                email,
                address,
                city,
                state,
                phoneNumber,
                password,
            });

            console.log(response.data);

            await fetchUserProfile();

            navigate('/');
        } catch (error) {
            console.error('Error editing profile:', error);
            setErrorMessage('Error editing profile. Please try again.');
        }
    };

    return (
        <div>
            <Navbar />
            <div className={styles.container}>
                <div className={styles.form}>
                    <h1>Edit profile</h1>
                    <form >
                        <input type="text" className={styles['form-input']} placeholder='Enter your new first name' value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                        <br />
                        <input type="text" className={styles['form-input']} placeholder='Enter your new last name' value={lastName} onChange={(e) => setLastName(e.target.value)} />
                        <br />
                        <input type="text" className={styles['form-input']} placeholder='Enter your new address' value={address} onChange={(e) => setAddress(e.target.value)} />
                        <br />
                        <input type="text" className={styles['form-input']} placeholder='Enter your new city' value={city} onChange={(e) => setCity(e.target.value)} />
                        <br />
                        <input type="text" className={styles['form-input']} placeholder='Enter your new state' value={state} onChange={(e) => setState(e.target.value)} />
                        <br />
                        <input type="number" className={styles['form-input']} placeholder='Enter your new phone number' value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} />
                        <br />
                        <input type="email" className={styles['form-input']} placeholder='Enter your new email' value={email} onChange={(e) => setEmail(e.target.value)} />
                        <br />
                        <input type="password" className={styles['form-input']} placeholder='Enter your new password' value={password} onChange={(e) => setPassword(e.target.value)} />
                        <br />
                        <button className={styles.button} onClick={(e) => {
                            e.preventDefault();
                            if (firstName.trim() === '' || lastName.trim() === '' || address.trim() === '' || city.trim() === '' || state.trim() === '' || phoneNumber.trim() === '' || email.trim() === '' || password.trim() === '') {
                                setErrorMessage('Please fill input fields!');
                            } else {
                                handleEditClick();
                                setErrorMessage('');
                            }
                        }}>Submit</button>
                        {errorMessage && <p style={{ color: 'red', textAlign: 'center', marginBottom: 20 }} > {errorMessage}</p>}
                    </form>
                </div>
            </div>
        </div>
    );
};
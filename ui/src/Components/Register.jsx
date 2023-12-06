import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export const Register = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [address, setAddress] = useState('');
    const [city, setCity] = useState('');
    const [state, setState] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const navigate = useNavigate();

    const handleRegister = async () => {
        try {
            const response = await axios.post('/register', {
                firstName,
                lastName,
                address,
                city,
                state,
                phoneNumber,
                email,
                password,
            });

            const successMessage = response.data;
            console.log(successMessage);

            setErrorMessage('');
            setSuccessMessage(successMessage);

        } catch (error) {
            console.error('Registration failed:', error.response ? error.response.data : error.message);
            setSuccessMessage('');
            setErrorMessage('Registration failed. Please check your details and try again.');
        }
    };

    const handleLoginClick = () => {
        navigate('/');
    }

    return (
        <div>
            <h1>Register</h1>
            <label>First Name:</label>
            <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
            <br />
            <label>Last Name:</label>
            <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} />
            <br />
            <label>Address:</label>
            <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} />
            <br />
            <label>City:</label>
            <input type="text" value={city} onChange={(e) => setCity(e.target.value)} />
            <br />
            <label>State:</label>
            <input type="text" value={state} onChange={(e) => setState(e.target.value)} />
            <br />
            <label>Phone number:</label>
            <input type="number" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} />
            <br />
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <br />
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <br />
            <button onClick={() => { handleRegister(); handleLoginClick(); }}>Register</button>

            {successMessage && <p style={{ color: 'green' }} > {successMessage}</p>}
            {errorMessage && <p style={{ color: 'red' }} > {errorMessage}</p>}
            <button onClick={handleLoginClick}>Back</button>
        </div>
    );
};

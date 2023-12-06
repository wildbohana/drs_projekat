import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios'

export const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await axios.post('/login', {
                email,
                password,
            });

            const { token } = response.data;
            console.log('Token', token);

            setSuccessMessage('Login successful!');
            setErrorMessage('');
        } catch (error) {
            console.error('Login failed:', error.response ? error.response.data : error.message);
            setErrorMessage('Login failed. Please check your credentials.');
            setSuccessMessage('');
        }
    };

    const handleRegisterClick = () => {
        navigate('/register');
    };

    const handleLoginSuccessfulClick = () => {
        navigate('/home');
    };

    return (
        <div>
            <h1>Login</h1>
            <label>Email:</label>
            <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
            <br />
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <br />
            <button onClick={() => { handleLogin(); handleLoginSuccessfulClick() }}>Login</button>
            <button onClick={handleRegisterClick}>Register</button>
            {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}

        </div>
    );
};

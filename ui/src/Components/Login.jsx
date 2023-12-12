import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios'
import './LoginAndRegister.css'

export const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
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
            setErrorMessage('');
            handleLoginSuccessfulClick();

        } catch (error) {
            console.error('Login failed:', error.response ? error.response.data : error.message);
            setErrorMessage('Login failed. Please check your credentials.');
        }
    };

    const handleLoginSuccessfulClick = () => {
        navigate('/home');
    };

    return (
        <div className='container'>
            <div className="login form">
                <h1>Login</h1>
                <form>
                    <input type="text" placeholder='Enter your email' className="form-input" value={email} onChange={(e) => setEmail(e.target.value)} />
                    <input type="password" placeholder='Enter your password' className="form-input" value={password} onChange={(e) => setPassword(e.target.value)} />
                    <button className='button' onClick={(e) => {
                        e.preventDefault();
                        if (email.trim() === '' || password.trim() === '') {
                            setErrorMessage('Please enter both email and password.');
                        } else {
                            handleLogin();
                            setErrorMessage('');
                        }
                    }}>Login</button>
                    {errorMessage && <p style={{ color: 'red', textAlign: 'center', marginBottom: 20 }}>{errorMessage}</p>}
                </form>
                <div className='signup'>
                    <span className='signup'>Don't have an account?
                        <a className='link' href='/register'>Signup</a>
                    </span>
                </div>
            </div>
        </div>
    );
};

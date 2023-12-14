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
            window.alert('Registration successful!');
        } catch (error) {
            console.error('Registration failed:', error.response ? error.response.data : error.message);
            setErrorMessage('Registration failed. Please check your details and try again.');
        }
    };


    const handleRegisterClick = () => {
        navigate('/');
    }

    return (
        <div className='container'>
            <div className='register form'>
                <h1>Register</h1>
                <form>
                    <input type="text" className="form-input" placeholder='Enter your first name' value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                    <br />
                    <input type="text" className="form-input" placeholder='Enter your last name' value={lastName} onChange={(e) => setLastName(e.target.value)} />
                    <br />
                    <input type="text" className="form-input" placeholder='Enter your address' value={address} onChange={(e) => setAddress(e.target.value)} />
                    <br />
                    <input type="text" className="form-input" placeholder='Enter your city' value={city} onChange={(e) => setCity(e.target.value)} />
                    <br />
                    <input type="text" className="form-input" placeholder='Enter your state' value={state} onChange={(e) => setState(e.target.value)} />
                    <br />
                    <input type="number" className="form-input" placeholder='Enter your phone number' value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} />
                    <br />
                    <input type="email" className="form-input" placeholder='Enter your email' value={email} onChange={(e) => setEmail(e.target.value)} />
                    <br />
                    <input type="password" className="form-input" placeholder='Enter your password' value={password} onChange={(e) => setPassword(e.target.value)} />
                    <br />
                    <button className='button' onClick={(e) => {
                        e.preventDefault();
                        if (firstName.trim() === '' || lastName.trim() === '' || address.trim() === '' || city.trim() === '' || state.trim() === '' || phoneNumber.trim() === '' || email.trim() === '' || password.trim() === '') {
                            setErrorMessage('Please fill input fields!');
                        } else {
                            handleRegister();
                            handleRegisterClick();
                            setErrorMessage('');
                        }
                    }}>Register</button>
                    {errorMessage && <p style={{ color: 'red', textAlign: 'center', marginBottom: 20 }} > {errorMessage}</p>}
                </form>
            </div>
        </div>
    );
};

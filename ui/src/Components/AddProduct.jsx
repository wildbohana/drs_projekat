import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export const AddProduct = () => {
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [currency, setCurrency] = useState('');
    const [amount, setAmount] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const navigate = useNavigate();

    const handleAddProduct = async () => {
        try {
            const response = await axios.post('/register', {
                name,
                price,
                currency,
                amount,
            });

            const successMessage = response.data;
            console.log(successMessage);

            setErrorMessage('');
            setSuccessMessage(successMessage);

        } catch (error) {
            console.error('Adding product failed:', error.response ? error.response.data : error.message);
            setSuccessMessage('');
            setErrorMessage('Adding product failed. Please check your details and try again.');
        }
    };

    const handleAddProductClick = () => {
        navigate('/home');
    }

    const handleBackClick = () => {
        navigate('/home');
    };

    return (
        <div>
            <h1>Register</h1>
            <label>Name:</label>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
            <br />
            <label>Price:</label>
            <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
            <br />
            <label>Currency:</label>
            <input type="text" value={currency} onChange={(e) => setCurrency(e.target.value)} />
            <br />
            <label>Amount:</label>
            <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
            <br />
            <br />
            <button onClick={() => { handleAddProduct(); handleAddProductClick(); }}>Add product</button>

            {successMessage && <p style={{ color: 'green' }} > {successMessage}</p>}
            {errorMessage && <p style={{ color: 'red' }} > {errorMessage}</p>}
            <button onClick={handleBackClick}>Back</button>
        </div>
    );
};
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export const AddProduct = () => {
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [currency, setCurrency] = useState('');
    const [amount, setAmount] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate();

    const handleAddProduct = async () => {
        try {
            const response = await axios.post('/addProduct', {
                name,
                price,
                currency,
                amount,
            });

            const successMessage = response.data;
            console.log(successMessage);
            setErrorMessage('');

        } catch (error) {
            console.error('Adding product failed:', error.response ? error.response.data : error.message);
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
        <div className='container'>
            <div className='product form'>
                <h1>Create product</h1>
                <input type="text" placeholder="Product name" className="form-input" value={name} onChange={(e) => setName(e.target.value)} />
                <input type="number" placeholder='Product price' className="form-input" value={price} onChange={(e) => setPrice(e.target.value)} />
                <input type="text" placeholder='Product currency' className="form-input" value={currency} onChange={(e) => setCurrency(e.target.value)} />
                <input type="number" placeholder='Product amount' className="form-input" value={amount} onChange={(e) => setAmount(e.target.value)} />
                <button className='button' onClick={(e) => {
                    e.preventDefault();
                    if (name.trim() === '' || price.trim() === '' || currency.trim() === '' || amount.trim() === '') {
                        setErrorMessage('Please fill input fields!');
                    } else {
                        handleAddProduct();
                        handleAddProductClick();
                        window.alert('Successfully created product');
                        setErrorMessage('');
                    }
                }}>Submit</button>
                <button className='button' onClick={handleBackClick}>Back</button>
                {errorMessage && <p style={{ color: 'red', textAlign: 'center', marginBottom: 20 }} > {errorMessage}</p>}
            </div>
        </div>
    );
};
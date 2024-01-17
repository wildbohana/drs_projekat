import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './TransactionHistory.module.css'
import { Navbar } from './Navbar';

export const TransactionHistory = () => {
    const [Transactions, setTransaction] = useState([]);
    const [adminToken, setAdminToken] = useState(localStorage.getItem('adminToken'));
    const [error, setError] = useState('');
    const [componentDisabled, setComponentDisabled] = useState(true);


    useEffect(() => {
        const fetchTransactions = async () => {
            let response;

            try {
                if (adminToken) {
                    response = await axios.get(`/transactionHistory/${adminToken}`);
                }
                else {
                    const token = localStorage.getItem('userToken')
                    response = await axios.get(`/transaction/${token}`);
                }
                if (response.data && Array.isArray(response.data)) {
                    setTransaction(response.data);
                    setError('');
                } else {
                    setError('Invalid response format. Please try again later.');
                }
            } catch (error) {
                console.error('Error fetching products: ', error.response ? error.response.data : error.message);
                setError('Error fetching products. Please try again later.');
            }

        }

        if (adminToken) {
            fetchTransactions();
            setComponentDisabled(false);
        }

    }, [adminToken]);


    return (
        <div>
            <Navbar />
            {!componentDisabled ? (

                <div className={styles.homeContainer}>

                    <table className={styles.productTable}>
                        <thead>
                            <tr>

                                <th>Sender</th>
                                <th>Receiver</th>
                                <th>Currency</th>
                                <th>Amount</th>
                                <th>State</th>
                                <th>Product</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Transactions.map((Transaction, index) => (
                                <tr key={index}>
                                    <td>{Transaction.sender}</td>
                                    <td>{Transaction.receiver}</td>
                                    <td>{Transaction.currency}</td>
                                    <td>{Transaction.amount}</td>
                                    <td>{Transaction.state}</td>
                                    <td>{Transaction.product}</td>

                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {error && <p style={{ color: 'red', marginBottom: 20 }}>{error}</p>}

                </div>
            ) : <div>
                <h1>test</h1>
            </div>}


        </div >
    );

};


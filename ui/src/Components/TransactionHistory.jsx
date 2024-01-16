import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './TransactionHistory.module.css'
import { Navbar } from './Navbar';

export const TransactionHistory = () => {
    const [Transactions, setTransaction] = useState([]);
    const [adminToken, setAdminToken] = useState(localStorage.getItem('adminToken'));
    const [componentDisabled, setComponentsDisabled] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchTransactions = async () => {
            try {
                const response = await axios.get('/transaction');
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

        fetchTransactions();
    }, []);

    useEffect(() => {
        if (adminToken) {
            setComponentsDisabled(false);
        }
    }, [adminToken]);

    return (
        <div>
            <Navbar />
            {/*prvi uslov(true) prikazuje admina*/
                !componentDisabled ? (
                    <div className={styles.homeContainer}>

                        <table className={styles.productTable}>
                            <thead>
                                <tr>
                                    <th></th>
                                    <th>Sender</th>
                                    <th>Receiver</th>
                                    <th>Currency</th>
                                    <th>Amount</th>
                                    <th>State</th>
                                    <th>Product</th>
                                </tr>
                            </thead>
                            <tbody>
                                {Transactions.map(Transaction => (
                                    <tr key={Transaction.sender}>
                                        <td>{Transaction.seceiver}</td>
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
                ) :
                    /*TO DO: prikaz istorije kupovine kupca */
                    (<div>TEST-KUPAC</div>)}
        </div >
    );
};


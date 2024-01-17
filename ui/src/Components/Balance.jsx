import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './Balance.module.css'
import { Navbar } from './Navbar';

export const Balance = () => {
    const [Balances, setTransaction] = useState([]);
    const [adminToken, setAdminToken] = useState(localStorage.getItem('adminToken'));
    const [error, setError] = useState('');



    useEffect(() => {
        const fetchBalances = async () => {
            let token;
            try{

                if(!adminToken)
                {
                    token = localStorage.getItem('userToken');

                }  
                else
                {
                     token = adminToken   
                }                
            
                const response = await axios.get(`/accountBalance/${token}`);                  

                if (response.data && Array.isArray(response.data)) {
                    setTransaction(response.data);
                    setError('');
                } else {
                    setError('No balance');
                }
            }catch(error)
            {
                console.error("Error fetching balance", error.response ? error.response.data : error.message)
            }
        }
        
        if (adminToken || localStorage.getItem('userToken')) {
            fetchBalances();            
        }

    }, []);


    return (
        <div>
            <Navbar />
            (

                <div className={styles.homeContainer}>

                    <table className={styles.productTable}>
                        <thead>
                            <tr>                               
                                <th>Currency</th>
                                <th>Amount</th>                                
                            </tr>
                        </thead>
                        <tbody>
                            {Balances.map((Balance) => (
                                <tr key={Balance.accountNumber}>
                                    <td>{Balance.currency}</td>
                                    <td>{Balance.amount}</td>                                    

                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {error && <p style={{ color: 'red', marginBottom: 20 }}>{error}</p>}

                </div>
            ) : 

        </div >
    );

};


import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Home.module.css'
import styles1 from './Navbar.module.css'

export const Home = () => {
    const [products, setProducts] = useState([]);
    const [error, setError] = useState('');

    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get('/getAllProducts');

                if (response.data && Array.isArray(response.data)) {
                    setProducts(response.data);
                    setError('');
                } else {
                    setError('Invalid response format. Please try again later.');
                }
            } catch (error) {
                console.error('Error fetching products: ', error.response ? error.response.data : error.message);
                setError('Error fetching products. Please try again later.');
            }
        };
        fetchProducts();
    }, []);
    const handleNewProduct = () => {
        navigate('/addProduct');
    }

    const handleLogout = async () => {
        try {
            const userToken = localStorage.getItem('userToken');

            if (!userToken) {
                console.log('User token not found!');
                return;
            }

            await axios.post(`/logout/${userToken}`);
            localStorage.removeItem('userToken');
            navigate('/');
        } catch (error) {
            console.error('Error during logout: ', error.response ? error.response.data : error.message);
            setError('ErrorDuring logout. Please try again later');
        }
    }

    const handleAmountChange = async (productId, newAmount) => {
        try {
            const response = await axios.patch(`/changeAmount/${productId}`, {
                amount: newAmount
            });
            console.log(response.data);
            setProducts(prevProducts => prevProducts.map(product => product.id === productId ? { ...product, amount: newAmount } : product));
            setError('');
        } catch (error) {
            console.error('Error updationg product amount:', error.response ? error.response.data : error.message);
            setError('Error during update amount');
        }
    };

    return (
        <div>
            <header>
                <nav>
                    <ul className={styles1.nav_links}>
                        <li>
                            <a href="/home">Home</a>
                        </li>
                        <li>
                            <a href="#">Account</a>
                        </li>
                        <li>
                            <a href="#">History</a>
                        </li>
                        <li>
                            <a href="#">Edit profile</a>
                        </li>
                    </ul>
                </nav>
                <a href="/"><button onClick={handleLogout}>Logout</button></a>
            </header>
            <div className={styles.homeContainer}>

                <table className={styles.productTable}>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Price</th>
                            <th>Currency</th>
                            <th>Amount</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {products.map(product => (
                            <tr key={product.id}>
                                <td>{product.name}</td>
                                <td>{product.price}</td>
                                <td>{product.currency}</td>
                                <td>
                                    <input style={{ width: 100 }}
                                        type="number"
                                        value={product.amount}
                                        onChange={(e) => handleAmountChange(product.id, e.target.value)}
                                    />
                                </td>

                            </tr>
                        ))}
                    </tbody>
                </table>
                {error && <p style={{ color: 'red', marginBottom: 20 }}>{error}</p>}
                <div className={styles.divHomeButtons}>
                    <button className={styles.homeButton} onClick={handleNewProduct}>Add new</button>
                </div>
            </div>
        </div >
    );
};


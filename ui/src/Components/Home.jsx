import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Home.module.css'
import { Navbar } from './Navbar';

export const Home = () => {
    const [products, setProducts] = useState([]);
    const [selectedProductId, setSelectedProductId] = useState(null);
    const [adminToken, setAdminToken] = useState(localStorage.getItem('adminToken'));
    const [componentsDisabled, setComponentsDisabledd] = useState(true);
    const [error, setError] = useState('');
    const [sortOrder, setSortOrder] = useState('asc');
    const [sortBy, setSortBy] = useState(null);

    const navigate = useNavigate();

    const handleSort = (column) => {
        const newOrder = sortOrder === 'asc' ? 'desc' : 'asc';
        setSortOrder(newOrder);
        setSortBy(column);

        const sortedProducts = [...products];
        sortedProducts.sort((a, b) => {
            if (column === 'name') {
                const comparison = a.name.localeCompare(b.name);
                return newOrder === 'asc' ? comparison : -comparison;
            } else if (column === 'amount') {
                return newOrder === 'asc' ? a.amount - b.amount : b.amount - a.amount;
            } else if (column === 'price') {
                return newOrder === 'asc' ? a.price - b.price : b.price - a.price;
            } else if (column === 'currency') {
                const comparison = a.currency.localeCompare(b.currency);
                return newOrder === 'asc' ? comparison : -comparison;
            }
            return 0;
        });
        setProducts(sortedProducts);
    };
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

    useEffect(() => {
        if (adminToken) {
            setComponentsDisabledd(false);
        }
    }, [adminToken]);

    const handleNewProduct = () => {
        navigate('/addProduct');
    }

    const handleCheckboxChange = (productId) => {
        setSelectedProductId(productId);
    };

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
            <Navbar />
            <div className={styles.homeContainer}>
                <table className={styles.productTable}>
                    <thead>
                        <tr>{componentsDisabled ? (
                            <th></th>
                        ) : ""}
                            <th onClick={() => handleSort('name')}>Name
                                {sortBy === 'name' && <span>{sortOrder === 'asc' ? ' ▲' : ' ▼'}</span>}
                            </th>
                            <th onClick={() => handleSort('price')}>Price
                                {sortBy === 'price' && <span>{sortOrder === 'asc' ? ' ▲' : ' ▼'}</span>}
                            </th>
                            <th onClick={() => handleSort('currency')}>Currency
                                {sortBy === 'currency' && <span>{sortOrder === 'asc' ? ' ▲' : ' ▼'}</span>}
                            </th>
                            <th onClick={() => handleSort('amount')}>Amount
                                {sortBy === 'amount' && <span>{sortOrder === 'asc' ? ' ▲' : ' ▼'}</span>}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {products.map(product => (
                            <tr key={product.id}>
                                {componentsDisabled ? (
                                    <td>
                                        <input
                                            type="checkbox"
                                            checked={selectedProductId === product.id}
                                            onChange={() => handleCheckboxChange(product.id)}
                                        />
                                    </td>
                                ) : null}

                                <td>{product.name}</td>
                                <td>{product.price}</td>
                                <td>{product.currency}</td>
                                <td>
                                    {!componentsDisabled ? (
                                        <input style={{ width: 100 }}
                                            type="number"
                                            value={product.amount}
                                            onChange={(e) => handleAmountChange(product.id, e.target.value)}
                                        />
                                    ) : (
                                        <span>{product.amount}</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {error && <p style={{ color: 'red', marginBottom: 20 }}>{error}</p>}
                <div className={styles.divHomeButtons}>
                    {!componentsDisabled && (
                        <button className={styles.homeButton} onClick={handleNewProduct} >Add new</button>
                    )}
                </div>
            </div>
        </div >
    );
};

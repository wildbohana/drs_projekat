import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export const Home = () => {
    const [products, setProducts] = useState([]);
    const [error, setError] = useState('');
    const [productId] = useState(1);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get(`/getProduct/${productId}`);

                if (response.data && typeof response.data === 'object') {

                    setProducts([response.data]);
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
    }, [productId]);
    const handleNewProduct = () => {
        navigate('/addProduct');
    }


    return (
        <div>
            <h2>Product List</h2>
            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Currency</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map(product => (
                        <tr key={product.id}>
                            <td>{product.id}</td>
                            <td>{product.name}</td>
                            <td>{product.price}</td>
                            <td>{product.currency}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {error && <p>{error}</p>}
            <button onClick={handleNewProduct}>Add new product</button>
        </div>

    );
};


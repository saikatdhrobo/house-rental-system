import React from 'react'

import styles from '../components/ProductDetails.module.css'
import AdminNavbar from './AdminNavbar';
import { useParams } from 'react-router-dom';

const ProductDetails = () => {
    const { id } = useParams()
    return (
        <>
            <AdminNavbar />
            <h2>Testing {id}</h2>
        </>
    );
}

export default ProductDetails;
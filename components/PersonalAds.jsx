import React from 'react'
import { useState, useEffect } from "react";
import HomePageNavbar from './HomePageNavbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'
import URL from "../URL"
import styles from '../components/PersonalAds.module.css'


const PersonalAds = () => {
    const { register, handleSubmit } = useForm()
    const [token, setToken] = useState(sessionStorage.getItem("token") || '')
    const serverURL = URL()
    const navigate = useNavigate()

    const formSubmit = (data) => {
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
        axios.post(`${serverURL}/rents`, data, {headers:headers} ).then(res =>{
            if(res.status == 201){
                navigate('/dashboard')
            }else{
                alert('something went wrong!')
            }
        })
    }
    useEffect(() => {
        if (!token) {
            navigate('/signin')
        }
    },[token])
    return (
        <>
            <HomePageNavbar className={styles.navcontainer} />
            <div>
                <div>
                    <div className="container">
                        <Form onSubmit={handleSubmit(formSubmit)}>
                            <Form.Group className="mb-3" controlId="formBasicEmail">
                                <Form.Label><b>Title</b></Form.Label>
                                <Form.Control required {...register('title')} type="text" placeholder="Enter title" />

                            </Form.Group>

                            <Form.Group className="mb-3" controlId="formBasicPassword">
                                <Form.Label><b>Description</b></Form.Label>
                                <Form.Control required {...register('description')} as="textarea" type="text" placeholder="Description" />
                            </Form.Group>

                            <Form.Group className="mb-3" controlId="formBasicPassword">
                                <Form.Label><b>Location</b></Form.Label>
                                <Form.Control required {...register('location')} type="text" placeholder="Location" />
                            </Form.Group>
                            <Form.Group className="mb-3" controlId="formBasicPassword">
                                <Form.Label><b>Price</b></Form.Label>
                                <Form.Control required {...register('price')} type="number" placeholder="Price" />
                            </Form.Group>

                            <Button variant="success" type="Submit" className={styles.Button}>
                                Submit
                            </Button>
                            <Button variant="danger" size="sm">cancel</Button>
                        </Form>
                    </div>
                </div>
            </div>
        </>
    );
}

export default PersonalAds;
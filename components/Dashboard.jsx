import React, { useEffect, useState } from 'react'
import { Route, Routes, useNavigate } from 'react-router-dom'

import URL from '../URL'
import axios from 'axios'
import styles from '../components/Dashboard.module.css'
import HomePageNavbar from './HomePageNavbar'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Col, Row } from 'react-bootstrap'





const Dashboard = () => {
    const [token, setToken] = useState(sessionStorage.getItem("token") || '')
    const [rents, setRents] = useState([])
    const navigate = useNavigate()
    const serverURL = URL()
    const [projects, setProjects] = useState([])

    useEffect(() => {
        axios.get(`${serverURL}/rents/all`).then(res => setRents(res.data))
    }, [])

    useEffect(() => {
        if (!token) {
            navigate('/signin')
        }
        else {
            axios.get(`${serverURL}/users/me`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(response => {
                    if (response.status == 200) {
                        // console.log(typeof(response.data));

                    }
                })
                .catch(error => {
                    navigate('/signin')
                })
        }
    }, [])


    function handleDelete(id){
        axios.delete(`${serverURL}/rents/${id}`).then(() => {
            alert("deletion successful")
            window.location.reload()
        }).catch((e) => {
            // alert("deletion failed")
            console.log(e)
        })
    }

    return (
        <div className={styles.mainContainer}>
            

            <HomePageNavbar />
            <div className={styles.cardContainer}>
                <Row className='gap-2'>
                    {rents && rents.map((rent) => <Col lg={5} key={rent.id}>
                        <Card >
                            <Card.Body className={styles.mainCard}>
                                <Card.Title>{rent.title}</Card.Title>
                                <Card.Text><b>Description: </b>{rent.description}</Card.Text>
                                <Card.Text><b>Price: </b>{rent.price}</Card.Text>
                                <Card.Text><b>location: </b>{rent.location}</Card.Text>
                                <Card.Text><b>Posted by: </b>{rent.user.first_name}</Card.Text>
                                <Card.Text><b>Posted by: </b>{rent.user.contact}</Card.Text>
                                
                                <button onClick={() => handleDelete(rent.id)}>Delete</button>
                            </Card.Body>
                        </Card>
                    </Col>)}
                </Row>
            </div>




        </div>
    );
}

export default Dashboard;
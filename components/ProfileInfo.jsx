import React from 'react'
import { useState, useEffect } from 'react'
import axios from 'axios'
import URL from '../URL'
import { useNavigate } from 'react-router-dom'
import styles from '../components/ProfileInfo.module.css'

const ProfileInfo = () => {
  const [token, setToken] = useState(sessionStorage.getItem("token") || '')
    const serverURL = URL()
    const navigate = useNavigate()

    const [firstName, setFirstName] = useState('')
    const [lasttName, setLastName] = useState('')
    const [email, setEmail] = useState('')
    const [contact, setContact] = useState('')
    const [acCreated, setAcCreated] = useState('')

    const [active, setActive] = useState(1); // to manage active p tag

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
                        // console.log(response);
                        setFirstName(response.data.first_name)
                        setLastName(response.data.last_name)
                        setEmail(response.data.email)
                        setContact(response.data.contact)
                        setAcCreated(response.data.ac_creation)
                        console.log(response.data.contact);

                    }
                })
                .catch(error => {
                    console.log(error);
                    navigate('/signin')
                })
        }
    }, [])
  return (
<div className={styles.mainContainer} style={{ display: 'flex', alignItems: 'center' }}>
  {/* Profile Picture */}
  <div className={styles.pictureContainer} style={{ marginRight: '20px' }}>
    <img src="https://cdn.imgpile.com/f/eec7fZN_xl.jpg" alt="profile picture" />
  </div>

  {/* Information Section */}
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
    <p><b>First Name:</b> {firstName}</p>
    <p><b>Last Name:</b> {lasttName}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Contact:</b> {contact}</p>
    <p><b>Account Creation Date:</b> {acCreated}</p>
  </div>
</div>

  );
}

export default ProfileInfo;
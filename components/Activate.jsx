import React, { useEffect, useState } from 'react'
import styles from '../components/Activate.module.css'
import { useLocation, useNavigate } from 'react-router-dom';

import URL from '../URL';
import axios from 'axios';

const Activate = () => {
  // const location = useLocation();
  const [OTP, setOTP] = useState('');
  const [email, setEmail] = useState(sessionStorage.getItem("email") || "");
  const BACKEND_URL = `${URL()}/otp`

  const navigate = useNavigate();
  useEffect(() => {

    if (!email) {
      navigate("/signin");
    }
    else {
      axios.get(`${BACKEND_URL}/send/${email}`)
      sessionStorage.removeItem("email")
    }

  }, [])


  function verifyEmail(e) {
    e.preventDefault();

    const data = {
      email: email,
      otp: OTP
    }

    axios.post(`${BACKEND_URL}/verify/`, data)
      .then(response => {
        if (response.status == 200) {
          alert("Account Created")
          navigate('/signin')

        }
      })
      .catch(error => {
        alert(`Server says "${error.response.data.message}"`)
      })
  }

  return (
    <div className={styles.mainContainer}>
      <form onSubmit={verifyEmail} className={styles.inputs}>
        <h3>To activate your account, please verify your email address.</h3>
        <h5>Check your email, we sent an OTP. This is a one time verification.</h5>
        <input type="email" value={email} readOnly className={styles.email} />
        <input type="number" required placeholder='OTP' onChange={(e) => setOTP(e.target.value)} />
        <input type="submit" value='Verify OTP' className={styles.verifyButton} />

      </form>
    </div>
  );

}

export default Activate;
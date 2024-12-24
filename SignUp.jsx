import React, { useState } from 'react'
import styles from '../components/SignUp.module.css'
import axios from 'axios'
import Navbar from './Navbar';
import URL from '../URL';
import { useNavigate } from 'react-router-dom';
const SignUp = () => {

  const serverURL = `${URL()}/user`;
  const navigate = useNavigate();

  const [firstName, setFirstName] = useState('')
  const [lasttName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [contact, setContact] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  function createAccount(e) {
    e.preventDefault();
    if (password != confirmPassword) {
      alert("Password did not match.")
    }

    else {
      const userData = {
        first_name: firstName,
        last_name: lasttName,
        email: email,
        contact: contact,
        password: password,
      }

      axios.post(serverURL, userData).
        then(res => {
          if (res.status === 201) {
            sessionStorage.setItem('email', email);
            alert("Registration Successful");
            navigate('/activate');
          }
        }).
        catch(err => {
          if (err.status === 400) {
            alert("This email or contact number is already registered.")
          }
          else {
            alert("Something went worng.\nPlease Try again later.")
          }
        })

    }
  }

  return (
    <>
      <Navbar />
      <div className={styles.mainContainer}>

        <h2 className={styles.headline}>Register Your Account</h2>

        <form className={styles.inputs} onSubmit={createAccount}>
          <input type="text" placeholder='First Name' required onChange={(e) => setFirstName(e.target.value)} />
          <input type="text" placeholder='Last Name' required onChange={(e) => setLastName(e.target.value)} />
          <input type="email" placeholder='Email' required onChange={(e) => setEmail(e.target.value)} />
          <input type="number" placeholder='Contact Number' required onChange={(e) => setContact(e.target.value)} />
          <input type="password" placeholder='Password' required minLength={8} maxLength={32} onChange={(e) => setPassword(e.target.value)} />
          <input type="password" placeholder='Confirm Password' minLength={8} maxLength={32} required onChange={(e) => setConfirmPassword(e.target.value)} />
          <input type='submit' className={styles.submitButton} value='Sign Up' />
        </form>

      </div>
    </>
  );
}

export default SignUp;
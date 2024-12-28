import React from 'react'
import styles from '../components/Navbar.module.css'
import { Link, NavLink } from 'react-router-dom';
const Navbar = () => {
    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h2>&reg;</h2>
                <p className={styles.webName}>RentEase</p>
            </div>

            <div className={styles.listContainer}>
                <ul className={styles.navlist}>
                    <NavLink to='/' ><h2>Homepage</h2></NavLink>
                </ul>
            </div>

            <div className={styles.buttons}>
                <li className={styles.buttonList}>
                    <NavLink to='/signin'><button className={styles.signin}>Sign In</button></NavLink>
                    <NavLink to='/signup'><button className={styles.signup}>Sign Up</button></NavLink>
                </li>
            </div>
            

        </div>
        
        
    );
}

export default Navbar;
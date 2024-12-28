import React from 'react'
import Navbar from './Navbar';
import { Collection } from 'mongoose';



const Home = () => {
  return (
    <>
      <Navbar />
    <div className='container' >

    <section>
        <h2></h2>
        <div>
        </div>
    </section>
    <section>
        <h2 color='purple' >About</h2>
        <p color='purple'>This project is a web-based house rental management system. It provides a platform for users to browse available rental properties. Users can create and manage their own rental listings, including adding and updating details. The system also facilitates the management of rental inquiries from potential tenants. The primary goal is to streamline and simplify the house rental process. This involves making the process more accessible to both landlords and tenants. The system aims to provide a more organized approach to rental management. Ultimately, it seeks to create a user-friendly experience for all parties involved in the rental process.
        </p>
    </section>
<hr />
    <section>
        <h2>Features</h2>
        <ul>
            <li>View rental listings with detailed information.</li>
            <li>Create, update, and delete rental listings.</li>
            <li>User authentication and role management for regular users.</li>
            <li>Contact form for inquiries.</li>
            <li>Still under improvement</li>
        </ul>
    </section>

<hr />
    <section>
        <h2>Contact</h2>
        <div>
        <table border={3}>  <thead>
    <tr>
      <th>Name</th>
      <th>ID</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Kowsar</td>
      <td>2001041</td>
      <td><a href="https://bdu.ac.bd/">kowsarislam@gmail.com</a></td>
    </tr>
    <tr>
      <td>Siam</td>
      <td>1901012</td>
      <td><a href="https://bdu.ac.bd/">siamislam@gmail.com</a></td>
    </tr>
    <tr>
      <td>Saikat</td>
      <td>2001022</td>
      <td><a href="https://bdu.ac.bd/">saikat@gmail.com</a></td>
    </tr>
    <tr>
      <td>Fahim</td>
      <td>2001017</td>
      <td><a href="https://bdu.ac.bd/">fahim@gmail.com</a></td>
    </tr>
  </tbody>
</table>
        </div>
    </section>

<hr />

    </div>
    </>
  );
}

export default Home;
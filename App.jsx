import React from 'react'
import Navbar from './components/Navbar';

import { Routes, Route } from 'react-router-dom';

import Home from './components/Home'
import SignUp from './components/SignUp'
import Footer from './components/Footer';
import Activate from './components/Activate';
import SignIn from './components/SignIn';
import Dashboard from './components/Dashboard'
import PersonalAds from './components/PersonalAds';
import AdminDashboard from './components/AdminDashboard';
import ProductDetails from './components/ProductDetails';
import ProfileInfo from './components/ProfileInfo';



const App = () => {
  return (
    <div className='app-container'>

      <Routes>
        <Route path='' element={<Home />} />
        <Route path='profile' element={<ProfileInfo />} />
        <Route path='signup' element={<SignUp />} />
        <Route path='activate' element={<Activate />} />
        <Route path='signin' element={<SignIn />} />
        <Route path='dashboard' element={<Dashboard />} />
        <Route path='rents' element={<PersonalAds />} />
        <Route path='admin' element={<AdminDashboard />} />
        <Route path='project-detail/:id' element={<ProductDetails />} />
      </Routes>

      <Footer />
    </div>
  );
}

export default App;

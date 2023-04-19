import React from 'react'
import { useAuth } from '../../Firebase/AuthContext';
import Navbar from '../../components/Navbar/Navbar';

const Notifications = () => {
    const { userMode } = useAuth();
  return (
    <>
        <Navbar part="Notifications" mode="none" />
    </>
  )
}

export default Notifications
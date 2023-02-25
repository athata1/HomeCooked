import React from 'react'
import { useState } from 'react';
import Navbar from '../../components/Navbar/Navbar';
import { useAuth } from '../../Firebase/AuthContext';

const Dashboard = () => {
  const [userMode, setUserMode] = useState("consumer");
  const { currentUser, signout } = useAuth()

  return (
    <div className="dashboard">
      <Navbar />
      Dashboard
      <code>{currentUser ? JSON.stringify(currentUser) : ""}</code>
    </div>
    
  )
}

export default Dashboard
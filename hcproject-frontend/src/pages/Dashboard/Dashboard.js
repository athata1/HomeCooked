import React from 'react'
import { useState } from 'react';
import Navbar from '../../components/Navbar/Navbar';

const Dashboard = () => {
  const [userMode, setUserMode] = useState("consumer");
  return (
    <div className="dashboard">
      <Navbar placeholder="Search..." />
      Dashboard
    </div>
    
  )
}

export default Dashboard
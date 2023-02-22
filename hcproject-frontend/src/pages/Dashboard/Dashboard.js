import React from 'react'
import { useState } from 'react';
import Navbar from '../../components/Navbar/Navbar';
import { useAuth } from '../../Firebase/AuthContext';
import { useLocation, Navigate } from "react-router-dom";

const Dashboard = () => {
  const [userMode, setUserMode] = useState("consumer");
  const { currentUser, signout } = useAuth()

  let location = useLocation()
  if (currentUser === null) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return (
    <div className="dashboard">
      <Navbar/>
      Dashboard
      {currentUser ? currentUser.email : ""}
    </div>
    
  )
}

export default Dashboard
import React from 'react'
import { useState, useEffect } from 'react';
import Navbar from '../../components/Navbar/Navbar';
import { useAuth } from '../../Firebase/AuthContext';

const Dashboard = () => {
  const [userMode, setUserMode] = useState("consumer");
  const { currentUser, signout, getToken } = useAuth()
  const [token, setToken] = useState();
  useEffect(() => {
    getToken().then((t) => {
      setToken(t);
    })
  }, [])

  return (
    <div className="dashboard">
      <Navbar />
      Dashboard
      <code>{currentUser ? token : ""}</code>
    </div>
    
  )
}

export default Dashboard
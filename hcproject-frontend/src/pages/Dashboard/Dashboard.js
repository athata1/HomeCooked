import React from 'react'
import { useState, useEffect } from 'react';
import Navbar from '../../components/Navbar/Navbar';
import { useAuth } from '../../Firebase/AuthContext';

const Dashboard = () => {
  const { currentUser, getToken, userMode, setUserMode } = useAuth()
  const [token, setToken] = useState();
  
  useEffect(() => {
    getToken().then((t) => {
      setToken(t);
    })
  }, [])

  return (
    <div className="dashboard">
      <Navbar part="Posts" mode={userMode}/>
      Dashboard
      <code>{currentUser ? token : ""}</code>
    </div>
    
  )
}

export default Dashboard
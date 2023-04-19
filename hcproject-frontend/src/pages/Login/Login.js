import React, {useRef, useState} from 'react'
import {Link} from "react-router-dom"
import "./Login.css"
import { useAuth } from '../../Firebase/AuthContext'
import { useLocation, Navigate } from "react-router-dom";
import { Store } from 'react-notifications-component';
function createNotification(messageTitle, messageMessage, messageType) {
  Store.addNotification({
    title: messageTitle,
    message: messageMessage,
    type: messageType,
    insert: "top",
    container: "top-center",
    animationIn: ["animate__animated", "animate__fadeIn"],
    animationOut: ["animate__animated", "animate__fadeOut"],
    dismiss: {
      duration: 1000,
      onScreen: true
    }
  })
}

export default function Login() {

  const emailRef = useRef()
  const passwordRef = useRef()
  const [isLoading, setIsLoading] = useState(false);

  const {currentUser, login} = useAuth();
  let location = useLocation()
  if (currentUser !== null) {
    return <Navigate to="/dashboard" state={{ from: location }} replace />
  }

  const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

  async function handleSubmit(e) {
    e.preventDefault()

    console.log(emailRef.current.value)
      
    if (!validateEmail(emailRef.current.value)) {
      createNotification('Error', 'Please enter a valid email', 'danger')
      return;
    }

    if (passwordRef.current.value.length < 6) {
      createNotification('Error', 'Password must have length of at least 6', 'danger')

      return;
    }

    try {
      setIsLoading(true)
      await login(emailRef.current.value, passwordRef.current.value)
      console.log("Success!")
    }
    catch (e){
      createNotification('Error', 'Failed to login to account', 'danger')
      console.log(e);
    }
    setIsLoading(false);
  }

  return (
    <>
      <div className="login-background"></div>
      <div className="login">
        <div className="login-loginform">
          <div className="login-title">HomeCooked</div>
          <input ref={emailRef} className="login-input" type="email" placeholder='Enter Email Address'></input>
          <input ref={passwordRef} className="login-input" type="password" placeholder='Enter Password'></input>
          <button disabled={isLoading} onClick={(e) => {handleSubmit(e)}} className="login-button">Login</button>
          <div className='signup-forgot-links'>
          <Link to="/signup" style={{ textDecoration: 'none' }}>
            <div className="signup-link">Sign Up</div>
          </Link>
          <Link to="/reset" style={{ textDecoration: 'none' }}>
            <div className='forgot-password-link'>Forgot Password</div>
          </Link>
          </div>
        </div>
      </div>
    </>
  )
}

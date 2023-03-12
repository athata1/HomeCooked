import React, {useRef, useState} from 'react'
import {Link} from "react-router-dom"
import "./ChangePassword.css"
import { useAuth } from '../../Firebase/AuthContext'
import { useLocation, Navigate } from "react-router-dom";

export default function ChangePassword() {

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
      alert("Error: Please enter a valid email")
      return;
    }

    if (passwordRef.current.value.length < 6) {
      alert("Error: Password must have length of at least 6");
      return;
    }

    try {
      setIsLoading(true)
      await login(emailRef.current.value, passwordRef.current.value)
      console.log("Success!")
    }
    catch (e){
      alert("Failed to login to account")
      console.log(e);
    }
    setIsLoading(false);
  }

  return (
    <>
      <div className="change-password-background"></div>
      <div className="change-password">
        <div className="change-password-changepasswordform">
          <div className="change-password-title">Reset Password</div>
          <input ref={emailRef} className="change-password-input" type="email" placeholder='Enter Email Address'></input>
          <button disabled={isLoading} onClick={(e) => {handleSubmit(e)}} className="change-password-button">Submit</button>
        </div>
      </div>
    </>
  )
}

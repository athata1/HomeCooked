import React, {useRef, useState} from 'react'
import {Link} from "react-router-dom"
import "./ChangePassword.css"
import { useAuth } from '../../Firebase/AuthContext'
import { useLocation, Navigate } from "react-router-dom";

export default function ChangePassword() {

  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [succes, setSuccess] = useState(false);

  const {currentUser, resetPassword} = useAuth();
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

  if (succes) {
    return (
      <>
        <div className="change-password-background"></div>
        <div className="change-password">
          <div className="change-password-changepasswordform">
            <div>
            We sent an email to the provided email address. From there, you will be able to reset your password. If you did not receive the email, please click <span onClick={(e) => {handleSubmit(e)}} style={{display: "inline-block", textDecoration: "underline", cursor: "pointer"}}>Here</span>&nbsp; to receive another one.
            </div>
          </div>
        </div>
      </>
    )
  }

  async function handleSubmit(e) {
    e.preventDefault()

      
    if (!validateEmail(email)) {
      alert("Error: Please enter a valid email")
      return;
    }

    try {
      setIsLoading(true)
      resetPassword(email);
      console.log("Password email sent!")
      setSuccess(true);
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
          <input className="change-password-input" type="email" placeholder='Enter Email Address' 
          onChange={(e) => {setEmail(e.target.value)}}
          value={email}
          ></input>
          <button disabled={isLoading} onClick={(e) => {handleSubmit(e)}} className="change-password-button">Submit</button>
        </div>
      </div>
    </>
  )
}

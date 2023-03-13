import React, {useRef, useState} from 'react'
import "./ResetPassword.css"
import { useAuth } from '../../Firebase/AuthContext'
import { useLocation, Navigate } from "react-router-dom";

export default function ResetPassword() {

  const confirmPasswordRef = useRef()
  const passwordRef = useRef()
  const [isLoading, setIsLoading] = useState(false);

  const {currentUser, login} = useAuth();
  let location = useLocation()
  if (currentUser !== null) {
    return <Navigate to="/dashboard" state={{ from: location }} replace />
  }

  async function handleSubmit(e) {
    e.preventDefault()
    
    if (passwordRef.current.value.length < 6) {
      alert("Error: Password must have length of at least 6");
      return;
    }

    if (passwordRef.current.value !== confirmPasswordRef.current.value) {
      alert("Error: Passwords do not match")
      return;
    }
  }

  return (
    <>
      <div className="reset-background"></div>
      <div className="reset">
        <div className="reset-resetform">
          <div className="reset-title">Change Password</div>
          <input ref={passwordRef} className="reset-input" type="password" placeholder='Enter Password'></input>
          <input ref={confirmPasswordRef} className="reset-input" type="password" placeholder='Confirm Password'></input>
          <button disabled={isLoading} onClick={(e) => {handleSubmit(e)}} className="reset-button">Change Password</button>
        </div>
      </div>
    </>
  )
}

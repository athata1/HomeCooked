import React, {useRef, useState} from 'react'
import "./ResetPassword.css"
import { useAuth } from '../../Firebase/AuthContext'
import { useLocation, Navigate, useSearchParams, useNavigate } from "react-router-dom";

export default function ResetPassword() {

  const confirmPasswordRef = useRef()
  const passwordRef = useRef()
  const [queryParams] = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const {currentUser, changeResetPassword} = useAuth();
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

    setIsLoading(true);
    console.log(queryParams.get("oobCode"));
    changeResetPassword(queryParams.get("oobCode"), passwordRef.current.value).then(() => {
      console.log("Changed Password");
      setIsLoading(false);
      navigate("/login");

    }).catch(() => {
      console.log("Error while changing password")
      alert("Error while Changing password")
    }).finally(() => {
      setIsLoading(false);
    })
    
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

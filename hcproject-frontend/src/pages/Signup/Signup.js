import React from 'react'
import {Link} from "react-router-dom"
import "./Signup.css"


export default function Signup() {
  return (
    <>
      <div className="signup-background"></div>
      <div className="signup">
        <div className="signup-signupform">
          <div className="signup-title">HomeCooked</div>
          <input className="signup-input" type="email" placeholder='Enter Email Address'></input>
          <input className="signup-input" type="text" placeholder='Enter Username'></input>
          <input className="signup-input" type="password" placeholder='Enter Password'></input>
          <input className="signup-input" type="password" placeholder='Confirm Password'></input>
          <button className="signup-button" disabled={false}>Sign Up</button>
        <div className="signup-login">Already have an account: <Link to="/login" style={{ textDecoration: 'none' }}><span className="signup-login-link">Login</span></Link></div>
        </div>
      </div>
    </>
  )
}

import React from 'react'
import {Link} from "react-router-dom"
import "./Login.css"


export default function Login() {
  return (
    <div className="login">
      <div className="login-background"></div>
      <div className="login-signupform">
        <div className="login-title">HomeCooked</div>
        <input className="login-input" type="email" placeholder='Enter Email Address'></input>
        <input className="login-input" type="password" placeholder='Enter Password'></input>
        <button className="login-button" disabled={false}>Login</button>
        <div className='signup-forgot-links'>
        <Link to="/signup" style={{ textDecoration: 'none' }}>
          <div className="signup-link">Sign Up</div>
        </Link>
          <div className='forgot-password-link'>Forgot Password</div>
        </div>
      </div>
    </div>
  )
}

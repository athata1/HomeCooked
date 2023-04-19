import React, { useRef, useState } from "react";
import { Link } from "react-router-dom";
import "./Signup.css";
import { useAuth } from "../../Firebase/AuthContext";
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
export default function Signup() {
  const emailRef = useRef();
  const passwordRef = useRef();
  const confirmPasswordRef = useRef();
  const usernameRef = useRef();
  const { currentUser, signup, loading } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  let location = useLocation();
  if (currentUser !== null && !loading) {
    return <Navigate to="/dashboard" state={{ from: location }} replace />;
  }

  const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

  async function handleSubmit(e) {
    e.preventDefault();
    if (!emailRef.current || !emailRef.current.value) {
      createNotification('Success',"Error: email is empty", 'danger');
      
      return;
    }

    if (!validateEmail(emailRef.current.value)) {
      createNotification('Error',"Error: invalid email", 'danger');
      return;
    }

    if (!usernameRef.current || !usernameRef.current.value) {
      createNotification('Error',"Error: username is empty", 'danger');
      return;
    }

    if (!passwordRef.current || !passwordRef.current.value) {
      createNotification('Error',"password is empty", 'danger');
      return;
    }

    if (!confirmPasswordRef.current || !confirmPasswordRef.current.value) {
      createNotification('Error',"Conform password is empty", 'danger');
      return;
    }

    if (passwordRef.current.value.length < 6) {
      createNotification('Error',"Password must have length of at least 6", 'danger');
      return;
    }

    
    if (confirmPasswordRef.current.value !== passwordRef.current.value) {
      createNotification('Error',"Passwords do not match", 'danger');
      return;
    }
    
    let url = "http://localhost:8000/users/?uname=" + usernameRef.current.value;
    fetch(url, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      // mode: "no-cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    }).then((res) => {
      if (res.status === 200) {
        createNotification('Error', 'username already exists', 'danger')
      }
      else {
        res.json().then((data) => {
          try {
            setIsLoading(true);
            console.log(process.env.REACT_APP_FIREBASE_API_KEY);
            signup(
              emailRef.current.value,
              passwordRef.current.value,
              usernameRef.current.value
            );
            console.log("Success!");
          } catch (e) {
            createNotification('Error', 'Failed to create account', 'danger')
            
            console.log(e);
          }
          setIsLoading(false);
        })
      }
      return res.json()
    }).catch((res) => {
      console.log(res);
    })
  }

  return (
    <div className="signup">
      <div className="signup-background"></div>
      <div className="signup">
        <div className="signup-signupform">
          <div className="signup-title">HomeCooked</div>
          <input
            ref={emailRef}
            className="signup-input"
            type="email"
            placeholder="Enter Email Address"
          ></input>
          <input
            ref={usernameRef}
            className="signup-input"
            type="text"
            placeholder="Enter Username"
          ></input>
          <input
            ref={passwordRef}
            className="signup-input"
            type="password"
            placeholder="Enter Password"
          ></input>
          <input
            ref={confirmPasswordRef}
            className="signup-input"
            type="password"
            placeholder="Confirm Password"
          ></input>
          <button
            onClick={(e) => {
              handleSubmit(e);
            }}
            className="signup-button"
            disabled={isLoading}
          >
            Sign Up
          </button>
          <div className="signup-login">
            Already have an account:{" "}
            <Link to="/login" style={{ textDecoration: "none" }}>
              <span className="signup-login-link">Login</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

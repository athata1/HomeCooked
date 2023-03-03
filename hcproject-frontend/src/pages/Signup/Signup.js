import React, { useRef, useState } from "react";
import { Link } from "react-router-dom";
import "./Signup.css";
import { useAuth } from "../../Firebase/AuthContext";
import { useLocation, Navigate } from "react-router-dom";

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
      alert("Error: email is empty");
      return;
    }

    if (!validateEmail(emailRef.current.value)) {
      alert("Error: invalid email");
      return;
    }

    if (!usernameRef.current || !usernameRef.current.value) {
      alert("Error: username is empty");
      return;
    }

    if (!passwordRef.current || !passwordRef.current.value) {
      alert("Error: password is empty");
      return;
    }

    if (!confirmPasswordRef.current || !confirmPasswordRef.current.value) {
      alert("Error: conform password is empty");
      return;
    }

    if (passwordRef.current.value.length < 6) {
      alert("Error: Password must have length of at least 6");
      return;
    }

    
    if (confirmPasswordRef.current.value !== passwordRef.current.value) {
      alert("Error: Passwords do not match");
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
      return res.json()
    }).then((data) => {
      if (data.status == '404') {
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
          alert("Failed to create an account");
          console.log(e);
        }
        setIsLoading(false);
      }
      else {
        alert('Error: username already exists');
        return;
      }
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

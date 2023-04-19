import React, { useEffect, useRef } from "react";
import './Navbar.css'
import ProfileDropdown from '../ProfileDropdown/ProfileDropdown'
import {BsHouseDoor, BsBell} from 'react-icons/bs'
import NavbarDropdown from "../NavbarDropdown/NavbarDropdown";
import { Link } from "react-router-dom";
import {Switch} from "./../Switch/Switch"
import { useAuth } from "../../Firebase/AuthContext";
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

function Navbar({part, mode}) {
  const {searchMode, setSearchMode, searchText, setSearchText} = useAuth();
  const textRef = useRef();
  const dropdown = ["Default", "Zipcode", "City/State", "Profile", "Food"]

  function handleChange(e) {
    if (e.key === 'Enter') {
      if (searchMode === 1) {
        if (e.target.value.match(/^\d{5}$/))
          setSearchText(e.target.value)
        else
          createNotification('Error', 'Invalid zipcode', 'danger')
      }
      else if (searchMode === 2) {
        let arr = e.target.value.split(',');
        if (arr.length !== 2) {
          createNotification('Error', 'Invalid city,state', 'danger');
        }
        else {
          setSearchText(e.target.value)
        }
      }
      else {
        setSearchText(e.target.value)
      }
    }
  }

  useEffect(() => {
    console.log(searchMode)
  }, [searchMode])

  return <div className="navbar">
    <div className="navbarLeft">
      <Link to="/dashboard"><div className="navbarBellContainer">
        <BsHouseDoor size={40} style={{color: "#ffffff"}}/>
      </div>
      </Link>
      <NavbarDropdown part={part}/>
    </div>
    {mode == "consumer" ? 
    
    <div className="navbarMiddle">
      <div className="searchInput">
        <div className="search-dropdown">
          <div>Search By:</div>
          <div className="search-type">
            {dropdown.map((text, i)=> {
              return <div className={i === searchMode ? "search-mode selected" : "search-mode"} onClick={() => {setSearchMode(i)}}>
                {dropdown[i]}
              </div>
            })}
          </div>
        </div>
        <input className="navbar-search" type="text" placeholder={"Find profiles, posts, events..."} onKeyDown={handleChange}/> 
        <div className="searchIcon"> </div>
      </div>
      <div className="searchResult"></div>
    </div>
    
    : ""}
    <div className="navbarRight">
      {mode == "none" ? "" : <Switch mode={mode}/>}
      <div className="navbarBellContainer">
        <Link to="/notifications">
          <BsBell size={40} style={{color: "#ffffff"}}/>
        </Link>
      </div>
      <ProfileDropdown />
    </div>
  </div>;
};

export default Navbar;


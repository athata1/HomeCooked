import React from "react";
import './Navbar.css'
import ProfileDropdown from '../ProfileDropdown/ProfileDropdown'
import {BsHouseDoor} from 'react-icons/bs'
import {Link} from 'react-router-dom'

function Navbar({data}) {
  return <div className="navbar">
    <div className="navbarLeft">
      <Link to="/dashboard">
        <BsHouseDoor size={40} style={{color: "#ffffff"}}/>
      </Link>
    </div>
    <div className="navbarMiddle">
      <div className="searchInput">
        <input className="navbar-search" type="text" placeholder={"Find profiles, posts, events..."} /> 
        <div className="searchIcon"> </div>
      </div>
      <div className="searchResult"></div>
    </div>
    <div className="navbarRight">
      <ProfileDropdown />
    </div>
  </div>;
};

export default Navbar;


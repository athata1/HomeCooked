import React from "react";
import './Navbar.css'
import ProfileDropdown from '../ProfileDropdown/ProfileDropdown'
import {BsHouseDoor, BsBell} from 'react-icons/bs'
import NavbarDropdown from "../NavbarDropdown/NavbarDropdown";
import { Link } from "react-router-dom";
import {Switch} from "./../Switch/Switch"

function Navbar({part, mode}) {
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
        <input className="navbar-search" type="text" placeholder={"Find profiles, posts, events..."} /> 
        <div className="searchIcon"> </div>
      </div>
      <div className="searchResult"></div>
    </div>
    
    : ""}
    <div className="navbarRight">
      {mode == "none" ? "" : <Switch mode={mode}/>}
      <div className="navbarBellContainer">
        <BsBell size={40} style={{color: "#ffffff"}}/>
      </div>
      <ProfileDropdown />
    </div>
  </div>;
};

export default Navbar;


import React from "react";
import './Navbar.css'

function Navbar({data}) {
  return <div className="navbar">
    <div className="navbarLeft">left</div>
    <div className="navbarMiddle">
      <div className="searchInput">
        <input className="navbar-search" type="text" placeholder={"Find profiles, posts, events..."} /> 
        <div className="searchIcon"> </div>
      </div>
      <div className="searchResult"></div>
    </div>
    <div className="navbarRight">right</div>
  </div>;
};

export default Navbar;


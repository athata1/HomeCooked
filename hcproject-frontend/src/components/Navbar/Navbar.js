import React from "react";
import './Navbar.css'
import ProfileDropdown
 from "../ProfileDropdown/ProfileDropdown";
const Navbar = () => {
  return <nav className="navbar">
    <div className="navbar-left">a</div>
    <div className="navbar-middle">
    </div>
    <div className="navbar-right">
      <ProfileDropdown />
    </div>
  </nav>;
};

export default Navbar;

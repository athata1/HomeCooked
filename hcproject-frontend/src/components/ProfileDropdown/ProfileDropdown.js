import React from 'react'
import './ProfileDropdown.css'
import { CgProfile } from 'react-icons/cg'
import {useAuth} from '../../Firebase/AuthContext'
import { useNavigate, Link } from 'react-router-dom'


export default function ProfileDropdown() {

  const {currentUser, signout} = useAuth();
  let navigate = useNavigate();
  const redirect = (path) => {
    navigate(path);
  }


  return (
    <div className='profile-dropdown'>
      <CgProfile size={40} style={{color: "#FFFFFF"}}/>
      <ul className='profile-dropdown-list'>
        <li onClick={() => {redirect("/profile")}} className='profile-dropdown-item'>Profile</li>
        <li onClick={() => {redirect("/settings")}} className='profile-dropdown-item'>Settings</li>
        <li onClick={() => {signout()}} className='profile-dropdown-item'>Logout</li>
      </ul>
    </div>
  )
}

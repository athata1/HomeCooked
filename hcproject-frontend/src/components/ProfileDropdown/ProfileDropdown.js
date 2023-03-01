import React, { useEffect, useState } from 'react'
import './ProfileDropdown.css'
import { CgProfile } from 'react-icons/cg'
import {useAuth} from '../../Firebase/AuthContext'
import { useNavigate, Link } from 'react-router-dom'


export default function ProfileDropdown() {

  const {currentUser, signout, getCurrentPhoto} = useAuth();
  let navigate = useNavigate();
  const redirect = (path) => {
    navigate(path);
  }

  const [photo, setPhoto] = useState(null);

  useEffect(() => {
    getCurrentPhoto().then((link) => {
      if (link.length !== 0) {
        setPhoto(link);
      }
    })
  })

  return (
    <div className='profile-dropdown'>
      {
        photo !== null ?  <img src={photo} style={{width: "40px", height: "40px", borderRadius: "50%", border:"solid 2px white"}}/>
        :       <CgProfile size={40} style={{color: "#FFFFFF"}}/>
      }
      <ul className='profile-dropdown-list'>
        <li onClick={() => {redirect("/profile")}} className='profile-dropdown-item'>Profile</li>
        <li onClick={() => {redirect("/settings")}} className='profile-dropdown-item'>Settings</li>
        <li onClick={() => {signout()}} className='profile-dropdown-item'>Logout</li>
      </ul>
    </div>
  )
}

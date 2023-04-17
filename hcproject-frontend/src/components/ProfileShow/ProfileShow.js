import React, { useEffect, useState } from 'react'
import ProfileCard from './ProfileCard/ProfileCard';
import { useAuth } from '../../Firebase/AuthContext';
import './ProfileShow.css'
export default function ProfileShow() {

  const [profiles, setProfiles] = useState([]);
  const {searchText, searchMode} = useAuth()

  useEffect(() => {
    console.log("HERE")
    let url = "http://localhost:8000/search/items?query=" + searchText + "&filter_users=1";
    console.log(url);
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
      return res.json();
    }).then((data) => {
      console.log(JSON.parse(data.response))
      setProfiles(JSON.parse(data.response))
    })
  }, [searchText,searchMode])

  return (
    <div className='profile-show'>
      <div className='profile-container'>
        {profiles.map((profileData) => {
          return <ProfileCard profile={profileData}/>
        })}
      </div>
    </div>
  )
}

import React, { useEffect, useState } from 'react'
import './ProfileCard.css'
export default function ProfileCard(profile) {

  const [username, setUsername] = useState('');
  const [cityState, setCityState] = useState('');
  const [about, setAbout] = useState('');

  useEffect(() => {
    console.log(profile.profile.fields.user_uname)
    setUsername(profile.profile.fields.user_uname)
    const city = profile.profile.fields.user_city;
    const state = profile.profile.fields.user_state;
    if (city !== '' && state !== '') {
      setCityState(city + ", " + state);
    }
    else {
      setCityState("Unknown");
    }
    setAbout(profile.profile.fields.user_bio)
  }, [profile])

  return (
    <div className='profile-card'>
      <div className='profile-card-username'>
        {username}
      </div>
      <div className='profile-card-city-state'>
        {cityState}
      </div>
      <div className='profile-card-about'>
        {about}
      </div>
    </div>
  )
}

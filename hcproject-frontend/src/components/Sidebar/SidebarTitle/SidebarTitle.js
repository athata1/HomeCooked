import React, { useEffect, useState } from 'react'
import { useAuth } from '../../../Firebase/AuthContext'
import './SidebarTitle.css'
import { useSearchParams } from 'react-router-dom'
import { db } from '../../../Firebase/firebase'
import { doc, getDoc } from 'firebase/firestore'
import { useChatContext } from '../../MessageBoard/ChatProvider/ChatProvider';
import { CgProfile } from 'react-icons/cg'

export default function SidebarTitle() {
  
  const {currentUser, getCurrentPhoto} = useAuth();
  const [photo, setPhoto] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();
  const {setUser} = useChatContext()

  useEffect(() => {
    getCurrentPhoto().then((link) => {
      if (link && link.length !== 0) {
        setPhoto(link);
      }
    })
  }, [])

  return (
    <div className='sidebar-title'>
      {
        photo !== null ?  <img src={photo} style={{width: "40px", height: "40px", borderRadius: "50%", marginLeft: '5px', border:"solid 2px white"}}/>
        :       <CgProfile size={40} style={{color: "#FFFFFF"}}/>
      }
      <div className='sidebar-title-name'>
        {currentUser.displayName}
      </div>
    </div>
  )
}

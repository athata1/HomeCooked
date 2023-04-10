import React, { useEffect } from 'react'
import { useChatContext } from '../ChatProvider/ChatProvider';
import './MessageTitle.css'
export default function MessageTitle() {

  const {user, setUser} = useChatContext();
  useEffect(() => {
    console.log(user)
  }, [user])
  return (
    <div className='message-title'>
      <div className='message-title-name'>
        {user && user[1].userInfo.displayName}
      </div>
    </div>
  )
}

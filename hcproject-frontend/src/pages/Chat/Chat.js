import React, { useEffect } from 'react'
import MessageBoard from '../../components/MessageBoard/MessageBoard';
import Navbar from '../../components/Navbar/Navbar'
import Sidebar from '../../components/Sidebar/Sidebar';
import { useAuth } from '../../Firebase/AuthContext'
import './Chat.css'
export default function Chat() {

  const {currentUser} = useAuth();

  useEffect(() => {
    console.log(currentUser.displayName)
  }, [])

  return (
    <div className="chat">
      <Navbar part="Chat" mode="none" />
      <div className='chat-application mt-4'>
        <div className='chat-app-container'>
          <Sidebar />
          <MessageBoard />
        </div>
      </div>
    </div>
  )
}

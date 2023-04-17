import React, { useEffect } from 'react'
import MessageBoard from '../../components/MessageBoard/MessageBoard';
import Navbar from '../../components/Navbar/Navbar'
import Sidebar from '../../components/Sidebar/Sidebar';
import { useAuth } from '../../Firebase/AuthContext'
import { ChatProvider, useChatContext } from '../../components/MessageBoard/ChatProvider/ChatProvider';
import {useSearchParams} from 'react-router-dom';
import { db } from '../../Firebase/firebase';
import './Chat.css'
import { doc, getDoc } from 'firebase/firestore';
export default function Chat() {

  const {currentUser} = useAuth();

  return (
    <ChatProvider>
      <div className="chat">
        <Navbar part="Chat" mode="none" />
        <div className='chat-application mt-4'>
          <div className='chat-app-container'>
            <Sidebar />
            <MessageBoard />
          </div>
        </div>
      </div>
    </ChatProvider>
  )
}

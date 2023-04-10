import React, { useContext, useRef } from 'react'
import { useAuth } from '../../../Firebase/AuthContext'
import { useChatContext } from '../ChatProvider/ChatProvider'
import { db } from '../../../Firebase/firebase'
import './MessageInput.css'
import { arrayUnion, doc, Timestamp, updateDoc } from 'firebase/firestore'

export default function MessageInput() {

  const {currentUser} = useAuth()
  const {user} = useChatContext()
  const inputRef = useRef();

  async function handleSend() {
    if (inputRef.current.value === '') return;
    const combined = currentUser.uid > user[1].userInfo.uid ? currentUser.uid + user[1].userInfo.uid : user[1].userInfo.uid + currentUser.uid
    await updateDoc(doc(db, 'chats', combined), {
      messages: arrayUnion({
        id: crypto.randomUUID(),
        info: inputRef.current.value,
        type: 'text',
        senderID: currentUser.uid,
        date: Timestamp.now(),
      })
    })
    inputRef.current.value = "";

  }

  return (
    <div className='message-input'>
      <input 
        ref={inputRef} 
        type='text' 
        className='message-input-text'
        disabled={user == null}/>
      <button onClick={() => {handleSend()}}className='message-input-button'>Send</button>
    </div>
  )
}

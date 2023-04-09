import React, { useEffect, useRef, useState } from 'react'
import './MessageContainer.css'
import Message from '../Message/Message'
import MessageInput from '../MessageInput/MessageInput';
import { useChatContext } from '../ChatProvider/ChatProvider';
import { db } from '../../../Firebase/firebase';
import { doc, onSnapshot } from 'firebase/firestore';
import { useAuth } from '../../../Firebase/AuthContext';

export default function MessageContainer() {

  const [responses, setResponses] = useState(["Message","Message"])
  const feedRef = useRef();
  const {user} = useChatContext()
  const {currentUser} = useAuth()

  useEffect(() => {
    if (user === null)
      return;
    const combined = currentUser.uid > user[1].userInfo.uid ? currentUser.uid + user[1].userInfo.uid : user[1].userInfo.uid + currentUser.uid
    const unsub = onSnapshot(doc(db, "chats", combined), (doc) => {
      console.log(doc.data())
      doc.exists() && setResponses(doc.data().messages)
    })

    return () => {unsub()}
  }, [user])

  useEffect(() => {
    feedRef.current.scrollTop = feedRef.current.scrollHeight;
  }, [responses])

  return (
    <div className='message-container'>
      <div ref={feedRef} className='message-container-feed'>
        <div></div>
        <div>
          {responses.map((response) => {
            return <Message message={response}/>
          })}
        </div>
      </div>
      <MessageInput />
    </div>
  )
}

import React, { useEffect, useRef, useState } from 'react'
import './MessageContainer.css'
import Message from '../Message/Message'
import MessageInput from '../MessageInput/MessageInput';

export default function MessageContainer() {

  const [responses, setResponses] = useState(["Message","Message"])
  const feedRef = useRef();

  useEffect(() => {
    feedRef.current.scrollTop = feedRef.current.scrollHeight;
  }, [])

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

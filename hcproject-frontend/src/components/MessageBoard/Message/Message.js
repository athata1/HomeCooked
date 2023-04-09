import React, { useEffect, useState } from 'react'
import { useAuth } from '../../../Firebase/AuthContext'
import { useChatContext } from '../ChatProvider/ChatProvider';
import './Message.css'
export default function Message({message}) {

  const {currentUser} = useAuth();
  const {user} = useChatContext();
  const [text, setText] = useState();
  const [sender, setSender] = useState();
  useEffect(() => {
    setText(message.info)
    setSender(message.senderID);
    console.log(message)
  }, [message])
  return (
    <div className='message'>
      {message.type === 'text' ?
      
      <div className={'message-box ' + (message.senderID === currentUser.uid ? 'right' : 'left')}>
        {text}
      </div>
      
      : ""}
    </div>
  )
}

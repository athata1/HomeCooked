import React, { useEffect } from 'react'
import './Message.css'
export default function Message({message}) {

  return (
    <div className='message'>
      {message}
    </div>
  )
}

import React from 'react'
import './MessageInput.css'

export default function MessageInput() {
  return (
    <div className='message-input'>
      <input type='text' className='message-input-text'/>
      <button className='message-input-button'>Send</button>
    </div>
  )
}

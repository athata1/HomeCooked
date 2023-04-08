import React from 'react'
import './MessageBoard.css'
import MessageContainer from './MessageContainer/MessageContainer'
import MessageTitle from './MessageTitle/MessageTitle'
export default function MessageBoard() {
  return (
    <div className='messageboard'>
      <MessageTitle/>
      <MessageContainer/>
    </div>
  )
}

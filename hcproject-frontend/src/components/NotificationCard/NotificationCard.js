import React, { useEffect, useState } from 'react'
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import './NotificationCard.css'
import { FaCarrot } from 'react-icons/fa'
import { RxEnvelopeOpen } from 'react-icons/rx'

export default function NotificationCard({ response }) {

  const [type, setType] = useState('');
  const [message, setMessage] = useState('');
  const [color, setColor] = useState(['white', 'white']);

  useEffect(() => {
    setType(response.fields.notif_type);
    setMessage(response.fields.notif_message);
    console.log(response.fields.notif_type)
    if (response.fields.notif_type === 'PO') {
      setColor(['lightgreen','green']);
    }
    else if (response.fields.notif_type === 'EV') {
      setColor(['#A7C7E7', '#000080']);
    }
  }, [response])


  return (
    <>
      <div className='notification-card' style={{backgroundColor: color[0]}}>
        <div className='notification-card-icon' style={{backgroundColor: color[1]}}>
          {type === 'PO' ?
            <FaCarrot size={40}/>
          : "" }
          {type === 'EV' ?
            <RxEnvelopeOpen size={40} />
          : "" }
        </div>
        <div className='notification-card-message'>
          {message}
        </div>
      </div>
    </>
  )
}

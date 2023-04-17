import React, { useEffect, useState } from 'react'
import { useAuth } from '../../Firebase/AuthContext';
import Navbar from '../../components/Navbar/Navbar';
import NotificationCard from '../../components/NotificationCard/NotificationCard';
import './Notifications.css'

const Notifications = () => {
    const { userMode, getToken } = useAuth();
    const [response, setResponse] = useState([]);

  useEffect(() => {
    getToken().then((token) => {
      let url = `http://localhost:8000/notifications/get?token=${token}`;
      fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        // mode: "no-cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      }).then((res) => {
        return res.json();
      }).then((data) => {
        let res = JSON.parse(data.data).sort((a,b) => {
          return Date.parse(a.fields.notif_time) - Date.parse(b.fields.notif_time);
        })
        setResponse(res);
      })
    })
  }, [])

  return (
    <>
        <Navbar part="Notifications" mode="none" />
        <div className='notification-container'>
          {response.map((notif) => {
            return <NotificationCard response={notif}/>
          })}
        </div>
    </>
  )
}

export default Notifications
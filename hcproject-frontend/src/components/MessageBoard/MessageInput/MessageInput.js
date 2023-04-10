import React, { useContext, useRef } from 'react'
import { useAuth } from '../../../Firebase/AuthContext'
import { useChatContext } from '../ChatProvider/ChatProvider'
import { db } from '../../../Firebase/firebase'
import './MessageInput.css'
import { arrayUnion, doc, serverTimestamp, Timestamp, updateDoc } from 'firebase/firestore'
import {BiMapAlt} from 'react-icons/bi'

export default function MessageInput() {

  const {currentUser, getToken} = useAuth()
  const {user} = useChatContext()
  const inputRef = useRef();

  function handleDisclose() {
    if (user == null) return;

      getToken().then((token) => {
        let url = "http://localhost:8000/users/?type=Create&fid=" + token;
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
        return res.json()
      }).then(async (data) => {
        let userData = JSON.parse(data.user)[0];
        console.log(userData.fields.user_latitude)
        console.log(userData.fields.user_longitude)

        const text = userData.fields.user_latitude + " " + userData.fields.user_longitude;

        const combined = currentUser.uid > user[1].userInfo.uid ? currentUser.uid + user[1].userInfo.uid : user[1].userInfo.uid + currentUser.uid
        await updateDoc(doc(db, 'chats', combined), {
          messages: arrayUnion({
            id: crypto.randomUUID(),
            info: text,
            type: 'disclose',
            senderID: currentUser.uid,
            date: Timestamp.now(),
          })
        })
        //Create userChats
        await updateDoc(doc(db, 'userChats', currentUser.uid), {
          [combined+".userInfo"]: {
            uid: user[1].userInfo.uid,
            displayName: user[1].userInfo.displayName
          },
          [combined+".date"]: serverTimestamp()
        })
        //Create userChats
        await updateDoc(doc(db, 'userChats', user[1].userInfo.uid), {
          [combined+".userInfo"]: {
            uid: currentUser.uid,
            displayName: currentUser.displayName
          },
          [combined+".date"]: serverTimestamp()
        })

      })
      })
  }

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
    //Create userChats
    await updateDoc(doc(db, 'userChats', currentUser.uid), {
      [combined+".userInfo"]: {
        uid: user[1].userInfo.uid,
        displayName: user[1].userInfo.displayName
      },
      [combined+".date"]: serverTimestamp()
    })
    //Create userChats
    await updateDoc(doc(db, 'userChats', user[1].userInfo.uid), {
      [combined+".userInfo"]: {
        uid: currentUser.uid,
        displayName: currentUser.displayName
      },
      [combined+".date"]: serverTimestamp()
    })

  }

  return (
    <div className='message-input'>
      <input 
        ref={inputRef} 
        type='text' 
        className='message-input-text'
        disabled={user == null}/>
      <button onClick={() => {handleDisclose()}} className='message-disclose-button'>
        {<BiMapAlt size={30}/>}
      </button>
      <button onClick={() => {handleSend()}}className='message-input-button'>Send</button>
    </div>
  )
}

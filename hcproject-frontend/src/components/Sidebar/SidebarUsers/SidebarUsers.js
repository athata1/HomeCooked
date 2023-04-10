import { collection, doc, getDoc, getDocs, onSnapshot, query, serverTimestamp, setDoc, updateDoc, where } from 'firebase/firestore';
import React, { useEffect, useRef, useState } from 'react'
import { useAuth } from '../../../Firebase/AuthContext';
import { db } from '../../../Firebase/firebase';
import { useChatContext } from '../../MessageBoard/ChatProvider/ChatProvider';
import './SidebarUsers.css'
export default function SidebarUsers(selectedUser) {

  const [users, setUsers] = useState([]);
  const {user, setUser} = useChatContext()
  const {currentUser} = useAuth()
  const inputRef = useRef();

  useEffect(() => {
    const subscriber = onSnapshot(doc(db, 'userChats', currentUser.uid), (doc) => {
      let arr = Object.entries(doc.data())
      arr.sort((user1, user2) => {
        return user2[1].date.seconds - user1[1].date.seconds
      })
      setUsers(arr)
    })
    return () => {subscriber()}
  }, [currentUser.uid])

  async function handleSelect(user) {
    //Check if group exists and create new on if it doesn't

    //Create user chat
    try {
      const combined = currentUser.uid > user[1].userInfo.uid ? currentUser.uid + user[1].userInfo.uid : user[1].userInfo.uid + currentUser.uid

      const res = await getDoc(doc(db, 'chats', combined));
      if (!res.exists()) {
        await setDoc(doc(db, 'chats', combined), {
          messages: []
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
      setUser(user)
      inputRef.current.value = '';
    }
    catch (e) {
      console.log(e)
    }
  }

  async function handleChange(e) {
    if (e.code === 'Enter' && inputRef.current.value != '') {
      const userRef = collection(db, 'users');
      const username = inputRef.current.value
      const q = query(userRef, where('displayName', '==', username))
      
      const querySnapshot = await getDocs(q);
      console.log(querySnapshot.docs.length)
      if (querySnapshot.docs.length === 0) {
        alert("Error Could not find user");
        return;
      }
      querySnapshot.forEach((doc) => {
        
        const newUsers = [...users]
        let index = newUsers.findIndex((a) => {
          return a[1].userInfo.displayName === username
        })

        if (index === -1) {
          const data = doc.data();
          const tempData = [-1, {
            userInfo: {
              displayName: data.displayName,
              uid: data.uid
            },
            date: Date()
          }]
          handleSelect(tempData)
        }
      });

    }
  }
  return (
    <div className='sidebar-users'>
      <input
        ref={inputRef} 
        className='sidebar-users-input' 
        type='text'
        placeholder='Find a user'
        onKeyDown={(e) => {handleChange(e)}}
      />
      <div className='sidebar-user-buttons'>
        {users.map((currentUser) => {
          return <div 
              className={'sidebar-user-button ' + (user && user[1].userInfo.displayName == currentUser[1].userInfo.displayName ? "clicked" : "")}
              onClick={() => {handleSelect(currentUser)}}
                >
                  {currentUser[1].userInfo.displayName}
                 </div>
        })}
      </div>
    </div>
  )
}

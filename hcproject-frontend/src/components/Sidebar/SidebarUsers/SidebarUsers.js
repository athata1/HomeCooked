import React from 'react'
import './SidebarUsers.css'
export default function SidebarUsers(selectedUser) {

  //eeefad

  return (
    <div className='sidebar-users'>
      <input 
        className='sidebar-users-input' 
        type='text'
        placeholder='Find a user'
      />
      <div className='sidebar-user-buttons'>
        <div className='sidebar-user-button clicked'>
          John
        </div>
        <div className='sidebar-user-button'>
          Stacy
        </div>
        <div className='sidebar-user-button'>
          Nathanial
        </div>
      </div>
    </div>
  )
}

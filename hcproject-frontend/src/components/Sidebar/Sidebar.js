import React from 'react'
import './Sidebar.css'
import SidebarTitle from './SidebarTitle/SidebarTitle'
import SidebarUsers from './SidebarUsers/SidebarUsers'
export default function Sidebar() {
  return (
    <div className='sidebar'>
      <SidebarTitle/>
      <SidebarUsers/>
    </div>
  )
}

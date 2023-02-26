import React from 'react'
import { Link } from 'react-router-dom'
import './NavbarDropdown.css'

export default function NavbarDropdown({part}) {

  let types = [["Chat", "/chat"],["Events", "/events"], ["Posts", "/dashboard"]]

  return (
    <div className='navbar-page-dropdown'>
      <div className='navbar-page-dropdown-main'>
        {types.find((page) => {return page[0] === part})[0]}
      </div>
      <div className='navbar-page-dropdown-dropdown'>
        {types.filter((page) => {return page[0] !== part}).map((page) => {
            return <Link style={{textDecoration: "none"}}to={page[1]}><div className='navbar-page-dropdown-item'>
              {page[0]}
              </div></Link>
        })}
      </div>
    </div>
  )
}

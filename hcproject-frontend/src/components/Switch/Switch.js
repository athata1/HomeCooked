import React from 'react'
import './Switch.css'
import { useAuth } from '../../Firebase/AuthContext'
export function Switch({mode}) {

  const {setUserMode} = useAuth();

  function handleToggle() {
      if (mode == "consumer") {
        setUserMode("producer")
        return;
      }
      setUserMode("consumer");
  }

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  return (
    <div className="navbar-switch">
      <label class="navbar-switch-container">
        <input onChange={() => {handleToggle()}} checked={mode === "consumer"} className="navbar-switch-toggle"type="checkbox"/>
        <span class="navbar-switch-mode">{capitalizeFirstLetter(mode)}</span>
      </label>
    </div>
  )
}

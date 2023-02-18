import React from "react";
import "./Settings.css";

const Settings = () => {
  return (
    <div className="px-5">
      <h1 className="settings-title">Account</h1>
      <div className="settings-line"></div>
      <form className="settings-form">
        <div className="row">
          <div className="col">
            <input
              type="text"
              className="form-control settings-input"
              placeholder="First name"
            />
          </div>
          <div className="col">
            <input
              type="text"
              className="form-control settings-input"
              placeholder="Last name"
            />
          </div>
        </div>
        <br />
        <div className="row">
          <div className="col">
            <input
              type="text"
              className="form-control settings-input"
              placeholder="Username"
            />
          </div>
          <div className="col">
            <input
              type="text"
              className="form-control settings-input"
              placeholder="Email Address"
            />
          </div>
        </div>
      </form>
    </div>
  );
};

export default Settings;

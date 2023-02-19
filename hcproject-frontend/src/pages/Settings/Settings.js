import React from "react";
import "./Settings.css";
import { CgProfile } from "react-icons/cg";

const Settings = () => {
  return (
    <div className="px-5">
      <div>
        <h1 className="settings-title">Account</h1>
      </div>
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
        <div className="row mt-3">
          <div className="col">
            <h3 className="settings-label">Photo</h3>
          </div>
        </div>
        <div className="row mt-2">
          <div className="col">
            <button className="btn">
              <CgProfile size={80} />
            </button>
            <button className="mx-5 btn settings-button">Change</button>
            <button className="btn btn-danger settings-button-remove">
              Remove
            </button>
          </div>
        </div>
        <div className="row mt-5">
          <div className="col">
            <h3 className="settings-label">About</h3>
          </div>
        </div>
        <div className="row mb-5">
          <div className="col">
            <textarea className="settings-textarea"></textarea>
          </div>
        </div>
        <div className="col mb-3 settings-save-div d-flex justify-content-center">
          <button className="mx-5 btn settings-button settings-save-button">
            Save
          </button>
        </div>
        <div className="col mb-5 settings-save-div d-flex justify-content-center">
          <button className="btn btn-danger settings-button-remove settings-delete-account-button">
            Delete Account
          </button>
        </div>
      </form>
    </div>
  );
};

export default Settings;

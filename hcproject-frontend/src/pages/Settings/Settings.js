import React, { useState } from "react";
import "./Settings.css";
import { CgProfile } from "react-icons/cg";
import { states, stateCities } from "../../utils/stateCity";

const Settings = () => {
  const [selectedState, setSelectedState] = useState("");
  const [selectedImage, setSelectedImage] = useState(null);
  const availableCities = stateCities.getCities(selectedState);

  const handleDeleteAccount = (e) => {
    e.preventDefault();
  };

  const handleRemoveImage = (e) => {
    e.preventDefault();
    setSelectedImage(null);
  };

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
        <div className="row pt-3 pb-5">
          <div className="col pt-2">
            <select
              placeholder="State"
              className="form-select"
              aria-label="Default select example"
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
            >
              <option>--Choose State--</option>
              {states?.map((e, key) => {
                return (
                  <option value={e} key={key}>
                    {e}
                  </option>
                );
              })}
            </select>
          </div>
          <div className="col pt-2">
            <select className="form-select" aria-label="Default select example">
              <option>--Choose City--</option>
              {availableCities?.map((c) => (
                <option value={c} key={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
          <div className="col">
            <input
              type="text"
              className="form-control settings-input "
              placeholder="Zipcode"
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
            <button className="btn" disabled="true">
              <CgProfile size={80} />
            </button>
            <button className="mx-5 btn settings-button">Change</button>
            <button
              className="btn btn-danger settings-button-remove"
              onClick={handleRemoveImage}
            >
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
          <button
            className="btn btn-danger settings-button-remove settings-delete-account-button"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
            onClick={handleDeleteAccount}
          >
            Delete Account
          </button>
          <div
            className="modal fade"
            id="exampleModal"
            tabIndex="-1"
            aria-labelledby="exampleModalLabel"
            aria-hidden="true"
          >
            <div className="modal-dialog">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title" id="exampleModalLabel">
                    Modal title
                  </h5>
                  <button
                    type="button"
                    className="btn-close"
                    data-bs-dismiss="modal"
                    aria-label="Close"
                  ></button>
                </div>
                <div className="modal-body">...</div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button type="button" className="btn btn-primary">
                    Save changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
};

export default Settings;

import React, { useState } from "react";
import "./Settings.css";
import { CgProfile } from "react-icons/cg";
import { AiOutlineEdit } from "react-icons/ai";
import { states, stateCities } from "../../utils/stateCity";
import { useAuth } from "../../Firebase/AuthContext";
import Navbar from "../../components/Navbar/Navbar";
import Alert from "react-bootstrap/Alert";

const Settings = () => {
  const [selectedState, setSelectedState] = useState("--Choose State--");
  const [selectedCity, setSelectedCity] = useState("--Choose City--");
  const [edit, setEdit] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [firstName, setFirstName] = useState("FirstName");
  const [lastName, setLastName] = useState("LastName");
  const [username, setUsername] = useState("Username");
  const [email, setEmail] = useState("Email@email.com");
  const [zipcode, setZipcode] = useState("00000");
  const [about, setAbout] = useState("Aboutajsdlfkasdlkjfaksldjflkasjdlfk");
  const availableCities = stateCities.getCities(selectedState);
  const [validFields, setValidFields] = useState(true);
  const [errorField, setErrorField] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [deleteAccountPassword, setDeleteAccountPassword] = useState("");
  const { deleteUser } = useAuth();

  const handleDeleteAccount = (e) => {
    e.preventDefault();
  };

  const confirmDeleteAccount = async (e) => {
    e.preventDefault();
  };

  const handleRemoveImage = (e) => {
    e.preventDefault();
    setSelectedImage(null);
    e.target.value = null;
  };

  const handleChangeImage = (e) => {
    e.preventDefault();
    setSelectedImage(URL.createObjectURL(e.target.files[0]));
  };

  const handleEdit = () => {
    setEdit(true);
  };

  const handleSave = (e) => {
    e.preventDefault();
    console.log(selectedState);
    setValidFields(true);
    setEdit(false);
    if (!validateEmail(email)) {
      setErrorField("email");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (username.length <= 3 || username.length >= 25) {
      setErrorField("username");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (firstName.length === 0 || firstName.length >= 25) {
      setErrorField("first name.");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (lastName.length === 0 || lastName.length >= 25) {
      setErrorField("last name.");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (zipcode.length !== 5) {
      setErrorField("zipcode");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    if (about.length <= 15) {
      setErrorField("about section");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (selectedState === "--Choose State--") {
      setErrorField("state");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (selectedCity === "--Choose City--") {
      setErrorField("city");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

  return (
    <div>
      <Navbar />
      <div className="px-5">
        <div>
          <h1 className="settings-title pt-3">
            Account{" "}
            {!edit && (
              <AiOutlineEdit
                className="settings-edit ps-3"
                onClick={handleEdit}
              />
            )}
          </h1>
        </div>
        {!validFields && (
          <Alert variant="danger" onClick={() => setValidFields(false)}>
            <Alert.Heading>Please enter a valid {errorField}</Alert.Heading>
          </Alert>
        )}

        <div className="settings-line"></div>
        <form className="settings-form">
          <div className="row">
            <div className="col">
              <input
                type="text"
                className="form-control settings-input"
                placeholder="First name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                readOnly={!edit}
              />
            </div>
            <div className="col">
              <input
                type="text"
                className="form-control settings-input"
                placeholder="Last name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                readOnly={!edit}
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
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                readOnly={!edit}
              />
            </div>
            <div className="col">
              <input
                type="text"
                className="form-control settings-input"
                placeholder="Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                readOnly={!edit}
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
                disabled={!edit}
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
              <select
                className="form-select"
                aria-label="Default select example"
                disabled={!edit}
                onChange={(e) => setSelectedCity(e.target.value)}
              >
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
                type="number"
                className="form-control settings-input"
                placeholder="Zipcode"
                value={zipcode}
                onChange={(e) => setZipcode(e.target.value)}
                readOnly={!edit}
              />
            </div>
          </div>
          <div className="row mt-3">
            <div className="col">
              <h3 className="settings-label mb-4">Change Password</h3>
            </div>
          </div>
          <div className="row">
            <div className="col">
              <input
                type="password"
                className="form-control settings-input"
                placeholder="Old Password"
                value={oldPassword}
                onChange={(e) => setOldPassword(e.target.value)}
                readOnly={!edit}
              />
            </div>
            <div className="col">
              <input
                type="password"
                className="form-control settings-input"
                placeholder="New Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                readOnly={!edit}
              />
            </div>
            <div className="col">
              <input
                type="password"
                className="form-control settings-input"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                readOnly={!edit}
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
              <>
                {selectedImage ? (
                  <img
                    alt="profile-img"
                    src={selectedImage}
                    className="settings-img"
                  />
                ) : (
                  <CgProfile size={80} />
                )}
              </>

              {edit && (
                <input
                  type="file"
                  onChange={handleChangeImage}
                  className="ps-5"
                />
              )}
              {edit && (
                <button
                  className="btn btn-danger settings-button-remove"
                  onClick={handleRemoveImage}
                >
                  Remove
                </button>
              )}
            </div>
          </div>
          <div className="row mt-5">
            <div className="col">
              <h3 className="settings-label">About</h3>
            </div>
          </div>
          <div className="row mb-5">
            <div className="col">
              <textarea
                className="settings-textarea"
                value={about}
                onChange={(e) => setAbout(e.target.value)}
                readOnly={!edit}
              ></textarea>
            </div>
          </div>

          {edit && (
            <div className="col mb-3 settings-save-div d-flex justify-content-center">
              <button
                className="mx-5 btn settings-button settings-save-button"
                onClick={handleSave}
              >
                Save
              </button>
            </div>
          )}

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
                      Are You Sure You Want To Delete Your Account?
                    </h5>
                    <button
                      type="button"
                      className="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Close"
                    ></button>
                  </div>
                  <div className="modal-body">
                    <p>
                      All your data will be deleted. We will not store any
                      credentials, email included. If you want to use the
                      platfrom again you may do so with the same email. However,
                      all the data related to your previous account will be
                      deleted.
                    </p>

                    <input
                      type="password"
                      className="form-control settings-input pt-2"
                      placeholder="Confirm Password"
                      value={deleteAccountPassword}
                      onChange={(e) => setDeleteAccountPassword(e.target.value)}
                      readOnly={!edit}
                    />
                  </div>
                  <div className="modal-footer">
                    <button
                      type="button"
                      className="btn btn-secondary"
                      data-bs-dismiss="modal"
                    >
                      Close
                    </button>
                    <button
                      type="button"
                      className="btn btn-danger"
                      data-bs-dismiss="modal"
                      onClick={confirmDeleteAccount}
                    >
                      Delete Account
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Settings;

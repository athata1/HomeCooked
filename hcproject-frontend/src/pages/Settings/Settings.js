import React, { useEffect, useRef, useState } from "react";
import "./Settings.css";
import { CgProfile } from "react-icons/cg";
import { AiOutlineEdit } from "react-icons/ai";
import { states, stateCities } from "../../utils/stateCity";
import { useAuth } from "../../Firebase/AuthContext";
import Navbar from "../../components/Navbar/Navbar";
import Alert from "react-bootstrap/Alert";
import { ref, uploadBytes } from "firebase/storage";
import { storage } from "../../Firebase/firebase";
import { getDownloadURL } from "firebase/storage";

const Settings = () => {
  const [selectedState, setSelectedState] = useState("--Choose State--");
  const [selectedCity, setSelectedCity] = useState("--Choose City--");
  const [edit, setEdit] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("Email@email.com");
  const [about, setAbout] = useState("Aboutajsdlfkasdlkjfaksldjflkasjdlfk");
  const availableCities = stateCities.getCities(selectedState);
  const [validFields, setValidFields] = useState(true);
  const [errorField, setErrorField] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [deleteAccountPassword, setDeleteAccountPassword] = useState("");
  const [emailChangePassword, setEmailChangePassword] = useState("");
  const [passwordChangeSuccess, setPasswordChangeSuccess] = useState(true);
  const [emailChangeSuccess, setEmailChangeSuccess] = useState(true);
  const [deletedAccount, setDeletedAccount] = useState(true);
  const [prevPhotoSrc, setPrevPhotoSrc] = useState("");
  const {
    deleteUser,
    currentUser,
    changeEmail,
    setCurrentUsername,
    changePassword,
    creating,
    getToken,
    setCurrentPhoto,
    getCurrentPhoto,
  } = useAuth();
  const [uploadedFile, setCurrentUploadedFile] = useState(null);

  useEffect(() => {
    if (currentUser.email !== null) {
      setEmail(currentUser.email);
    }

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
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          let userData = JSON.parse(data.user)[0];
          setUsername(userData.fields.user_uname);
          setSelectedState(userData.fields.user_state.toUpperCase());
          setSelectedCity(userData.fields.user_city.toUpperCase());
          setAbout(userData.fields.user_bio);
        });
    });
    getCurrentPhoto().then((url) => {
      setSelectedImage(url);
      setPrevPhotoSrc(url);
    });
  }, []);

  useEffect(() => {}, [selectedState]);

  useEffect(() => {}, [selectedCity]);

  if (creating) {
    return <h1>Loading...</h1>;
  }

  if (creating || username === "") {
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
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          let userData = JSON.parse(data.user)[0];
          setUsername(userData.fields.user_uname);
          setSelectedState(userData.fields.user_state.toUpperCase());
          setSelectedCity(userData.fields.user_city.toUpperCase());
          setAbout(userData.fields.user_bio);
        });
    });
  }

  const handleDeleteAccount = (e) => {
    e.preventDefault();
  };

  const confirmDeleteAccount = async (e) => {
    e.preventDefault();
    getToken().then((token) => {
      let url = "http://localhost:8000/users/delete?fid=" + token;
      fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        // mode: "no-cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          if (data.status == "200") {
            deleteUser(deleteAccountPassword).then((res) =>
              setDeletedAccount(res)
            );
          } else {
            alert("Error: Could not delete account");
          }
        });
    });
  };

  const handleRemoveImage = (e) => {
    e.preventDefault();
    setSelectedImage(null);
    e.target.value = prevPhotoSrc;
  };

  const handleChangeImage = (e) => {
    e.preventDefault();
    if (
      e.target.files[0].type !== "image/png" &&
      e.target.files[0].type !== "image/jpeg"
    ) {
      return;
    }
    setSelectedImage(URL.createObjectURL(e.target.files[0]));
    setCurrentUploadedFile(e.target.files[0]);
  };

  const handleEdit = () => {
    setEdit(true);
  };

  const handleSave = (e) => {
    e.preventDefault();

    if (validationChecks()) {
      if (oldPassword !== "" && newPassword !== "" && confirmPassword !== "") {
        changePassword(oldPassword, newPassword).then((res) => {
          setPasswordChangeSuccess(res);
        });
      }

      if (emailChangePassword !== "") {
        changeEmail(email, emailChangePassword)
          .then((res) => setEmailChangeSuccess(res))
          .catch((err) => console.log(err));
      }

      getToken().then((token) => {
        let url =
          "http://localhost:8000/users/?type=Change&uname=" +
          username +
          "&fid=" +
          token +
          "&city=" +
          selectedCity +
          "&state=" +
          selectedState +
          "&bio=" +
          about;
        fetch(url, {
          method: "POST", // *GET, POST, PUT, DELETE, etc.
          // mode: "no-cors", // no-cors, *cors, same-origin
          cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
          credentials: "same-origin", // include, *same-origin, omit
          headers: {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
          redirect: "follow", // manual, *follow, error
          referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        })
          .then((res) => {
            return res.json();
          })
          .then((data) => {
            if (data.status === "200") {
              if (uploadedFile !== null) {
                let url = crypto.randomUUID();
                const imageRef = ref(storage, "images/" + url);
                uploadBytes(imageRef, uploadedFile).then((e) => {
                    getDownloadURL(e.ref).then((url) => {
                      setCurrentPhoto(url);
                      return url
                    }).then((link) => {
                      let url =
                      "http://localhost:8000/users/?type=Change&uname=" +
                      "&fid=" +
                      token +
                      "&image=" + link + "&uname=" + username;
                      fetch(url, {
                        method: "POST", // *GET, POST, PUT, DELETE, etc.
                        // mode: "no-cors", // no-cors, *cors, same-origin
                        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
                        credentials: "same-origin", // include, *same-origin, omit
                        headers: {
                          "Content-Type": "application/json",
                          // 'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        redirect: "follow", // manual, *follow, error
                        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
                      })
                    })
                })
              }
            }
          });
      });
    }

    setOldPassword("");
    setNewPassword("");
    setConfirmPassword("");
    setEmailChangePassword("");
  };

  const validationChecks = () => {
    setValidFields(true);
    setEdit(false);
    setDeletedAccount(true);
    if (!validateEmail(email)) {
      setErrorField("email");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return false;
    }
    if (username.length <= 6 || username.length >= 25) {
      setErrorField("username");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return false;
    }

    if (about.length <= 15) {
      setErrorField("about section");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return false;
    }
    if (selectedState === "--Choose State--" || selectedState === "") {
      setErrorField("state");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return false;
    }
    if (selectedCity === "--Choose City--" || selectedCity === "") {
      setErrorField("city");
      setEdit(true);
      setValidFields(false);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return false;
    }
    if (!passwordChangeSuccess) {
      setEdit(true);
      return false;
    }
    return true;
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
      <Navbar part="Settings" mode="none" />
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
          <Alert
            variant="danger"
            onClick={() => setValidFields(true)}
            dismissible
          >
            <Alert.Heading>Please enter a valid {errorField}</Alert.Heading>
          </Alert>
        )}

        <div className="settings-line"></div>
        <form className="settings-form">
          <div className="row mt-3">
            <div className="col">
              <input
                type="text"
                className="form-control settings-input settings-input-username"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                readOnly={!edit}
              />
            </div>
            <div className="col"></div>
          </div>

          <div className="row pt-3 pb-5">
            <div className="col pt-2">
              {edit ? (
                <select
                  placeholder="State"
                  className="form-select"
                  aria-label="Default select example"
                  value={selectedState}
                  onChange={(e) => {
                    setSelectedState(e.target.value);
                  }}
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
              ) : (
                <input
                  type="test"
                  className="form-control settings-input"
                  placeholder="--Choose State--"
                  value={selectedState}
                  readOnly={!edit}
                />
              )}
            </div>
            <div className="col pt-2">
              {edit ? (
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
              ) : (
                <input
                  type="text"
                  className="form-control settings-input"
                  placeholder="--Change City--"
                  value={selectedCity}
                  onChange={(e) => setOldPassword(e.target.value)}
                  readOnly={!edit}
                />
              )}
            </div>
          </div>
          {newPassword !== confirmPassword && (
            <div className="align-items-center">
              <Alert
                variant="danger"
                className="settings-delete-banner"
                onClick={() => setDeletedAccount(true)}
              >
                <Alert.Heading>Passwords Do Not Match</Alert.Heading>
              </Alert>
            </div>
          )}
          {!passwordChangeSuccess && (
            <Alert
              variant="danger"
              onClick={() => setPasswordChangeSuccess(true)}
              dismissible
            >
              <Alert.Heading>Unable to change password</Alert.Heading>
            </Alert>
          )}
          <div className="row">
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
          {!emailChangeSuccess && (
            <Alert
              variant="danger"
              onClick={() => setEmailChangeSuccess(true)}
              dismissible
            >
              <Alert.Heading>Unable to change email</Alert.Heading>
            </Alert>
          )}
          <div className="row mt-3">
            <div className="col">
              <h3 className="settings-label mb-4">Change Email</h3>
            </div>
          </div>
          <div className="row">
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
            <div className="col">
              <input
                type="password"
                className="form-control settings-input"
                placeholder="Current Password"
                value={emailChangePassword}
                onChange={(e) => setEmailChangePassword(e.target.value)}
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
                  onChange={(e) => {
                    handleChangeImage(e);
                  }}
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
          {deletedAccount === false && (
            <div className="align-items-center">
              <Alert
                variant="danger"
                className="settings-delete-banner"
                dismissible
                onClick={() => setDeletedAccount(true)}
              >
                <Alert.Heading>Unable to delete account.</Alert.Heading>
              </Alert>
            </div>
          )}
          {edit && (
            <div className="col mb-3 settings-save-div d-flex justify-content-center">
              <button
                className="mx-5 btn settings-button settings-save-button"
                onClick={handleSave}
                disabled={newPassword !== confirmPassword}
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

import React, { useContext, useEffect, useState } from "react";
import { auth } from "./firebase";
import firebase from "firebase/compat/app";
const AuthContext = React.createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState();
  const [loading, setLoading] = useState(true);
  const [userMode, setUserMode] = useState("consumer");
  const [creating, setCreating] = useState(false);
  async function getToken() {
    let token = await auth.currentUser.getIdToken(false);
    return token;
  }

  async function deleteUser(password) {
    /*const user = auth.currentUser;
    console.log(auth);

    const credentials = firebase.auth.EmailAuthProvider.credential(
      auth.currentUser.email,
      password
    );

    if (credentials === undefined) {
      return false;
    }*/
    try {
      //await user.reauthenticateWithCredential(credentials);
      await auth.signInWithEmailAndPassword(currentUser.email, password);
      await auth.currentUser.delete();
    } catch (e) {
      console.log(e);
      return false;
    }
    return true;
  }

  
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setLoading(true);
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  function signout() {
    auth.signOut().then(() => {
      console.log("Signed out successfully");
    });
  }

  async function login(email, password) {
    await auth.signInWithEmailAndPassword(email, password);
  }

  async function loginWithoutEmail(password) {
    await auth.signInWithEmailAndPassword(auth.currentUser.email, password)
  }

  async function changePassword(oldPassword, newPassword) {
    try {
      await auth
        .signInWithEmailAndPassword(currentUser.email, oldPassword)
        .then((userCred) => {
          userCred.user.updatePassword(newPassword);
        });
    } catch (e) {
      return false;
    }
    return true;
  }

  async function changeEmail(email, password) {
    try {
      await auth
        .signInWithEmailAndPassword(currentUser.email, password)
        .then((userCred) => {
          userCred.user.updateEmail(email);
        });
    } catch (e) {
      return false;
    }
    return true;
  }

  function getUsername() {
    return auth.currentUser.displayName;
  }

  async function setCurrentUsername(username) {
    await auth.currentUser.updateProfile({
      displayName: username,
    });
  }

  async function setCurrentPhoto(link) {
    auth.currentUser.updateProfile({
      photoURL: link
    })
  }

  async function getCurrentPhoto() {
    return auth.currentUser.photoURL
  }

  async function signup(email, password, username) {
    setCreating(true);
    await auth
      .createUserWithEmailAndPassword(email, password)
      .then(async (user) => {
        await auth.currentUser.updateProfile({
          displayName: username,
        });

        await new Promise((r) => setTimeout(r, 1000));

        let token = await user.user.getIdToken(false);

        let url =
          "http://localhost:8000/users/?type=Create&uname=" +
          username +
          "&fid=" +
          token;
        try {
          await fetch(url, {
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
            .then(async (res) => {
              return res.json();
            })
            .then((res) => {
              console.log(res);
            });
        } catch (e) {
          console.log(e);
        }
      }).catch(() => {
        alert("Error: Email already Exists")
      })
    setCreating(false);
  }

  const value = {
    currentUser,
    signup,
    signout,
    login,
    deleteUser,
    getToken,
    userMode,
    setUserMode,
    changeEmail,
    changePassword,
    getUsername,
    setCurrentUsername,
    loading,
    creating,
    setCurrentPhoto,
    getCurrentPhoto,
    loginWithoutEmail
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

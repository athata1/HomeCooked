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
    await auth.signInWithEmailAndPassword(email, password)
  }


  async function updatePassword(oldPassword, newPassword) {
    await auth.signInWithEmailAndPassword(currentUser.email, oldPassword).then((user)=> 
    {
      user.updatePassword(newPassword)
    });
  }

  async function updateEmail(password, email) {
    await auth.signInWithEmailAndPassword(currentUser.email, password).then((user) => {
      user.updateEmail(email);
    })
  }

  async function signup(email, password) {
     await auth.createUserWithEmailAndPassword(email, password).then((user) => {
      console.log(user.getIdToken(true));
     });
  }

  const value = {
    currentUser,
    signup,
    signout,
    login,
    deleteUser,
    getToken,
    userMode,
    setUserMode
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

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

  function login(email, password) {
    return auth.signInWithEmailAndPassword(email, password);
  }

  function signup(email, password) {
    return auth.createUserWithEmailAndPassword(email, password);
  }

  const value = {
    currentUser,
    signup,
    signout,
    login,
    deleteUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

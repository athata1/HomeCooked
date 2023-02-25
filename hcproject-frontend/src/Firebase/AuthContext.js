import React, { useContext, useEffect, useState } from 'react'
import {auth} from "./firebase"

const AuthContext = React.createContext()

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({children}) {

  const [currentUser, setCurrentUser] = useState();
  const [loading, setLoading] = useState(true);

  async function deleteUser(password) {
    const credential = auth.EmailAuthProvider.credential(
      currentUser.email,
      password
    )
  
    const result = await auth.reauthenticateWithCredential(
      auth.currentUser,
      credential
    )
  
    // Pass result.user here
    await deleteUser(result.user)
   
    console.log("success in deleting")
    localStorage.removeItem("user");
  }

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged( user => {
      setLoading(true)
      setCurrentUser(user)
      setLoading(false)
    })

    return unsubscribe
  }, [])

  function signout() {
    auth.signOut().then(() => {
      console.log("Signed out successfully")
    })
  }

  async function login(email, password) {
    await auth.signInWithEmailAndPassword(email, password)
  }

  function signup(email, password) {
    return auth.createUserWithEmailAndPassword(email, password)
  }

  const value = {
    currentUser,
    signup,
    signout,
    login,
    deleteUser
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

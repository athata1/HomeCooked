import React, { useContext, useEffect, useState } from 'react'
import {auth} from "./firebase"

const AuthContext = React.createContext()

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({children}) {

  const [currentUser, setCurrentUser] = useState();
  const [loading, setLoading] = useState(true);

  async function deleteUser() {
    return auth.currentUser.delete()
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

  function login(email, password) {
    return auth.signInWithEmailAndPassword(email, password)
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

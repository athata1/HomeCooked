import React from 'react'
import  {Navigate} from 'react-router-dom'
import { useAuth } from '../../Firebase/AuthContext'
import Login from '../../pages/Login/Login';


export default function PrivateRoute({element}) {
  const {currentUser} = useAuth();
  
  return currentUser ? element : <Navigate to="/login"/>
}

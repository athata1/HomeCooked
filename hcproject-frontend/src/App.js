import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Settings from "./pages/Settings/Settings";
import Login from "./pages/Login/Login";
import Signup from "./pages/Signup/Signup";
import Dashboard from "./pages/Dashboard/Dashboard"
import { AuthProvider } from "./Firebase/AuthContext";
import PrivateRoute from "./components/PrivateRoute/PrivateRoute";
import "./App.css";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={
            <PrivateRoute element={<Dashboard/>}/> } />
          <Route path="/settings" element={
            <PrivateRoute element={<Settings/>}/> } />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;

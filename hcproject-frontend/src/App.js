import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Settings from "./pages/Settings";
import Login from "./pages/Login/Login"
import Signup from "./pages/Signup/Signup";
import Dashboard from "./pages/Dashboard/Dashboard"
import "./App.css";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/settings" element={<Settings />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard/>} />
      </Routes>
    </Router>
  );
}

export default App;
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Settings from "./pages/Settings";
import Login from "./pages/Login/Login"
import Signup from "./pages/Signup/Signup";
<<<<<<< HEAD
=======
import Dashboard from "./pages/Dashboard/Dashboard"
>>>>>>> 3f9cc0f563bb71026c02bb2dfcd04cfbe64a7954
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/settings" element={<Settings />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
<<<<<<< HEAD
=======
        <Route path="/dashboard" element={<Dashboard/>} />
>>>>>>> 3f9cc0f563bb71026c02bb2dfcd04cfbe64a7954
      </Routes>
    </Router>
  );
}

export default App;
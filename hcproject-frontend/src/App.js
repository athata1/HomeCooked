import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Settings from "./pages/Settings";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App;

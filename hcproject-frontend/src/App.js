import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Settings from "./pages/Settings/Settings";
import Login from "./pages/Login/Login";
import Signup from "./pages/Signup/Signup";
import Dashboard from "./pages/Dashboard/Dashboard";
import { AuthProvider } from "./Firebase/AuthContext";
import PrivateRoute from "./components/PrivateRoute/PrivateRoute";
import "./App.css";
import Profile from "./pages/Profile/Profile";
import OtherProfiles from "./pages/OtherProfiles/OtherProfiles";
import ChangePassword from "./pages/ChangePassword/ChangePassword";
import ResetPassword from "./pages/ResetPassword/ResetPassword";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/public/:uname" element={<OtherProfiles/>} />
          <Route
            path="/reset"
            element={<ChangePassword/>}
          />
          <Route path="/change" element={<ResetPassword/>} />
          <Route
            path="/dashboard"
            element={<PrivateRoute element={<Dashboard />} />}
          />
          <Route
            path="/profile"
            element={<PrivateRoute element={<Profile />} />}
          />
          <Route
            path="/settings"
            element={<PrivateRoute element={<Settings />} />}
          />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;

import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import Register from './Register';
import Login from './Login';
import NewProblem from './NewProblem';
import TaskHistory from './TaskHistory';
import Logout from './Logout';
import ErrorBoundary from './ErrorBoundary';
import { AuthContext } from './AuthContext';

function Navigation() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const location = useLocation();

  return (
    <nav>
      <ul>
        {!isAuthenticated && location.pathname !== '/register' && <li><Link to="/register">Register</Link></li>}
        {!isAuthenticated && location.pathname !== '/login' && <li><Link to="/login">Login</Link></li>}
        {isAuthenticated && location.pathname !== '/submit-problem' && <li><Link to="/submit-problem">Submit Problem</Link></li>}
        {isAuthenticated && location.pathname !== '/task-history' && <li><Link to="/task-history">Task History</Link></li>}
        {isAuthenticated && <li><Link to="/logout" onClick={logout}>Logout</Link></li>}
      </ul>
    </nav>
  );
}

function App() {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <Router>
      <ErrorBoundary>
        <div className='App'>
          <Navigation />
          <Routes>
            <Route
              path="/register"
              element={!isAuthenticated ? <Register /> : <Navigate to="/submit-problem" replace />}
            />
            <Route
              path="/login"
              element={!isAuthenticated ? <Login /> : <Navigate to="/submit-problem" replace />}
            />
            <Route
              path="/submit-problem"
              element={isAuthenticated ? <NewProblem /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/task-history"
              element={isAuthenticated ? <TaskHistory /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/"
              element={<Navigate to={isAuthenticated ? "/submit-problem" : "/login"} replace />}
            />
            <Route
              path="*"
              element={<Navigate to="/" replace />}
            />
          </Routes>
        </div>
      </ErrorBoundary>
    </Router>
  );
}

export default App;
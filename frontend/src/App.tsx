import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Layout from './components/Layout';
import AdminRoute from './components/AdminRoute';
import OrganizationManagementPage from './pages/Admin/OrganizationManagementPage';
import { auth } from './services/api';

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser = await auth.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Failed to fetch user data', error);
        auth.logout();
        window.location.reload();
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  return (
    <div>
      <h2>Welcome, {user?.full_name || user?.username}!</h2>
      <p>This is your personalized dashboard. Here you can see an overview of your evaluations, praises, and project activities.</p>
      {/* Add more dashboard widgets here */}
      <div style={{ marginTop: '20px', padding: '15px', border: '1px solid #eee', borderRadius: '8px' }}>
        <h3>Quick Stats</h3>
        <p>Total Praises Received: <strong>5</strong></p>
        <p>Projects Participated: <strong>3</strong></p>
        <p>Upcoming Evaluations: <strong>1</strong></p>
      </div>
    </div>
  );
};

const Profile: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser = await auth.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Failed to fetch user data', error);
        auth.logout();
        window.location.reload();
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) {
    return <p>Loading profile...</p>;
  }

  return (
    <div>
      <h2>User Profile</h2>
      {user ? (
        <div style={{ lineHeight: '1.8' }}>
          <p><strong>Username:</strong> {user.username}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Full Name:</strong> {user.full_name}</p>
          <p><strong>Role:</strong> {user.role}</p>
          <p><strong>Organization:</strong> {user.organization?.name || 'N/A'}</p>
          {/* Add external account integration here */}
          <h3 style={{ marginTop: '20px' }}>External Accounts</h3>
          <p>No external accounts linked yet.</p>
        </div>
      ) : (
        <p>User data not available.</p>
      )}
    </div>
  );
};

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(!!localStorage.getItem('access_token'));

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={isLoggedIn ? <Navigate to="/" /> : <Login onLoginSuccess={handleLoginSuccess} />}
        />
        <Route
          path="/*"
          element={isLoggedIn ? (
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/admin/organizations" element={<AdminRoute><OrganizationManagementPage /></AdminRoute>} />
                {/* Add other routes here */}
              </Routes>
            </Layout>
          ) : (
            <Navigate to="/login" />
          )}
        />
      </Routes>
    </Router>
  );
};

export default App;
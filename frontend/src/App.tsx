import { ThemeProvider, createTheme } from '@mui/material/styles';
import { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import api from './services/api';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import OrganizationManagementPage from './pages/Admin/OrganizationManagementPage';
import ProjectManagementPage from './pages/Admin/ProjectManagementPage';
import AuthorizedRoute from './components/AuthorizedRoute';
import MemberWeightManagementPage from './pages/Admin/MemberWeightManagementPage';
import EvaluationSettingsPage from './pages/Admin/EvaluationSettingsPage';
import MyEvaluationsPage from './pages/MyEvaluationsPage';
import FinalGradeAdjustmentPage from './pages/Admin/FinalGradeAdjustmentPage';
import EvaluationResultPage from './pages/Admin/EvaluationResultPage';
import HistoryPage from './pages/HistoryPage';
import DepartmentEvaluationPage from './pages/Admin/DepartmentEvaluationPage'; // New import
import type { User } from './schemas';
import { UserRole } from './schemas';

const theme = createTheme({
  palette: {
    primary: {
      main: 'rgb(20, 36, 62)',
    },
  },
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [user, setUser] = useState<User | null>(null);

  const checkAuth = useCallback(async () => {
    try {
      const { data: currentUser } = await api.auth.getCurrentUser();
      // Defensive check: Ensure we have a valid user object with an ID
      if (currentUser && currentUser.id) {
        setUser(currentUser);
        setIsAuthenticated(true);
      } else {
        // Treat as unauthenticated if the user object is invalid
        setUser(null);
        setIsAuthenticated(false);
        localStorage.removeItem('access_token');
      }
    } catch (error) {
      setUser(null);
      setIsAuthenticated(false);
      localStorage.removeItem('access_token');
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    setUser(null);
    window.location.href = '/login';
  };

  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Or a proper spinner
  }

  return (
    <ThemeProvider theme={theme}>
      <Router>
        {isAuthenticated && user ? (
          <Layout user={user} onLogout={handleLogout}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/my-evaluations" element={<MyEvaluationsPage />} />
              <Route path="/history" element={<HistoryPage />} />
              
              <Route
                path="/admin/organizations"
                element={
                  <AuthorizedRoute roles={[UserRole.ADMIN]}>
                    <OrganizationManagementPage />
                  </AuthorizedRoute>
                }
              />
              <Route
                path="/admin/projects"
                element={
                  <AuthorizedRoute roles={[UserRole.ADMIN, UserRole.DEPT_HEAD]}>
                    <ProjectManagementPage />
                  </AuthorizedRoute>
                }
              />
              <Route
                path="/admin/member-weights"
                element={
                  <AuthorizedRoute roles={[UserRole.ADMIN, UserRole.DEPT_HEAD]}>
                    <MemberWeightManagementPage />
                  </AuthorizedRoute>
                }
              />
              <Route
                path="/admin/evaluation-settings"
                element={
                  <AuthorizedRoute roles={[UserRole.ADMIN]}>
                    <EvaluationSettingsPage />
                  </AuthorizedRoute>
                }
              />
              <Route
                path="/admin/grade-adjustment"
                element={
                  <AuthorizedRoute roles={[UserRole.ADMIN, UserRole.DEPT_HEAD]}>
                    <FinalGradeAdjustmentPage />
                  </AuthorizedRoute>
                }
              />
              <Route
                path="/admin/evaluation-results"
                element={
                  <AuthorizedRoute roles={[UserRole.ADMIN, UserRole.DEPT_HEAD]}>
                    <EvaluationResultPage />
                  </AuthorizedRoute>
                }
              />
              {/* New Department Evaluation Route */}
              <Route
                path="/admin/department-evaluation"
                element={
                  <AuthorizedRoute roles={[UserRole.ADMIN, UserRole.CENTER_HEAD]}>
                    <DepartmentEvaluationPage />
                  </AuthorizedRoute>
                }
              />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </Layout>
        ) : (
          <Routes>
            <Route path="/login" element={<Login onLoginSuccess={checkAuth} />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        )}
      </Router>
    </ThemeProvider>
  );
}

export default App;

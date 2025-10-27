
import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { auth } from '../services/api';
import { UserRole } from '../schemas/user';

interface AuthorizedRouteProps {
  children: React.ReactElement;
  allowedRoles: UserRole[];
}

const AuthorizedRoute: React.FC<AuthorizedRouteProps> = ({ children, allowedRoles }) => {
  const [isAuthorized, setIsAuthorized] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const user = await auth.getCurrentUser();
        if (user && allowedRoles.includes(user.role)) {
          setIsAuthorized(true);
        } else {
          setIsAuthorized(false);
        }
      } catch (error) {
        console.error('Error fetching user role:', error);
        setIsAuthorized(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, [allowedRoles]);

  if (loading) {
    return <p>Loading...</p>; // Or a spinner component
  }

  return isAuthorized ? children : <Navigate to="/" />;
};

export default AuthorizedRoute;

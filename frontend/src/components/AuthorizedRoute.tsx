
import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import api from '../services/api';
import type { User, UserRole } from '../schemas';

interface AuthorizedRouteProps {
  children: React.ReactElement;
  roles: UserRole[];
}

const AuthorizedRoute: React.FC<AuthorizedRouteProps> = ({ children, roles }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkUser = async () => {
      try {
        const { data } = await api.auth.getCurrentUser();
        setUser(data);
      } catch (error) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    checkUser();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (user && roles.includes(user.role)) {
    return children;
  }

  return <Navigate to="/" />;
};

export default AuthorizedRoute;

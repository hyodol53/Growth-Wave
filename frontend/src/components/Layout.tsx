import React, { useState, useEffect, useCallback } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { auth } from '../services/api';
import type { User } from '../schemas/user'; // Assuming you have a user schema/type defined

import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Button
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AssessmentIcon from '@mui/icons-material/Assessment';
import SummarizeIcon from '@mui/icons-material/Summarize';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import TuneIcon from '@mui/icons-material/Tune';
import AccountTreeIcon from '@mui/icons-material/AccountTree';


import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';

const drawerWidth = 240;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);

  const handleLogout = useCallback(() => {
    auth.logout();
    navigate('/login');
    window.location.reload(); // Force reload to clear state
  }, [navigate]);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser = await auth.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Failed to fetch user', error);
        handleLogout();
      }
    };
    fetchUser();
  }, [handleLogout]);

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'My Profile', icon: <AccountCircleIcon />, path: '/profile' },
    { text: 'My Evaluations', icon: <AssessmentIcon />, path: '/evaluations' },
    { text: 'My History', icon: <SummarizeIcon />, path: '/history' },
  ];

  const managementMenuItems = [
    { text: 'Organization', icon: <AdminPanelSettingsIcon />, path: '/admin/organizations', roles: ['admin'] },
    { text: 'Projects', icon: <BusinessCenterIcon />, path: '/admin/projects', roles: ['admin', 'dept_head'] },
    { text: 'Member Weights', icon: <AccountTreeIcon />, path: '/admin/member-weights', roles: ['admin', 'dept_head'] },
    { text: 'Grade Adjustment', icon: <TuneIcon />, path: '/admin/grade-adjustment', roles: ['admin', 'dept_head'] },
    { text: 'Evaluation Settings', icon: <TuneIcon />, path: '/admin/evaluation-settings', roles: ['admin'] },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Growth-Wave
          </Typography>
          <Typography sx={{ mr: 2 }}>{user?.full_name || user?.username}</Typography>
          <Button color="inherit" onClick={handleLogout}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton component={RouterLink} to={item.path}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
          {(user?.role === 'admin' || user?.role === 'dept_head') && (
            <List>
              <ListItem disablePadding>
                 <Typography sx={{ pl: 2, pt: 1, pb: 1, fontWeight: 'bold', color: 'text.secondary' }}>Management</Typography>
              </ListItem>
              {managementMenuItems.map((item) => (
                item.roles.includes(user.role) && (
                  <ListItem key={item.text} disablePadding>
                    <ListItemButton component={RouterLink} to={item.path}>
                      <ListItemIcon>{item.icon}</ListItemIcon>
                      <ListItemText primary={item.text} />
                    </ListItemButton>
                  </ListItem>
                )
              ))}
            </List>
          )}
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import type { User } from '../schemas/user';

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
import FactCheckIcon from '@mui/icons-material/FactCheck';
import BusinessCenterIcon from '@mui/icons-material/BusinessCenter';
import DomainVerificationIcon from '@mui/icons-material/DomainVerification'; // New import

const drawerWidth = 240;

interface LayoutProps {
  children: React.ReactNode;
  user: User | null;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, user, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  const menuItems = [
    { text: '대시보드', icon: <DashboardIcon />, path: '/' },
    { text: '내 프로필', icon: <AccountCircleIcon />, path: '/profile' },
    { text: '내 평가', icon: <AssessmentIcon />, path: '/my-evaluations' },
    { text: '내 이력', icon: <SummarizeIcon />, path: '/history' },
  ];

  const managementMenuItems = [
    { text: '조직 관리', icon: <AdminPanelSettingsIcon />, path: '/admin/organizations', roles: ['admin'] },
    { text: '프로젝트 관리', icon: <BusinessCenterIcon />, path: '/admin/projects', roles: ['admin', 'dept_head'] },
    { text: '투입률 설정', icon: <AccountTreeIcon />, path: '/admin/member-weights', roles: ['admin', 'dept_head'] },
    { text: '고과 부여', icon: <TuneIcon />, path: '/admin/grade-adjustment', roles: ['admin', 'dept_head'] },
    { text: '평가 설정', icon: <TuneIcon />, path: '/admin/evaluation-settings', roles: ['admin'] },
    { text: '평가 결과 조회', icon: <FactCheckIcon />, path: '/admin/evaluation-results', roles: ['admin', 'dept_head'] },
    { text: '부서 평가', icon: <DomainVerificationIcon />, path: '/admin/department-evaluation', roles: ['admin', 'center_head'] }, // New menu item
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: 'rgb(20, 36, 62)' }}
      >
        <Toolbar>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <img src="/images/logo.png" alt="Growth-Wave Logo" style={{ width: '40px', height: '40px', verticalAlign: 'middle' }} />
            <Box sx={{ display: 'inline-block', verticalAlign: 'middle', marginLeft: '10px' }}>
              <Typography variant="h6" noWrap component="div">
                Growth-Wave
              </Typography>
              <Typography variant="caption" noWrap component="div">
                슈어소트테크 인사평가시스템
              </Typography>
            </Box>
          </Box>
          <Typography sx={{ mr: 2 }}>{user?.full_name || user?.username}</Typography>
          <Button color="inherit" onClick={handleLogout}>로그아웃</Button>
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
          {user?.role !== 'admin' && (
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
          )}
          {(user?.role === 'admin' || user?.role === 'dept_head' || user?.role === 'center_head') && (
            <List>
              <ListItem disablePadding>
                 <Typography sx={{ pl: 2, pt: 1, pb: 1, fontWeight: 'bold', color: 'text.secondary' }}>관리</Typography>
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
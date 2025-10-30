import React from 'react';
import { Typography, Container } from '@mui/material';

const Dashboard: React.FC = () => {
  return (
    <Container>
      <Typography variant="h4" sx={{ mt: 4 }}>
        Dashboard
      </Typography>
      <Typography sx={{ mt: 2 }}>
        Welcome to the Growth-Wave platform.
      </Typography>
    </Container>
  );
};

export default Dashboard;

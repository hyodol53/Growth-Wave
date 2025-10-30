import React from 'react';
import { Typography, Container } from '@mui/material';

const Profile: React.FC = () => {
  return (
    <Container>
      <Typography variant="h4" sx={{ mt: 4 }}>
        Profile Page
      </Typography>
      <Typography sx={{ mt: 2 }}>
        User profile information will be displayed here.
      </Typography>
    </Container>
  );
};

export default Profile;


import React, { useState, useEffect, useCallback } from 'react';
import { Box, Container, Typography, Paper } from '@mui/material';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import type { GridColDef } from '@mui/x-data-grid';
import AccountTreeIcon from '@mui/icons-material/AccountTree';

import { getMySubordinates } from '../../services/api';
import type { User } from '../../schemas/user';
import UserProjectWeightsDialog from '../../components/Admin/UserProjectWeightsDialog';

const MemberWeightManagementPage: React.FC = () => {
  const [subordinates, setSubordinates] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [managingUser, setManagingUser] = useState<User | null>(null);
  const [isWeightsDialogOpen, setIsWeightsDialogOpen] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      // Assuming the API returns the subordinates for the currently logged-in manager
      const subs = await getMySubordinates();
      setSubordinates(subs.data);
    } catch (error) {
      console.error("Failed to fetch subordinates", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleOpenWeightsDialog = (user: User) => {
    setManagingUser(user);
    setIsWeightsDialogOpen(true);
  };

  const handleCloseWeightsDialog = () => {
    setManagingUser(null);
    setIsWeightsDialogOpen(false);
    // Optionally refresh data if weights might affect other views
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'full_name', headerName: 'Name', width: 200 },
    { field: 'email', headerName: 'Email', width: 250 },
    { field: 'role', headerName: 'Role', width: 150 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Manage Weights',
      width: 150,
      getActions: (params) => [
        <GridActionsCellItem 
          icon={<AccountTreeIcon />} 
          label="Manage Project Weights" 
          onClick={() => handleOpenWeightsDialog(params.row as User)} 
        />,
      ],
    },
  ];

  return (
    <Container maxWidth="lg">
      {managingUser && (
        <UserProjectWeightsDialog
          open={isWeightsDialogOpen}
          onClose={handleCloseWeightsDialog}
          user={managingUser}
        />
      )}

      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Member Project Weight Management
        </Typography>
        <Typography variant="body1" gutterBottom>
          Manage the project participation weights for your subordinates. The total weight for each member across all their projects must be 100%.
        </Typography>
        <Paper sx={{ height: 600, width: '100%', mt: 2 }}>
          <DataGrid
            rows={subordinates}
            columns={columns}
            loading={loading}
            initialState={{
              pagination: {
                paginationModel: {
                  pageSize: 10,
                },
              },
            }}
            pageSizeOptions={[10, 20]}
            disableRowSelectionOnClick
          />
        </Paper>
      </Box>
    </Container>
  );
};

export default MemberWeightManagementPage;

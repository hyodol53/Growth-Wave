
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
    { field: 'full_name', headerName: '이름', width: 200 },
    { field: 'email', headerName: '이메일', width: 250 },
    { field: 'role', headerName: '역할', width: 150 },
    {
      field: 'actions',
      type: 'actions',
      headerName: '참여 비중 관리',
      width: 150,
      getActions: (params) => [
        <GridActionsCellItem 
          icon={<AccountTreeIcon />} 
          label="프로젝트 참여 비중 관리" 
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
          멤버 프로젝트 참여 비중 관리
        </Typography>
        <Typography variant="body1" gutterBottom>
          부서원의 프로젝트 참여 비중을 관리합니다. 각 멤버의 모든 프로젝트 참여 비중의 합은 반드시 100%여야 합니다.
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

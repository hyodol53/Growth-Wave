import React, { useState, useEffect, useMemo } from 'react';
import { Box, Typography, Container, Button, Alert, Snackbar } from '@mui/material';
import { DataGrid, GridColDef, GridValueGetterParams, GridCellParams } from '@mui/x-data-grid';
import { getMySubordinates, getEvaluationResultForUser, adjustGrades } from '../services/api';
import { User } from '../schemas/user';
import { ManagerEvaluationView, GradeAdjustment } from '../schemas/evaluation';

interface UserEvaluationData extends User {
  final_score: number | null;
  current_grade: string | null;
}

const FinalGradeAdjustmentPage: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [users, setUsers] = useState<UserEvaluationData[]>([]);
  const [adjustedGrades, setAdjustedGrades] = useState<Record<number, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const subordinatesRes = await getMySubordinates();
        const subordinates = subordinatesRes.data;

        const evaluationDataPromises = subordinates.map(user => 
          getEvaluationResultForUser(user.id).then(res => ({...user, result: res.data}))
        );
        
        const results = await Promise.all(evaluationDataPromises);

        const combinedData: UserEvaluationData[] = results.map(item => ({
          ...item,
          final_score: item.result.final_evaluation?.final_score ?? null,
          current_grade: item.result.final_evaluation?.grade ?? 'N/A',
        }));

        setUsers(combinedData);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleGradeChange = (userId: number, newGrade: string) => {
    setAdjustedGrades(prev => ({ ...prev, [userId]: newGrade }));
  };

  const validationError = useMemo(() => {
    const grades = Object.values(adjustedGrades);
    const bPlusCount = grades.filter(g => g === 'B+').length;
    const bMinusCount = grades.filter(g => g === 'B-').length;
    if (bPlusCount !== bMinusCount) {
      return `The number of B+ grades (${bPlusCount}) must equal the number of B- grades (${bMinusCount}).`;
    }
    return null;
  }, [adjustedGrades]);

  const handleSaveChanges = async () => {
    if (validationError) {
      setError(validationError);
      return;
    }
    setError(null);
    setSuccess(null);

    const adjustments: GradeAdjustment[] = Object.entries(adjustedGrades).map(([userId, grade]) => ({
      user_id: parseInt(userId, 10),
      grade,
    }));

    try {
      await adjustGrades({ adjustments });
      setSuccess('Grades adjusted successfully!');
      setAdjustedGrades({});
      // Optionally re-fetch data here
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save changes.');
      console.error(err);
    }
  };

  const columns: GridColDef[] = [
    { field: 'full_name', headerName: 'Name', width: 180 },
    { field: 'username', headerName: 'Username', width: 150 },
    { 
      field: 'final_score', 
      headerName: 'Final Score', 
      width: 120,
      valueGetter: (params: GridValueGetterParams) => params.row.final_score?.toFixed(2) ?? 'N/A',
    },
    { field: 'current_grade', headerName: 'Current Grade', width: 130 },
    {
      field: 'adjusted_grade',
      headerName: 'Adjusted Grade',
      width: 150,
      editable: true,
      type: 'singleSelect',
      valueOptions: ['S', 'A', 'B+', 'B', 'B-', 'C', 'D'],
      renderCell: (params: GridCellParams) => {
        const value = adjustedGrades[params.id as number] || params.row.current_grade;
        return (
          <select
            value={value}
            onChange={(e) => handleGradeChange(params.id as number, e.target.value)}
            style={{ width: '100%', border: 'none', background: 'transparent' }}
          >
            {['S', 'A', 'B+', 'B', 'B-', 'C', 'D', 'N/A'].map(g => <option key={g} value={g}>{g}</option>)}
          </select>
        );
      },
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Final Grade Adjustment
        </Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <Box sx={{ height: 600, width: '100%', mt: 2 }}>
          <DataGrid
            rows={users}
            columns={columns}
            loading={loading}
            getRowId={(row) => row.id}
          />
        </Box>
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            color="primary"
            disabled={Object.keys(adjustedGrades).length === 0 || !!validationError}
            onClick={handleSaveChanges}
          >
            Save Changes
          </Button>
        </Box>
        {validationError && <Alert severity="warning" sx={{ mt: 2 }}>{validationError}</Alert>}
      </Box>
      <Snackbar open={!!success} autoHideDuration={6000} onClose={() => setSuccess(null)}>
        <Alert onClose={() => setSuccess(null)} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default FinalGradeAdjustmentPage;
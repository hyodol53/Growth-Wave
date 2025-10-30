import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, CircularProgress, Alert, Snackbar, Container } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import type { GridColDef, GridCellParams } from '@mui/x-data-grid';
import api from '../../services/api';
import type { User } from '../../schemas/user';
import type { GradeAdjustment } from '../../schemas/evaluation';

interface RowData extends User {
  final_score: number | null;
  grade: string | null;
}

const FinalGradeAdjustmentPage: React.FC = () => {
  const [rows, setRows] = useState<RowData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [adjustedGrades, setAdjustedGrades] = useState<{ [key: number]: string }>({});
  const [saving, setSaving] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const { data: subordinates } = await api.users.getMySubordinates();
        const evaluationData = await Promise.all(
          subordinates.map(async (user) => {
            try {
              const { data: result } = await api.evaluations.getEvaluationResultForUser(user.id);
              return {
                ...user,
                final_score: result.final_evaluation?.final_score ?? null,
                grade: result.final_evaluation?.grade ?? 'N/A',
              };
            } catch (e) {
              return { ...user, final_score: null, grade: 'N/A' };
            }
          })
        );
        setRows(evaluationData);
      } catch (err) {
        setError('Failed to load data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleGradeChange = (userId: number, newGrade: string) => {
    setAdjustedGrades((prev) => ({ ...prev, [userId]: newGrade }));
  };

  const handleSaveChanges = async () => {
    const adjustments: GradeAdjustment[] = Object.entries(adjustedGrades).map(([userId, grade]) => ({
      user_id: Number(userId),
      adjusted_grade: grade,
    }));

    if (adjustments.length === 0) {
      setValidationError("No changes to save.");
      return;
    }

    // B+/B- validation
    const bPlusCount = adjustments.filter(a => a.adjusted_grade === 'B+').length;
    const bMinusCount = adjustments.filter(a => a.adjusted_grade === 'B-').length;
    if (bPlusCount !== bMinusCount) {
        setValidationError('The number of B+ and B- grades must be equal.');
        return;
    }

    try {
      setSaving(true);
      setValidationError(null);
      await api.evaluations.adjustGrades(adjustments);
      setSuccess('Grades adjusted successfully!');
      setSnackbarOpen(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save changes.');
    } finally {
      setSaving(false);
    }
  };

  const columns: GridColDef[] = [
    { field: 'full_name', headerName: 'Name', flex: 1 },
    { field: 'final_score', headerName: 'Final Score', flex: 1, valueFormatter: (params: any) => params.value?.toFixed(2) ?? '' },
    { field: 'grade', headerName: 'Current Grade', flex: 1 },
    {
      field: 'adjusted_grade',
      headerName: 'Adjusted Grade',
      flex: 1,
      renderCell: (params: GridCellParams) => {
        const currentGrade = adjustedGrades[params.id as number] ?? params.row.grade;
        return (
          <select
            value={currentGrade}
            onChange={(e) => handleGradeChange(params.id as number, e.target.value)}
            style={{ width: '100%' }}
          >
            {['S', 'A', 'B+', 'B', 'B-', 'C', 'D'].map(g => <option key={g} value={g}>{g}</option>)}
          </select>
        );
      },
    },
  ];

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>Final Grade Adjustment</Typography>
      {error && <Alert severity="error">{error}</Alert>}
      {loading ? <CircularProgress /> : (
        <Box sx={{ height: 600, width: '100%' }}>
          <DataGrid
            rows={rows}
            columns={columns}
            getRowId={(row: RowData) => row.id}
          />
        </Box>
      )}
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          onClick={handleSaveChanges}
          disabled={saving || !!validationError}
        >
          {saving ? <CircularProgress size={24} /> : 'Save Changes'}
        </Button>
      </Box>
      {validationError && <Alert severity="warning" sx={{ mt: 2 }}>{validationError}</Alert>}
      <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={() => setSnackbarOpen(false)}>
        <Alert onClose={() => setSnackbarOpen(false)} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default FinalGradeAdjustmentPage;
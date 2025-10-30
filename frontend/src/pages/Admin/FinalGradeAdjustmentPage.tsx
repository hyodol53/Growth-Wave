import React, { useState, useEffect, useMemo } from 'react';
import { Box, Typography, Button, CircularProgress, Alert, Snackbar, Container, FormControl, InputLabel, Select, MenuItem, Paper } from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import type { GridColDef, GridCellParams } from '@mui/x-data-grid';
import AssessmentIcon from '@mui/icons-material/Assessment';
import api from '../../services/api';
import type { User } from '../../schemas/user';
import type { GradeAdjustment, EvaluationPeriod, DepartmentGradeRatio, Organization, DetailedEvaluationResult } from '../../schemas';
import EvaluationDetailDialog from '../../components/Admin/EvaluationDetailDialog';

interface RowData extends User {
  final_score: number | null;
  grade: string | null;
}

const FinalGradeAdjustmentPage: React.FC = () => {
  const [periods, setPeriods] = useState<EvaluationPeriod[]>([]);
  const [selectedPeriod, setSelectedPeriod] = useState<string>('');
  const [rows, setRows] = useState<RowData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [adjustedGrades, setAdjustedGrades] = useState<{ [key: number]: string }>({});
  const [saving, setSaving] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  const [gradeRatios, setGradeRatios] = useState<DepartmentGradeRatio[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [gradeQuotas, setGradeQuotas] = useState<{ S: number; A: number } | null>(null);
  const [departmentGrade, setDepartmentGrade] = useState<string | null>(null);
  const [departmentEvaluations, setDepartmentEvaluations] = useState<DepartmentEvaluation[]>([]);

  const [isDetailOpen, setIsDetailOpen] = useState<boolean>(false);
  const [detailData, setDetailData] = useState<DetailedEvaluationResult | null>(null);
  const [detailLoading, setDetailLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [periodsRes, ratiosRes, orgsRes, userRes] = await Promise.all([
          api.evaluations.getEvaluationPeriods(),
          api.evaluations.getDepartmentGradeRatios(),
          api.organizations.getOrganizations(),
          api.auth.getCurrentUser(),
        ]);

        setPeriods(periodsRes.data);
        setGradeRatios(ratiosRes.data);
        setOrganizations(orgsRes.data);
        setCurrentUser(userRes.data);

        const activePeriod = periodsRes.data.find(p => p.is_active);
        if (activePeriod) {
          setSelectedPeriod(activePeriod.name);
        } else if (periodsRes.data.length > 0) {
          setSelectedPeriod(periodsRes.data[0].name);
        }
      } catch (err) {
        setError('Failed to load initial data.');
      }
    };
    fetchInitialData();
  }, []);

  useEffect(() => {
    const period = periods.find(p => p.name === selectedPeriod);
    if (!period) return;

    const fetchDepartmentEvaluations = async () => {
      try {
        const { data } = await api.evaluations.getDepartmentEvaluations(period.id);
        setDepartmentEvaluations(data);
      } catch (err) {
        setError('Failed to load department evaluations for the selected period.');
        setDepartmentEvaluations([]);
      }
    };

    fetchDepartmentEvaluations();
  }, [selectedPeriod, periods]);

  useEffect(() => {
    const period = periods.find(p => p.name === selectedPeriod);
    if (!period) return; // Guard clause to prevent error if period is not found

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        setValidationError(null);
        setAdjustedGrades({});
        const { data: subordinates } = await api.users.getMySubordinates();
        const evaluationData = await Promise.all(
          subordinates.map(async (user) => {
            try {
              // Using the same API as the detail view to guarantee data consistency
              const { data: result } = await api.evaluations.getDetailedEvaluationResult(period.id, user.id);
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
        setError('Failed to load data for the selected period.');
        setRows([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [selectedPeriod, periods]);

  useEffect(() => {
    if (!currentUser || !currentUser.organization_id || departmentEvaluations.length === 0 || gradeRatios.length === 0 || rows.length === 0) {
      setGradeQuotas(null);
      return;
    }

    const myDeptEvaluation = departmentEvaluations.find(de => de.department_id === currentUser.organization_id);

    if (!myDeptEvaluation || !myDeptEvaluation.grade) {
      setDepartmentGrade(null);
      setGradeQuotas(null);
      return;
    }
    
    const currentDepartmentGrade = myDeptEvaluation.grade;
    setDepartmentGrade(currentDepartmentGrade);

    const ratio = gradeRatios.find(r => r.department_grade === currentDepartmentGrade);
    if (!ratio) {
      setGradeQuotas(null);
      return;
    }

    const totalMembers = rows.length + 1;
    const sQuota = Math.floor(totalMembers * (ratio.s_ratio / 100));
    const aQuota = Math.floor(totalMembers * (ratio.a_ratio / 100));

    setGradeQuotas({ S: sQuota, A: aQuota });

  }, [rows, currentUser, departmentEvaluations, gradeRatios]);

  const currentGradeCounts = useMemo(() => {
    const counts = { S: 0, A: 0, 'B+': 0, 'B-': 0 };
    if (departmentGrade === 'S') {
      counts.S = 1;
    } else if (departmentGrade === 'A') {
      counts.A = 1;
    }

    rows.forEach(row => {
      const grade = adjustedGrades[row.id] || row.grade;
      if (grade === 'S') counts.S++;
      if (grade === 'A') counts.A++;
      if (grade === 'B+') counts['B+']++;
      if (grade === 'B-') counts['B-']++;
    });
    return counts;
  }, [rows, adjustedGrades, departmentGrade]);

  const handlePeriodChange = (event: SelectChangeEvent<string>) => {
    setSelectedPeriod(event.target.value as string);
  };

  const handleGradeChange = (userId: number, newGrade: string) => {
    setAdjustedGrades((prev) => ({ ...prev, [userId]: newGrade }));
  };

  const handleSaveChanges = async () => {
    setValidationError(null);
    if (!selectedPeriod) {
        setValidationError("Please select an evaluation period.");
        return;
    }

    const adjustments: GradeAdjustment[] = Object.entries(adjustedGrades).map(([userId, grade]) => ({
      user_id: Number(userId),
      grade: grade,
    }));

    if (adjustments.length === 0) {
      setValidationError("No changes to save.");
      return;
    }

    if (gradeQuotas && currentGradeCounts.S > gradeQuotas.S) {
      setValidationError(`Number of S grades (${currentGradeCounts.S}) exceeds the quota (${gradeQuotas.S}).`);
      return;
    }
    if (gradeQuotas && currentGradeCounts.A > gradeQuotas.A) {
      setValidationError(`Number of A grades (${currentGradeCounts.A}) exceeds the quota (${gradeQuotas.A}).`);
      return;
    }

    if (currentGradeCounts['B+'] !== currentGradeCounts['B-']) {
        setValidationError('The number of B+ and B- grades must be equal.');
        return;
    }

    try {
      setSaving(true);
      await api.evaluations.adjustGrades(selectedPeriod, adjustments);
      setSuccess('Grades adjusted successfully!');
      setSnackbarOpen(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save changes.');
    } finally {
      setSaving(false);
    }
  };

  const handleViewDetails = async (userId: number) => {
    const period = periods.find(p => p.name === selectedPeriod);
    if (!period) {
      setError("Cannot find selected period details.");
      return;
    }
    try {
      setDetailLoading(true);
      setIsDetailOpen(true);
      const { data } = await api.evaluations.getDetailedEvaluationResult(period.id, userId);
      setDetailData(data);
    } catch (err) {
      setError('Failed to load evaluation details.');
      setIsDetailOpen(false);
    } finally {
      setDetailLoading(false);
    }
  };

  const handleCloseDetail = () => {
    setIsDetailOpen(false);
    setDetailData(null);
  };

  const columns: GridColDef[] = [
    { field: 'full_name', headerName: 'Name', flex: 1.5 },
    {
      field: 'final_score',
      headerName: 'Final Score',
      flex: 1,
      valueFormatter: (params: any) => {
        if (params !== null ) {
          return Number(params).toFixed(2);
        }
        return '';
      },
    },
    { field: 'grade', headerName: 'Current Grade', flex: 1 },
    {
      field: 'adjusted_grade',
      headerName: 'Adjusted Grade',
      flex: 1.5,
      renderCell: (params: GridCellParams) => {
        const currentGrade = adjustedGrades[params.id as number] ?? params.row.grade;
        return (
          <select
            value={currentGrade}
            onChange={(e) => handleGradeChange(params.id as number, e.target.value)}
            style={{ width: '100%' }}
          >
            {['S', 'A', 'B+', 'B', 'B-', 'C', 'D', 'N/A'].map(g => <option key=
{g} value={g}>{g}</option>)}
          </select>
        );
      },
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Details',
      width: 80,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<AssessmentIcon />}
          label="View Details"
          onClick={() => handleViewDetails(params.id as number)}
          disabled={params.row.grade === 'N/A'}
        />,
      ],
    },
  ];

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>고과 부여</Typography>
      
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="period-select-label">Evaluation Period</InputLabel>
        <Select
          labelId="period-select-label"
          value={selectedPeriod}
          label="Evaluation Period"
          onChange={handlePeriodChange}
          disabled={loading || saving}
        >
          {periods.map((p) => (
            <MenuItem key={p.id} value={p.name}>
              {p.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {gradeQuotas && departmentGrade && (
        <Paper elevation={2} sx={{ p: 2, mb: 2, backgroundColor: 'grey.100' }}>
          <Typography variant="h6" gutterBottom>
            부서 등급: {departmentGrade}
          </Typography>
          <Box sx={{ display: 'flex', gap: 4 }}>
            <Typography>
              <b>S등급 TO:</b> {currentGradeCounts.S} / {gradeQuotas.S}
            </Typography>
            <Typography>
              <b>A등급 TO:</b> {currentGradeCounts.A} / {gradeQuotas.A}
            </Typography>
            <Typography>
              <b>B+/B- 현황:</b> B+ ({currentGradeCounts['B+']}), B- ({currentGradeCounts['B-']})
            </Typography>
          </Box>
        </Paper>
      )}

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
          disabled={saving || loading || !selectedPeriod}
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

      {detailData && (
        <EvaluationDetailDialog
          open={isDetailOpen}
          onClose={handleCloseDetail}
          data={detailData}
          loading={detailLoading}
        />
      )}
    </Container>
  );
};

export default FinalGradeAdjustmentPage;
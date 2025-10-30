import React, { useEffect, useState, useCallback } from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Select, MenuItem, Button, Snackbar, Alert, CircularProgress, FormControl, InputLabel } from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import type { Organization } from '../../schemas/organization';
import type { EvaluationPeriod } from '../../schemas/evaluation';
import * as api from '../../services/api';
import { DepartmentGrade, UserRole } from '../../schemas';

// Helper function to find all descendant organizations (remains the same)
const getDescendantOrgIds = (allOrgs: Organization[], parentId: number): number[] => {
    const children = allOrgs.filter(org => org.parent_id === parentId);
    let descendantIds: number[] = children.map(c => c.id);
    children.forEach(child => {
        descendantIds = [...descendantIds, ...getDescendantOrgIds(allOrgs, child.id)];
    });
    return descendantIds;
};

const DepartmentEvaluationPage: React.FC = () => {
  const [evaluationPeriods, setEvaluationPeriods] = useState<EvaluationPeriod[]>([]);
  const [selectedPeriodId, setSelectedPeriodId] = useState<number | ''>('');
  const [departments, setDepartments] = useState<Organization[]>([]);
  const [departmentGrades, setDepartmentGrades] = useState<Record<number, DepartmentGrade | ''>>({});
  const [initialDepartmentGrades, setInitialDepartmentGrades] = useState<Record<number, DepartmentGrade | ''>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({ open: false, message: '', severity: 'success' });

  // Fetch evaluation periods on initial load
  useEffect(() => {
    const fetchPeriods = async () => {
      try {
        const response = await api.evaluations.getEvaluationPeriods();
        const activePeriods = response.data.filter(p => p.is_active);
        setEvaluationPeriods(activePeriods);
        if (activePeriods.length > 0) {
          setSelectedPeriodId(activePeriods[0].id); // Select the first active period by default
        } else {
          setLoading(false);
        }
      } catch (err) {
        setError('평가 기간을 불러오는 데 실패했습니다.');
        setLoading(false);
      }
    };
    fetchPeriods();
  }, []);

  // Fetch departments and their grades when a period is selected
  const fetchDataForPeriod = useCallback(async (periodId: number) => {
    try {
      setLoading(true);
      setError(null);
      
      // Step 1: Fetch essential data (users and organizations)
      const [userResponse, orgsResponse] = await Promise.all([
        api.auth.getCurrentUser(),
        api.organizations.getOrganizations(),
      ]);
      
      const user = userResponse.data;
      const allOrgs = orgsResponse.data;

      // Filter departments user can evaluate
      let filteredOrgs: Organization[] = [];
      if (user.role === UserRole.ADMIN) {
        filteredOrgs = allOrgs.filter(org => org.level === 3); // 팀 단위로 평가
      } else if (user.role === UserRole.CENTER_HEAD && user.organization_id) {
        const descendantIds = getDescendantOrgIds(allOrgs, user.organization_id);
        const descendantOrgs = allOrgs.filter(org => descendantIds.includes(org.id));
        filteredOrgs = descendantOrgs.filter(org => org.level === 3); // 팀 단위로 평가
      }
      setDepartments(filteredOrgs);

      // Step 2: Fetch existing evaluations, handle failure gracefully
      let evaluations = [];
      try {
        const evaluationsResponse = await api.evaluations.getDepartmentEvaluations(periodId);
        evaluations = evaluationsResponse.data;
      } catch (evalError) {
        console.warn(`Could not fetch existing evaluations for period ${periodId}, assuming none exist.`, evalError);
        // Proceed with an empty array if fetching evaluations fails
      }

      // Step 3: Merge the data
      const grades: Record<number, DepartmentGrade | ''> = {};
      evaluations.forEach(ev => {
        grades[ev.department_id] = ev.grade;
      });
      
      filteredOrgs.forEach(dept => {
        if (!grades[dept.id]) {
          grades[dept.id] = '';
        }
      });
      setDepartmentGrades(grades);
      setInitialDepartmentGrades(grades);

    } catch (err) {
      setError('부서 목록을 불러오는 데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (selectedPeriodId) {
      fetchDataForPeriod(selectedPeriodId);
    }
  }, [selectedPeriodId, fetchDataForPeriod]);

  const handleGradeChange = (orgId: number, event: SelectChangeEvent<DepartmentGrade | ''>) => {
    const newGrade = event.target.value as DepartmentGrade | '';
    setDepartmentGrades(prev => ({ ...prev, [orgId]: newGrade }));
  };

  const handleSubmit = async (orgId: number) => {
    const grade = departmentGrades[orgId];
    if (!grade || !selectedPeriodId) {
      setSnackbar({ open: true, message: '평가 기간과 등급을 모두 선택해주세요.', severity: 'error' });
      return;
    }

    try {
      await api.evaluations.upsertDepartmentEvaluation({
        department_id: orgId,
        grade: grade,
        evaluation_period_id: selectedPeriodId,
      });
      setSnackbar({ open: true, message: `부서 등급이 성공적으로 저장되었습니다.`, severity: 'success' });
      // Update the initial state to reflect the successful save
      setInitialDepartmentGrades(prev => ({
        ...prev,
        [orgId]: grade,
      }));
    } catch (err) {
      setSnackbar({ open: true, message: '부서 등급 저장에 실패했습니다.', severity: 'error' });
    }
  };
  
  const handleCloseSnackbar = () => setSnackbar({ ...snackbar, open: false });

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>부서 평가</Typography>
      
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel id="evaluation-period-select-label">평가 기간 선택</InputLabel>
        <Select
          labelId="evaluation-period-select-label"
          value={selectedPeriodId}
          label="평가 기간 선택"
          onChange={(e) => setSelectedPeriodId(e.target.value as number)}
          disabled={evaluationPeriods.length === 0}
        >
          {evaluationPeriods.map((period) => (
            <MenuItem key={period.id} value={period.id}>{period.name}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {loading ? <CircularProgress /> : error ? <Alert severity="error">{error}</Alert> : (
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>부서명</TableCell>
                  <TableCell>평가 등급</TableCell>
                  <TableCell>작업</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {departments.map((dept) => (
                  <TableRow key={dept.id}>
                    <TableCell>{dept.name}</TableCell>
                    <TableCell>
                      <Select
                        value={departmentGrades[dept.id] || ''}
                        onChange={(e) => handleGradeChange(dept.id, e)}
                        displayEmpty
                        size="small"
                        sx={{ minWidth: 120 }}
                      >
                        <MenuItem value="" disabled><em>등급 선택</em></MenuItem>
                        <MenuItem value={DepartmentGrade.S}>S</MenuItem>
                        <MenuItem value={DepartmentGrade.A}>A</MenuItem>
                        <MenuItem value={DepartmentGrade.B}>B</MenuItem>
                      </Select>
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="contained"
                        onClick={() => handleSubmit(dept.id)}
                        disabled={!departmentGrades[dept.id]}
                      >
                        {initialDepartmentGrades[dept.id] ? '수정 제출' : '제출'}
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      <Snackbar open={snackbar.open} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default DepartmentEvaluationPage;
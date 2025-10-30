import React, { useEffect, useState, useCallback } from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Select, MenuItem, Button, Snackbar, Alert, CircularProgress } from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import type { Organization } from '../../schemas/organization';
import * as api from '../../services/api';
import { DepartmentGrade, UserRole } from '../../schemas';

// Helper function to find all descendant organizations
const getDescendantOrgIds = (allOrgs: Organization[], parentId: number): number[] => {
    const children = allOrgs.filter(org => org.parent_id === parentId);
    let descendantIds: number[] = children.map(c => c.id);
    children.forEach(child => {
        descendantIds = [...descendantIds, ...getDescendantOrgIds(allOrgs, child.id)];
    });
    return descendantIds;
};


const DepartmentEvaluationPage: React.FC = () => {
  const [departments, setDepartments] = useState<Organization[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({ open: false, message: '', severity: 'success' });
  const [departmentGrades, setDepartmentGrades] = useState<Record<number, DepartmentGrade | ''>>({});

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      
      // 1. Fetch current user and all organizations in parallel
      const [userResponse, orgsResponse] = await Promise.all([
        api.auth.getCurrentUser(),
        api.organizations.getOrganizations()
      ]);
      
      const user = userResponse.data;
      const allOrgs = orgsResponse.data;

      // 2. Filter organizations based on user role
      let filteredOrgs: Organization[] = [];
      if (user.role === UserRole.ADMIN) {
        // Admin sees all level 3 organizations (Teams)
        filteredOrgs = allOrgs.filter(org => org.level === 3);
      } else if (user.role === UserRole.CENTER_HEAD && user.organization_id) {
        // Center Head sees all level 3 teams within their center
        const descendantIds = getDescendantOrgIds(allOrgs, user.organization_id);
        const descendantOrgs = allOrgs.filter(org => descendantIds.includes(org.id));
        
        filteredOrgs = descendantOrgs.filter(org => org.level === 3);
      }
      
      setDepartments(filteredOrgs);
      
      setDepartments(filteredOrgs);

      // 3. Initialize grades for the filtered departments
      const initialGrades: Record<number, DepartmentGrade | ''> = {};
      filteredOrgs.forEach(dept => {
          initialGrades[dept.id] = dept.department_grade || '';
      });
      setDepartmentGrades(initialGrades);

    } catch (err) {
      setError('데이터를 불러오는 데 실패했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleGradeChange = (orgId: number, event: SelectChangeEvent<DepartmentGrade | ''>) => {
    const newGrade = event.target.value as DepartmentGrade | '';
    setDepartmentGrades(prev => ({
      ...prev,
      [orgId]: newGrade,
    }));
  };

  const handleSubmit = async (orgId: number) => {
    const grade = departmentGrades[orgId];
    if (!grade) {
      setSnackbar({ open: true, message: '등급을 선택해주세요.', severity: 'error' });
      return;
    }

    try {
      await api.organizations.setDepartmentGrade(orgId, grade);
      setSnackbar({ open: true, message: `조직(ID: ${orgId}) 등급이 성공적으로 업데이트되었습니다.`, severity: 'success' });
    } catch (err) {
      setSnackbar({ open: true, message: '조직 등급 업데이트에 실패했습니다.', severity: 'error' });
      console.error(err);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        부서 평가
      </Typography>
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>부서명</TableCell>
                <TableCell>현재 등급</TableCell>
                <TableCell>새 등급 설정</TableCell>
                <TableCell>작업</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {departments.map((dept) => (
                <TableRow key={dept.id}>
                  <TableCell>{dept.name}</TableCell>
                  <TableCell>{dept.department_grade || '미설정'}</TableCell>
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
                      {dept.department_grade ? '수정 제출' : '제출'}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
      <Snackbar open={snackbar.open} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default DepartmentEvaluationPage;
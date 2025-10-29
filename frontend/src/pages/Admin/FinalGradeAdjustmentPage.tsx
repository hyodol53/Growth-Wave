import React, { useState, useEffect, useMemo } from 'react';
import { Box, Typography, Container, Button, Alert, Snackbar } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import type { GridColDef, GridCellParams } from '@mui/x-data-grid';
import { getMySubordinates, getEvaluationResultForUser, adjustGrades } from '../../services/api';
import type { User } from '../../schemas/user';
import type { GradeAdjustment, ManagerEvaluationView } from '../../schemas/evaluation';
import { AxiosError } from 'axios';

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

        const evaluationDataPromises = subordinates.map((user: User) => 
          getEvaluationResultForUser(user.id).then(res => ({...user, result: res.data as ManagerEvaluationView}))
        );
        
        const results = await Promise.all(evaluationDataPromises);

        const combinedData: UserEvaluationData[] = results.map((item: User & { result: ManagerEvaluationView }) => ({
          ...item,
          final_score: item.result.final_evaluation?.final_score ?? null,
          current_grade: item.result.final_evaluation?.grade ?? '없음',
        }));

        setUsers(combinedData);
      } catch (err) {
        if (err instanceof AxiosError) {
          setError(err.response?.data?.detail || '데이터를 불러오는데 실패했습니다.');
        } else {
          setError('예상치 못한 오류가 발생했습니다.');
        }
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
      return `B+ 등급(${bPlusCount}명)과 B- 등급(${bMinusCount}명)의 인원수는 동일해야 합니다.`;
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
      setSuccess('등급이 성공적으로 조정되었습니다!');
      setAdjustedGrades({});
      // Optionally re-fetch data here
    } catch (err) {
      if (err instanceof AxiosError) {
        setError(err.response?.data?.detail || '변경사항 저장에 실패했습니다.');
      } else {
        setError('저장 중 예상치 못한 오류가 발생했습니다.');
      }
      console.error(err);
    }
  };

  const columns: GridColDef[] = [
    { field: 'full_name', headerName: '이름', width: 180 },
    { field: 'username', headerName: '사용자 이름', width: 150 },
    { 
      field: 'final_score', 
      headerName: '최종 점수', 
      width: 120,
      valueGetter: (_value, row) => row.final_score?.toFixed(2) ?? '없음',
    },
    { field: 'current_grade', headerName: '현재 등급', width: 130 },
    {
      field: 'adjusted_grade',
      headerName: '조정 등급',
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
            {['S', 'A', 'B+', 'B', 'B-', 'C', 'D', '없음'].map(g => <option key={g} value={g}>{g}</option>)}
          </select>
        );
      },
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          최종 등급 조정
        </Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <Box sx={{ height: 600, width: '100%', mt: 2 }}>
          <DataGrid
            rows={users}
            columns={columns}
            loading={loading}
            getRowId={(row: UserEvaluationData) => row.id}
          />
        </Box>
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            color="primary"
            disabled={Object.keys(adjustedGrades).length === 0 || !!validationError}
            onClick={handleSaveChanges}
          >
            변경사항 저장
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
import React, { useState, useEffect } from 'react';
import {
  Typography, Container, CircularProgress, Alert, Paper, List, ListItem, ListItemText, Divider, ListItemButton
} from '@mui/material';
import { GridLegacy as Grid } from '@mui/material';
import { getMySubordinates, getEvaluationResultForUser } from '../../services/api';
import type { User } from '../../schemas/user';
import type { ManagerEvaluationView } from '../../schemas/evaluation';
import { AxiosError } from 'axios';

const EvaluationResultPage: React.FC = () => {
  const [subordinates, setSubordinates] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [evaluationData, setEvaluationData] = useState<ManagerEvaluationView | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubordinates = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await getMySubordinates();
        setSubordinates(response.data);
      } catch (err) {
        const errorMessage = err instanceof AxiosError ? err.response?.data?.detail : '하위 직원 목록을 불러오는데 실패했습니다.';
        setError(errorMessage);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchSubordinates();
  }, []);

  useEffect(() => {
    if (!selectedUser) return;

    const fetchEvaluationDetails = async () => {
      setLoadingDetails(true);
      setError(null);
      try {
        const response = await getEvaluationResultForUser(selectedUser.id);
        setEvaluationData(response.data);
      } catch (err) {
        const errorMessage = err instanceof AxiosError ? err.response?.data?.detail : `${selectedUser.full_name}님의 평가 결과를 불러오는데 실패했습니다.`;
        setError(errorMessage);
        setEvaluationData(null); // Clear previous data on error
        console.error(err);
      } finally {
        setLoadingDetails(false);
      }
    };

    fetchEvaluationDetails();
  }, [selectedUser]);

  const handleUserSelect = (user: User) => {
    setSelectedUser(user);
  };

  const renderEvaluationDetails = () => {
    if (loadingDetails) return <CircularProgress />;
    if (!evaluationData) return <Typography>사용자를 선택하여 평가 결과를 확인하세요.</Typography>;

    const { final_evaluation, peer_feedback } = evaluationData;

    return (
      <Paper sx={{ p: 2 }}>
        <Typography variant="h5" gutterBottom>{selectedUser?.full_name}님의 평가 결과</Typography>
        
        <Grid container spacing={2}>
          <Grid xs={12} md={6}>
            <Typography variant="h6" gutterBottom>종합 평가</Typography>
            {final_evaluation ? (
              <>
                <Typography><strong>최종 등급:</strong> {final_evaluation.grade || '미정'}</Typography>
                <Divider sx={{ my: 1 }} />
                <Typography>동료 평가 점수: {final_evaluation.peer_score.toFixed(2)}</Typography>
                <Typography>PM 평가 점수: {final_evaluation.pm_score.toFixed(2)}</Typography>
                <Typography>정성 평가 점수: {final_evaluation.qualitative_score.toFixed(2)}</Typography>
                <Typography sx={{ fontWeight: 'bold' }}>최종 점수: {final_evaluation.final_score.toFixed(2)}</Typography>
              </>
            ) : (
              <Typography>종합 평가 데이터가 없습니다.</Typography>
            )}
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>동료 평가 피드백</Typography>
            <List dense sx={{ maxHeight: 300, overflow: 'auto' }}>
              {peer_feedback.length > 0 ? (
                peer_feedback.map((fb) => (
                  <ListItem key={fb.id}>
                    <ListItemText primary={`- ${fb.feedback}`} />
                  </ListItem>
                ))
              ) : (
                <ListItem><ListItemText primary="작성된 피드백이 없습니다." /></ListItem>
              )}
            </List>
          </Grid>
        </Grid>
      </Paper>
    );
  };

  return (
    <Container maxWidth="xl">
      <Typography variant="h4" component="h1" gutterBottom sx={{ my: 4 }}>
        평가 결과 조회 (관리자/실장)
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Grid container spacing={2}>
        <Grid xs={12} md={4}>
          <Paper sx={{ p: 2, maxHeight: '70vh', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>조회 대상 선택</Typography>
            {loading ? (
              <CircularProgress />
            ) : (
              <List component="nav">
                {subordinates.map((user) => (
                  <ListItemButton key={user.id} selected={selectedUser?.id === user.id} onClick={() => handleUserSelect(user)}>
                    <ListItemText primary={user.full_name} secondary={user.email} />
                  </ListItemButton>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
        <Grid xs={12} md={8}>
          {renderEvaluationDetails()}
        </Grid>
      </Grid>
    </Container>
  );
};

export default EvaluationResultPage;

import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Button, CardActions, CircularProgress, Box } from '@mui/material';
import * as api from '../services/api';
import type { User } from '../schemas/user';
import type { QualitativeEvaluationCreate } from '../schemas/evaluation';
import QualitativeEvaluationDialog from './QualitativeEvaluationDialog';

const QualitativeEvaluationCard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [subordinates, setSubordinates] = useState<User[]>([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  useEffect(() => {
    const fetchSubordinates = async () => {
      try {
        setLoading(true);
        const res = await api.users.getMySubordinates();
        setSubordinates(res.data);
      } catch (error) {
        console.error("Failed to fetch subordinates", error);
        alert('평가 대상자 목록을 불러오는 데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };
    fetchSubordinates();
  }, []);

  const handleOpenDialog = () => {
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
  };

  const handleSubmit = async (data: QualitativeEvaluationCreate) => {
    try {
      await api.evaluations.submitQualitativeEvaluations(data);
      alert('정성평가가 성공적으로 제출되었습니다.');
      handleCloseDialog();
    } catch (error) {
      console.error('Failed to submit qualitative evaluations', error);
      alert('정성평가 제출에 실패했습니다.');
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card>
        <CardContent>
          <Typography variant="h6">정성평가</Typography>
          {subordinates.length > 0 ? (
            <Typography color="text.secondary" sx={{ mt: 1 }}>
              총 {subordinates.length}명의 팀/부서 구성원에 대한 정성평가를 진행합니다.
            </Typography>
          ) : (
            <Typography color="text.secondary" sx={{ mt: 1 }}>
              정성평가를 진행할 대상이 없습니다.
            </Typography>
          )}
        </CardContent>
        <CardActions>
          <Button 
            size="small" 
            variant="contained" 
            onClick={handleOpenDialog}
            disabled={subordinates.length === 0}
          >
            평가하기
          </Button>
        </CardActions>
      </Card>
      <QualitativeEvaluationDialog
        open={isDialogOpen}
        onClose={handleCloseDialog}
        onSubmit={handleSubmit}
        evaluatees={subordinates}
      />
    </>
  );
};

export default QualitativeEvaluationCard;

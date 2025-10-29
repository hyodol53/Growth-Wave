import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Button, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Paper, TextField, Chip
} from '@mui/material';
import type { PeerEvaluationData, PeerEvaluationSubmit } from '../schemas/evaluation';

interface PeerEvaluationGridProps {
  data: PeerEvaluationData;
  onSubmit: (formData: PeerEvaluationSubmit) => void;
}

interface EvaluationEntry {
  evaluatee_id: number;
  evaluatee_name: string;
  score: number | null;
  comment: string | null;
}

const PeerEvaluationGrid: React.FC<PeerEvaluationGridProps> = ({ data, onSubmit }) => {
  const [evaluations, setEvaluations] = useState<EvaluationEntry[]>([]);

  useEffect(() => {
    setEvaluations(data.peers_to_evaluate);
  }, [data]);

  const handleScoreChange = (evaluatee_id: number, score: string) => {
    const newScore = score === '' ? null : Number(score);
    if (newScore !== null && (isNaN(newScore) || newScore < 0 || newScore > 100)) return;

    setEvaluations(prev =>
      prev.map(e => (e.evaluatee_id === evaluatee_id ? { ...e, score: newScore } : e))
    );
  };

  const handleCommentChange = (evaluatee_id: number, comment: string) => {
    setEvaluations(prev =>
      prev.map(e => (e.evaluatee_id === evaluatee_id ? { ...e, comment: comment } : e))
    );
  };

  const handleSubmit = () => {
    const isAllScored = evaluations.every(e => e.score !== null);
    if (!isAllScored) {
      alert('모든 동료의 점수를 입력해주세요.');
      return;
    }

    const payload: PeerEvaluationSubmit = {
      evaluations: evaluations.map(e => ({
        project_id: data.project_id,
        evaluatee_id: e.evaluatee_id,
        score: e.score!,
        comment: e.comment || undefined,
      })),
    };
    onSubmit(payload);
  };

  const getStatusChip = () => {
    switch (data.status) {
      case 'COMPLETED':
        return <Chip label="평가 완료" color="success" />;
      case 'IN_PROGRESS':
        return <Chip label="평가 진행중" color="warning" />;
      case 'NOT_STARTED':
        return <Chip label="평가 시작 전" color="default" />;
      default:
        return null;
    }
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">동료평가: {data.project_name}</Typography>
        {getStatusChip()}
      </Box>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>이름</TableCell>
              <TableCell align="right" sx={{width: '100px'}}>점수 (0-100)</TableCell>
              <TableCell>코멘트</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {evaluations.map((row) => (
              <TableRow key={row.evaluatee_id}>
                <TableCell component="th" scope="row">
                  {row.evaluatee_name}
                </TableCell>
                <TableCell align="right">
                  <TextField
                    type="number"
                    size="small"
                    value={row.score ?? ''}
                    onChange={(e) => handleScoreChange(row.evaluatee_id, e.target.value)}
                    inputProps={{ min: 0, max: 100 }}
                  />
                </TableCell>
                <TableCell>
                  <TextField
                    fullWidth
                    multiline
                    size="small"
                    value={row.comment ?? ''}
                    onChange={(e) => handleCommentChange(row.evaluatee_id, e.target.value)}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <Button variant="contained" onClick={handleSubmit}>
          {data.status === 'NOT_STARTED' ? '동료평가 제출' : '동료평가 수정 제출'}
        </Button>
      </Box>
    </Paper>
  );
};

export default PeerEvaluationGrid;

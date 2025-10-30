import React, { useState, useEffect, useMemo } from 'react';
import {
  Box, Typography, Button, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Paper, TextField, Chip, Tooltip
} from '@mui/material';
import type { PeerEvaluationData, PeerEvaluationSubmit } from '../schemas/evaluation';

interface PeerEvaluationGridProps {
  data: PeerEvaluationData;
  onSubmit: (formData: PeerEvaluationSubmit) => void;
}

interface EvaluationEntry {
  evaluatee_id: number;
  evaluatee_name: string;
  scores: (number | null)[];
  comment: string | null;
}

const evaluationCriteria = [
    { name: '업무 기한 완수', maxScore: 20, description: '본인이 맡은 업무를 기한 내 완수하였는가?' },
    { name: '업무 정확성', maxScore: 20, description: '담당 업무를 정확하고 오류 없이 처리 하였는가?' },
    { name: '프로젝트 이해도', maxScore: 10, description: '프로젝트에 대하여 충분히 이해하고 적합하게 업무를 처리하는가?' },
    { name: '의사소통', maxScore: 10, description: '상대방의 의견을 경청하며, 자신의 생각을 효과적으로 전달하는가?' },
    { name: '문제 해결 능력', maxScore: 10, description: '문제 해결을 위해 새롭거나 기발한 방식의 해결 방안을 제시하는가?' },
    { name: '윤리성', maxScore: 10, description: '기본 윤리와 원칙에 따르며, 부당한 행동을 하지 않는가?' },
    { name: '팀 기여도', maxScore: 20, description: '팀의 공동목표를 달성하기 위해 팀의 방향을 설정하고 구성원들을 동기부여/독려하는가?' },
];

const PeerEvaluationGrid: React.FC<PeerEvaluationGridProps> = ({ data, onSubmit }) => {
  const [evaluations, setEvaluations] = useState<EvaluationEntry[]>([]);

  useEffect(() => {
    setEvaluations(
      data.peers_to_evaluate.map(peer => ({
        ...peer,
        scores: peer.scores && peer.scores.length > 0 ? peer.scores : Array(evaluationCriteria.length).fill(null),
      }))
    );
  }, [data]);

  const handleScoreChange = (evaluatee_id: number, criterionIndex: number, score: string) => {
    const newScore = score === '' ? null : Number(score);
    const maxScore = evaluationCriteria[criterionIndex].maxScore;
    if (newScore !== null && (isNaN(newScore) || newScore < 0 || newScore > maxScore)) return;

    setEvaluations(prev =>
      prev.map(e =>
        e.evaluatee_id === evaluatee_id
          ? {
              ...e,
              scores: e.scores.map((s, i) => (i === criterionIndex ? newScore : s)),
            }
          : e
      )
    );
  };

  const handleCommentChange = (evaluatee_id: number, comment: string) => {
    setEvaluations(prev =>
      prev.map(e => (e.evaluatee_id === evaluatee_id ? { ...e, comment: comment } : e))
    );
  };

  const handleSubmit = () => {
    const isAllScored = evaluations.every(e => e.scores.every(s => s !== null));
    if (!isAllScored) {
      alert('모든 동료의 모든 항목 점수를 입력해주세요.');
      return;
    }

    const payload: PeerEvaluationSubmit = {
      evaluations: evaluations.map(e => ({
        project_id: data.project_id,
        evaluatee_id: e.evaluatee_id,
        scores: e.scores.map(s => s!),
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

  const calculateTotalScore = (scores: (number | null)[]) => {
    return scores.reduce((acc: number, score) => acc + (score || 0), 0);
  };

  const { averageScore, isSubmittable } = useMemo(() => {
    const totalScores = evaluations.map(e => calculateTotalScore(e.scores));
    const isAllScored = evaluations.every(e => e.scores.every(s => s !== null));
    const average = totalScores.length > 0 ? totalScores.reduce((a, b) => a + b, 0) / totalScores.length : 0;
    const isSubmittable = isAllScored && average <= 70;
    return { averageScore: average, isSubmittable };
  }, [evaluations]);


  return (
    <Paper sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">동료평가: {data.project_name}</Typography>
        {getStatusChip()}
      </Box>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>이름</TableCell>
              {evaluationCriteria.map((criterion, index) => (
                <TableCell key={index} align="right" sx={{minWidth: '120px'}}>
                    <Tooltip title={criterion.description} placement="top">
                        <Typography variant="subtitle2">{criterion.name} ({criterion.maxScore}점)</Typography>
                    </Tooltip>
                </TableCell>
              ))}
              <TableCell align="right">합계</TableCell>
              <TableCell>코멘트</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {evaluations.map((row) => (
              <TableRow key={row.evaluatee_id}>
                <TableCell component="th" scope="row">
                  {row.evaluatee_name}
                </TableCell>
                {row.scores.map((score, index) => (
                  <TableCell key={index} align="right">
                    <TextField
                      type="number"
                      size="small"
                      value={score ?? ''}
                      onChange={(e) => handleScoreChange(row.evaluatee_id, index, e.target.value)}
                      inputProps={{ min: 0, max: evaluationCriteria[index].maxScore, style: { textAlign: 'right' } }}
                      sx={{width: '80px'}}
                    />
                  </TableCell>
                ))}
                <TableCell align="right">
                  <Typography variant="body2">{calculateTotalScore(row.scores)}</Typography>
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
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
        <Typography 
            variant="body1"
            sx={{
                mr: 2,
                color: averageScore > 70 ? 'red' : 'green',
                fontWeight: 'bold'
            }}
        >
            동료평가 평균: {averageScore.toFixed(2)} / 70
        </Typography>
        <Button variant="contained" onClick={handleSubmit} disabled={!isSubmittable}>
          {data.status === 'NOT_STARTED' ? '동료평가 제출' : '동료평가 수정 제출'}
        </Button>
      </Box>
    </Paper>
  );
};

export default PeerEvaluationGrid;

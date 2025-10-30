import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  Button,
  Chip
} from '@mui/material';
import type { QualitativeEvaluationData, QualitativeEvaluationCreate } from '../schemas/evaluation';

interface QualitativeEvaluationGridProps {
  data: QualitativeEvaluationData;
  onSubmit: (formData: QualitativeEvaluationCreate) => void;
}

const QualitativeEvaluationGrid: React.FC<QualitativeEvaluationGridProps> = ({ data, onSubmit }) => {
  const [evaluations, setEvaluations] = useState<Record<number, {
    qualitative_score: number;
    department_contribution_score: number;
    feedback: string;
  }>>({});

  useEffect(() => {
    const initialEvals: typeof evaluations = {};
    data.members_to_evaluate.forEach(member => {
      initialEvals[member.evaluatee_id] = {
        qualitative_score: member.qualitative_score ?? 0,
        department_contribution_score: member.department_contribution_score ?? 0,
        feedback: member.feedback ?? ''
      };
    });
    setEvaluations(initialEvals);
  }, [data]);

  const handleInputChange = (
    userId: number,
    field: 'qualitative_score' | 'department_contribution_score' | 'feedback',
    value: string | number
  ) => {
    let processedValue = value;
    if (typeof value === 'number') {
        if (field === 'qualitative_score') {
            processedValue = Math.max(0, Math.min(20, value));
        } else if (field === 'department_contribution_score') {
            processedValue = Math.max(0, Math.min(10, value));
        }
    }

    setEvaluations(prev => ({
      ...prev,
      [userId]: {
        ...prev[userId],
        [field]: processedValue
      }
    }));
  };

  const handleSubmit = () => {
    const formData: QualitativeEvaluationCreate = {
      evaluations: Object.entries(evaluations).map(([evaluatee_id, evalData]) => ({
        evaluatee_id: Number(evaluatee_id),
        ...evalData
      }))
    };
    onSubmit(formData);
  };

  const getStatusChip = (status: 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED') => {
    if (status === 'COMPLETED') {
      return <Chip label="평가 완료" color="success" />;
    }
    if (status === 'IN_PROGRESS') {
      return <Chip label="평가 진행중" color="warning" />;
    }
    return <Chip label="평가 미시작" color="default" />;
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">평가 대상 목록</Typography>
        {getStatusChip(data.status)}
      </Box>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>이름</TableCell>
              <TableCell>직책</TableCell>
              <TableCell>소속</TableCell>
              <TableCell align="right" sx={{minWidth: 150}}>정성평가 (20점)</TableCell>
              <TableCell align="right" sx={{minWidth: 150}}>부서기여도 (10점)</TableCell>
              <TableCell sx={{minWidth: 300}}>피드백</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.members_to_evaluate.map((member) => (
              <TableRow key={member.evaluatee_id}>
                <TableCell>{member.evaluatee_name}</TableCell>
                <TableCell>{member.title}</TableCell>
                <TableCell>{member.organization_name}</TableCell>
                <TableCell align="right">
                  <TextField
                    type="number"
                    size="small"
                    variant="outlined"
                    value={evaluations[member.evaluatee_id]?.qualitative_score ?? ''}
                    onChange={(e) => handleInputChange(member.evaluatee_id, 'qualitative_score', parseInt(e.target.value, 10) || 0)}
                    inputProps={{ min: 0, max: 20, style: { textAlign: 'right' } }}
                  />
                </TableCell>
                <TableCell align="right">
                  <TextField
                    type="number"
                    size="small"
                    variant="outlined"
                    value={evaluations[member.evaluatee_id]?.department_contribution_score ?? ''}
                    onChange={(e) => handleInputChange(member.evaluatee_id, 'department_contribution_score', parseInt(e.target.value, 10) || 0)}
                    inputProps={{ min: 0, max: 10, style: { textAlign: 'right' } }}
                  />
                </TableCell>
                <TableCell>
                  <TextField
                    fullWidth
                    multiline
                    size="small"
                    variant="outlined"
                    value={evaluations[member.evaluatee_id]?.feedback ?? ''}
                    onChange={(e) => handleInputChange(member.evaluatee_id, 'feedback', e.target.value)}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <Button variant="contained" onClick={handleSubmit}>
          {data.status === 'NOT_STARTED' ? '정성평가 제출' : '정성평가 수정 제출'}
        </Button>
      </Box>
    </Box>
  );
};

export default QualitativeEvaluationGrid;

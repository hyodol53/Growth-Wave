import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, List, ListItem, ListItemText, Typography, Box } from '@mui/material';
import type { User } from '../schemas/user';
import type { QualitativeEvaluationCreate } from '../schemas/evaluation';

interface EvaluationInput {
  qualitative_score: number;
  department_contribution_score: number;
  feedback: string;
}

interface QualitativeEvaluationDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: QualitativeEvaluationCreate) => void;
  evaluatees: User[];
}

const QualitativeEvaluationDialog: React.FC<QualitativeEvaluationDialogProps> = ({ open, onClose, onSubmit, evaluatees }) => {
  const [evaluations, setEvaluations] = useState<Record<number, EvaluationInput>>({});

  useEffect(() => {
    if (open) {
      const initialEvaluations: Record<number, EvaluationInput> = {};
      evaluatees.forEach(e => {
        initialEvaluations[e.id] = {
          qualitative_score: 0,
          department_contribution_score: 0,
          feedback: '',
        };
      });
      setEvaluations(initialEvaluations);
    }
  }, [open, evaluatees]);

  const handleInputChange = (userId: number, field: keyof EvaluationInput, value: string | number) => {
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
        [field]: processedValue,
      },
    }));
  };

  const handleSubmit = () => {
    const evaluationData: QualitativeEvaluationCreate = {
      evaluations: Object.entries(evaluations).map(([evaluatee_id, data]) => ({
        evaluatee_id: Number(evaluatee_id),
        qualitative_score: data.qualitative_score,
        department_contribution_score: data.department_contribution_score,
        feedback: data.feedback,
      }))
    };
    onSubmit(evaluationData);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle>정성평가 진행</DialogTitle>
      <DialogContent>
        <Typography sx={{ mt: 2, mb: 1 }}>아래 팀원/부서원의 정성평가를 입력해주세요.</Typography>
        <List>
          {evaluatees.map(evaluatee => (
            <ListItem key={evaluatee.id} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
              <ListItemText primary={evaluatee.full_name || evaluatee.username} />
              <Box sx={{ display: 'flex', flexDirection: 'row', gap: 2, width: '100%', mt: 1 }}>
                <TextField
                  label="정성평가 (20점 만점)"
                  type="number"
                  size="small"
                  variant="outlined"
                  value={evaluations[evaluatee.id]?.qualitative_score || 0}
                  onChange={(e) => handleInputChange(evaluatee.id, 'qualitative_score', parseInt(e.target.value, 10) || 0)}
                  inputProps={{ min: 0, max: 20 }}
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="부서기여도 (10점 만점)"
                  type="number"
                  size="small"
                  variant="outlined"
                  value={evaluations[evaluatee.id]?.department_contribution_score || 0}
                  onChange={(e) => handleInputChange(evaluatee.id, 'department_contribution_score', parseInt(e.target.value, 10) || 0)}
                  inputProps={{ min: 0, max: 10 }}
                  sx={{ flex: 1 }}
                />
              </Box>
              <TextField
                label="피드백"
                multiline
                rows={2}
                fullWidth
                variant="outlined"
                value={evaluations[evaluatee.id]?.feedback || ''}
                onChange={(e) => handleInputChange(evaluatee.id, 'feedback', e.target.value)}
                sx={{ mt: 2 }}
              />
            </ListItem>
          ))}
        </List>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">Submit</Button>
      </DialogActions>
    </Dialog>
  );
};

export default QualitativeEvaluationDialog;

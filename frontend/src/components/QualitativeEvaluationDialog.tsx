
import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, List, ListItem, ListItemText, Typography } from '@mui/material';
import type { User } from '../schemas/user';
import type { QualitativeEvaluationCreate } from '../schemas/evaluation';

interface QualitativeEvaluationDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: QualitativeEvaluationCreate) => void;
  evaluatees: User[];
}

const QualitativeEvaluationDialog: React.FC<QualitativeEvaluationDialogProps> = ({ open, onClose, onSubmit, evaluatees }) => {
  const [scores, setScores] = useState<Record<number, number>>({});

  useEffect(() => {
    // Reset scores when dialog opens or evaluatees change
    const initialScores: Record<number, number> = {};
    evaluatees.forEach(e => {
      initialScores[e.id] = 0;
    });
    setScores(initialScores);
  }, [open, evaluatees]);

  const handleScoreChange = (userId: number, score: number) => {
    const newScore = Math.max(0, Math.min(100, score)); // Clamp score between 0 and 100
    setScores(prev => ({ ...prev, [userId]: newScore }));
  };

  const handleSubmit = () => {
    const evaluationData: QualitativeEvaluationCreate = {
      evaluations: Object.entries(scores).map(([evaluatee_id, score]) => ({
        evaluatee_id: Number(evaluatee_id),
        score: score,
      }))
    };
    onSubmit(evaluationData);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>정성평가 진행</DialogTitle>
      <DialogContent>
        <Typography sx={{mt: 2, mb: 1}}>아래 팀원/부서원의 정성평가 점수를 입력해주세요. (0-100점)</Typography>
        <List>
          {evaluatees.map(evaluatee => (
            <ListItem key={evaluatee.id}>
              <ListItemText primary={evaluatee.full_name || evaluatee.username} />
              <TextField
                type="number"
                size="small"
                variant="outlined"
                value={scores[evaluatee.id] || 0}
                onChange={(e) => handleScoreChange(evaluatee.id, parseInt(e.target.value, 10) || 0)}
                inputProps={{ min: 0, max: 100, style: { textAlign: 'right' } }}
                sx={{width: '100px'}}
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

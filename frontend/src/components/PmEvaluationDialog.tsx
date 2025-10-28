
import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, List, ListItem, ListItemText, Typography } from '@mui/material';
import type { PmEvaluationCreate } from '../schemas/evaluation';

// This is a mock schema for project members based on the API spec we defined
interface ProjectMember {
    user_id: number;
    full_name: string;
    is_pm: boolean;
    participation_weight: number;
}

interface PmEvaluationDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: PmEvaluationCreate) => void;
  evaluatees: ProjectMember[];
  project: { id: number; name: string }; // Simplified project type for the dialog
}

const PmEvaluationDialog: React.FC<PmEvaluationDialogProps> = ({ open, onClose, onSubmit, evaluatees, project }) => {
  const [scores, setScores] = useState<Record<number, number>>({});

  useEffect(() => {
    const initialScores: Record<number, number> = {};
    evaluatees.forEach(e => {
      initialScores[e.user_id] = 0;
    });
    setScores(initialScores);
  }, [open, evaluatees]);

  const handleScoreChange = (userId: number, score: number) => {
    const newScore = Math.max(0, Math.min(100, score));
    setScores(prev => ({ ...prev, [userId]: newScore }));
  };

  const handleSubmit = () => {
    const evaluationData: PmEvaluationCreate = {
      evaluations: Object.entries(scores).map(([evaluatee_id, score]) => ({
        project_id: project.id,
        evaluatee_id: Number(evaluatee_id),
        score: score,
      }))
    };
    onSubmit(evaluationData);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>PM 평가: {project.name}</DialogTitle>
      <DialogContent>
        <Typography sx={{mt: 2, mb: 1}}>아래 프로젝트 멤버의 PM평가 점수를 입력해주세요. (0-100점)</Typography>
        <List>
          {evaluatees.map(evaluatee => (
            <ListItem key={evaluatee.user_id}>
              <ListItemText primary={evaluatee.full_name} />
              <TextField
                type="number"
                size="small"
                variant="outlined"
                value={scores[evaluatee.user_id] || 0}
                onChange={(e) => handleScoreChange(evaluatee.user_id, parseInt(e.target.value, 10) || 0)}
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

export default PmEvaluationDialog;

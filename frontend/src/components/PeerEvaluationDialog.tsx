
import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, List, ListItem, ListItemText, Typography, Accordion, AccordionSummary, AccordionDetails, Alert } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { PeerEvaluationCreate } from '../schemas/evaluation';

// This is a mock schema for project members based on the API spec we defined
interface ProjectMember {
    user_id: number;
    full_name: string;
    is_pm: boolean;
    participation_weight: number;
}

interface PeerEvaluationDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: PeerEvaluationCreate) => void;
  evaluatees: ProjectMember[];
  project: { id: number; name: string };
}

const PeerEvaluationDialog: React.FC<PeerEvaluationDialogProps> = ({ open, onClose, onSubmit, evaluatees, project }) => {
  const [scores, setScores] = useState<Record<number, number>>({});
  const [feedbacks, setFeedbacks] = useState<Record<number, string>>({});
  const [average, setAverage] = useState(0);

  useEffect(() => {
    const initialScores: Record<number, number> = {};
    const initialFeedbacks: Record<number, string> = {};
    evaluatees.forEach(e => {
      initialScores[e.user_id] = 0;
      initialFeedbacks[e.user_id] = '';
    });
    setScores(initialScores);
    setFeedbacks(initialFeedbacks);
  }, [open, evaluatees]);

  useEffect(() => {
    const scoreValues = Object.values(scores);
    const total = scoreValues.reduce((sum, score) => sum + score, 0);
    const avg = scoreValues.length > 0 ? total / scoreValues.length : 0;
    setAverage(avg);
  }, [scores]);

  const handleScoreChange = (userId: number, score: number) => {
    const newScore = Math.max(0, Math.min(100, score));
    setScores(prev => ({ ...prev, [userId]: newScore }));
  };

  const handleFeedbackChange = (userId: number, feedback: string) => {
    setFeedbacks(prev => ({ ...prev, [userId]: feedback }));
  };

  const handleSubmit = () => {
    if (average > 70) {
      alert('평균 점수는 70점을 초과할 수 없습니다.');
      return;
    }
    const evaluationData: PeerEvaluationCreate = {
      evaluations: Object.entries(scores).map(([evaluatee_id, score]) => ({
        project_id: project.id,
        evaluatee_id: Number(evaluatee_id),
        score: score,
        feedback: feedbacks[Number(evaluatee_id)] || '',
      }))
    };
    onSubmit(evaluationData);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle>동료평가: {project.name}</DialogTitle>
      <DialogContent>
        <Typography sx={{mt: 2, mb: 1}}>아래 프로젝트 동료의 점수와 피드백을 입력해주세요.</Typography>
        <Alert severity={average > 70 ? "error" : "info"} sx={{mb: 2}}>
          현재 평균 점수: {average.toFixed(2)} / 70.00
        </Alert>
        <Box>
          {evaluatees.map(evaluatee => (
            <Accordion key={evaluatee.user_id}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
                  <Typography>{evaluatee.full_name}</Typography>
                  <TextField
                    type="number"
                    size="small"
                    variant="outlined"
                    value={scores[evaluatee.user_id] || 0}
                    onClick={(e) => e.stopPropagation()} // Prevent accordion from toggling
                    onChange={(e) => {
                        e.stopPropagation();
                        handleScoreChange(evaluatee.user_id, parseInt(e.target.value, 10) || 0)
                    }}
                    inputProps={{ min: 0, max: 100, style: { textAlign: 'right' } }}
                    sx={{width: '100px', mr: 2}}
                  />
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <TextField
                    label={`${evaluatee.full_name}님에 대한 서술형 피드백`}
                    multiline
                    rows={3}
                    fullWidth
                    variant="outlined"
                    value={feedbacks[evaluatee.user_id] || ''}
                    onChange={(e) => handleFeedbackChange(evaluatee.user_id, e.target.value)}
                />
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained" disabled={average > 70}>Submit</Button>
      </DialogActions>
    </Dialog>
  );
};

export default PeerEvaluationDialog;

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Divider
} from '@mui/material';
import type { DetailedEvaluationResult } from '../../schemas/evaluation';

interface EvaluationDetailDialogProps {
  open: boolean;
  onClose: () => void;
  data: DetailedEvaluationResult | null;
  loading: boolean;
}

const EvaluationDetailDialog: React.FC<EvaluationDetailDialogProps> = ({ open, onClose, data, loading }) => {
  const renderContent = () => {
    if (loading) {
      return <CircularProgress />;
    }

    if (!data) {
      return <Typography>No data available.</Typography>;
    }

    if (data.status === 'IN_PROGRESS') {
      return <Typography variant="h6" color="text.secondary">아직 평가가 완료되지 않았습니다.</Typography>;
    }

    return (
      <Box>
        <Typography variant="h6" gutterBottom>Final Result</Typography>
        <Chip 
          label={`Grade: ${data.final_evaluation?.grade || 'N/A'}`}
          color="primary"
          sx={{ mr: 1, mb: 2 }}
        />
        <Chip 
          label={`Final Score: ${data.final_evaluation?.final_score?.toFixed(2) || 'N/A'}`}
          variant="outlined"
          sx={{ mb: 2 }}
        />
        
        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" gutterBottom>Project Evaluations</Typography>
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Project</TableCell>
                <TableCell align="right">Weight</TableCell>
                <TableCell align="right">Peer Score</TableCell>
                <TableCell align="right">PM Score</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.project_evaluations.map((p) => (
                <TableRow key={p.project_id}>
                  <TableCell component="th" scope="row">{p.project_name}</TableCell>
                  <TableCell align="right">{p.participation_weight}%</TableCell>
                  <TableCell align="right">{p.peer_evaluation_score?.toFixed(2) || '-'}</TableCell>
                  <TableCell align="right">{p.pm_evaluation_score?.toFixed(2) || '-'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" gutterBottom>Qualitative Evaluation</Typography>
        <Typography variant="body1"><b>Score:</b> {data.qualitative_evaluation?.score || 'N/A'}</Typography>
        <Typography variant="body2" color="text.secondary"><b>Comment:</b> {data.qualitative_evaluation?.comment || '-'}</Typography>
      </Box>
    );
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle>
        Evaluation Details for {data?.user_info.full_name}
      </DialogTitle>
      <DialogContent sx={{ minHeight: '300px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        {renderContent()}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default EvaluationDetailDialog;

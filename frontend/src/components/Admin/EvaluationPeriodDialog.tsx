
import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box } from '@mui/material';
import type { EvaluationPeriod, EvaluationPeriodCreate, EvaluationPeriodUpdate } from '../../schemas/evaluation';

interface EvaluationPeriodDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: EvaluationPeriodCreate | EvaluationPeriodUpdate) => void;
  period: EvaluationPeriod | null;
}

const EvaluationPeriodDialog: React.FC<EvaluationPeriodDialogProps> = ({ open, onClose, onSave, period }) => {
  const [name, setName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  useEffect(() => {
    if (period) {
      setName(period.name);
      setStartDate(period.start_date.split('T')[0]); // Format for date input
      setEndDate(period.end_date.split('T')[0]);
    } else {
      setName('');
      setStartDate('');
      setEndDate('');
    }
  }, [period, open]);

  const handleSave = () => {
    const data = { name, start_date: startDate, end_date: endDate };
    onSave(data);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{period ? 'Edit Evaluation Period' : 'Add New Evaluation Period'}</DialogTitle>
      <DialogContent>
        <Box component="form" sx={{ mt: 2 }}>
          <TextField
            autoFocus
            margin="dense"
            label="Period Name"
            type="text"
            fullWidth
            variant="outlined"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Start Date"
            type="date"
            fullWidth
            variant="outlined"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            InputLabelProps={{
              shrink: true,
            }}
          />
          <TextField
            margin="dense"
            label="End Date"
            type="date"
            fullWidth
            variant="outlined"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            InputLabelProps={{
              shrink: true,
            }}
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave} variant="contained">Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default EvaluationPeriodDialog;

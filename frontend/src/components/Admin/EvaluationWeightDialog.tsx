
import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import type { EvaluationWeight, EvaluationWeightCreate, EvaluationWeightUpdate } from '../../schemas/evaluation';
import { UserRole, EvaluationItem } from '../../schemas/evaluation';

interface EvaluationWeightDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: EvaluationWeightCreate | EvaluationWeightUpdate) => void;
  weight: EvaluationWeight | null;
}

const EvaluationWeightDialog: React.FC<EvaluationWeightDialogProps> = ({ open, onClose, onSave, weight }) => {
  const [role, setRole] = useState<UserRole>(UserRole.EMPLOYEE);
  const [evaluationItem, setEvaluationItem] = useState<EvaluationItem>(EvaluationItem.PEER);
  const [itemWeight, setItemWeight] = useState(0);

  useEffect(() => {
    if (weight) {
        setRole(weight.role);
        setEvaluationItem(weight.evaluation_item);
        setItemWeight(weight.weight);
    } else {
        setRole(UserRole.EMPLOYEE);
        setEvaluationItem(EvaluationItem.PEER);
        setItemWeight(0);
    }
  }, [weight, open]);

  const handleSave = () => {
    const data = { role: role, evaluation_item: evaluationItem, weight: itemWeight };
    onSave(data);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{weight ? 'Edit Evaluation Weight' : 'Add New Evaluation Weight'}</DialogTitle>
      <DialogContent>
        <Box component="form" sx={{ mt: 2 }}>
          <FormControl fullWidth margin="dense">
            <InputLabel>User Role</InputLabel>
            <Select
              value={role}
              label="User Role"
              onChange={(e) => setRole(e.target.value as UserRole)}
              disabled={!!weight}
            >
              {Object.values(UserRole).map((roleValue) => (
                <MenuItem key={roleValue} value={roleValue}>{roleValue}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel>Evaluation Item</InputLabel>
            <Select
              value={evaluationItem}
              label="Evaluation Item"
              onChange={(e) => setEvaluationItem(e.target.value as EvaluationItem)}
              disabled={!!weight}
            >
              {Object.values(EvaluationItem).map((evalItem) => (
                <MenuItem key={evalItem} value={evalItem}>{evalItem}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label="Weight (%)"
            type="number"
            fullWidth
            variant="outlined"
            value={itemWeight}
            onChange={(e) => setItemWeight(Number(e.target.value))}
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

export default EvaluationWeightDialog;

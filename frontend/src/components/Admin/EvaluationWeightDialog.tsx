
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
  const [userRole, setUserRole] = useState<UserRole>(UserRole.EMPLOYEE);
  const [item, setItem] = useState<EvaluationItem>(EvaluationItem.PEER_REVIEW);
  const [itemWeight, setItemWeight] = useState(0);

  useEffect(() => {
    if (weight) {
        setUserRole(weight.user_role);
        setItem(weight.item);
        setItemWeight(weight.weight);
    } else {
        setUserRole(UserRole.EMPLOYEE);
        setItem(EvaluationItem.PEER_REVIEW);
        setItemWeight(0);
    }
  }, [weight, open]);

  const handleSave = () => {
    const data = { user_role: userRole, item: item, weight: itemWeight };
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
              value={userRole}
              label="User Role"
              onChange={(e) => setUserRole(e.target.value as UserRole)}
              disabled={!!weight}
            >
              {Object.values(UserRole).map((role) => (
                <MenuItem key={role} value={role}>{role}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel>Evaluation Item</InputLabel>
            <Select
              value={item}
              label="Evaluation Item"
              onChange={(e) => setItem(e.target.value as EvaluationItem)}
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

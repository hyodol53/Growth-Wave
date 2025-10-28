
import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import type { DepartmentGradeRatio, DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate } from '../../schemas/evaluation';
import { DepartmentGrade } from '../../schemas/evaluation';

interface DepartmentGradeRatioDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: DepartmentGradeRatioCreate | DepartmentGradeRatioUpdate) => void;
  ratio: DepartmentGradeRatio | null;
}

const DepartmentGradeRatioDialog: React.FC<DepartmentGradeRatioDialogProps> = ({ open, onClose, onSave, ratio }) => {
  const [departmentGrade, setDepartmentGrade] = useState<DepartmentGrade>(DepartmentGrade.B);
  const [sRatio, setSRatio] = useState(0);
  const [aRatio, setARatio] = useState(0);
  const [bRatio, setBRatio] = useState(0);

  useEffect(() => {
    if (ratio) {
        setDepartmentGrade(ratio.department_grade);
        setSRatio(ratio.s_ratio);
        setARatio(ratio.a_ratio);
        setBRatio(ratio.b_ratio);
    } else {
        setDepartmentGrade(DepartmentGrade.B);
        setSRatio(0);
        setARatio(0);
        setBRatio(0);
    }
  }, [ratio, open]);

  const handleSave = () => {
    const data = { department_grade: departmentGrade, s_ratio: sRatio, a_ratio: aRatio, b_ratio: bRatio };
    onSave(data);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{ratio ? 'Edit Grade Ratio' : 'Add New Grade Ratio'}</DialogTitle>
      <DialogContent>
        <Box component="form" sx={{ mt: 2 }}>
          <FormControl fullWidth margin="dense">
            <InputLabel>Department Grade</InputLabel>
            <Select
              value={departmentGrade}
              label="Department Grade"
              onChange={(e) => setDepartmentGrade(e.target.value as DepartmentGrade)}
              disabled={!!ratio} // Cannot edit grade for existing ratio
            >
              {Object.values(DepartmentGrade).map((grade) => (
                <MenuItem key={grade} value={grade}>{grade}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label="S-Grade Ratio (%)"
            type="number"
            fullWidth
            variant="outlined"
            value={sRatio}
            onChange={(e) => setSRatio(Number(e.target.value))}
          />
          <TextField
            margin="dense"
            label="A-Grade Ratio (%)"
            type="number"
            fullWidth
            variant="outlined"
            value={aRatio}
            onChange={(e) => setARatio(Number(e.target.value))}
          />
          <TextField
            margin="dense"
            label="B-Grade Ratio (%)"
            type="number"
            fullWidth
            variant="outlined"
            value={bRatio}
            onChange={(e) => setBRatio(Number(e.target.value))}
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

export default DepartmentGradeRatioDialog;

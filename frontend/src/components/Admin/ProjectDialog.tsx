import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
  Select, MenuItem, FormControl, InputLabel
} from '@mui/material';
import { GridLegacy as Grid } from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import type { Project, ProjectCreate, ProjectUpdate } from '../../schemas/project';
import type { User } from '../../schemas/user';
import type { Organization } from '../../schemas/organization';
import type { EvaluationPeriod } from '../../schemas/evaluation';


const initialFormData: ProjectCreate = {
  name: '',
  pm_id: 0,
  evaluation_period_id: 0,
  start_date: '',
  end_date: '',
};

interface ProjectDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (project: ProjectCreate | ProjectUpdate) => void;
  project: Project | null;
  users: User[];
  organizations: Organization[];
  evaluationPeriods: EvaluationPeriod[];
  selectedEvaluationPeriodId?: number;
}

const ProjectDialog: React.FC<ProjectDialogProps> = ({
  open,
  onClose,
  onSave,
  project,
  users,
  evaluationPeriods,
  selectedEvaluationPeriodId,
}) => {
  const [formData, setFormData] = useState<ProjectCreate | Omit<ProjectUpdate, 'id'>>(initialFormData);

  useEffect(() => {
    if (open) {
      if (project) {
        setFormData({
          name: project.name || '',
          pm_id: project.pm_id || 0,
          evaluation_period_id: project.evaluation_period_id,
          start_date: project.start_date ? project.start_date.split('T')[0] : '',
          end_date: project.end_date ? project.end_date.split('T')[0] : '',
        });
      } else {
        setFormData({
          ...initialFormData,
          pm_id: users.length > 0 ? users[0].id : 0,
          evaluation_period_id: selectedEvaluationPeriodId || 0,
        });
      }
    }
  }, [project, open, users, selectedEvaluationPeriodId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | SelectChangeEvent<number>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name!]: value }));
  };

  const handleSave = () => {
    // Ensure evaluation_period_id is set, especially for new projects
    const dataToSave = {
      ...formData,
      evaluation_period_id: formData.evaluation_period_id || selectedEvaluationPeriodId || 0,
    };
    onSave(dataToSave);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{project ? 'Edit Project' : 'Create Project'}</DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid xs={12}>
            <TextField
              name="name"
              label="Project Name"
              value={formData.name}
              onChange={handleChange}
              fullWidth
              required
            />
          </Grid>
          <Grid xs={12}>
            <FormControl fullWidth required>
              <InputLabel id="evaluation-period-select-label">Evaluation Period</InputLabel>
              <Select
                labelId="evaluation-period-select-label"
                name="evaluation_period_id"
                value={formData.evaluation_period_id}
                label="Evaluation Period"
                onChange={handleChange}
                disabled={!!project} // Don't allow changing the period for existing projects
              >
                {evaluationPeriods.map(period => (
                  <MenuItem key={period.id} value={period.id}>{period.name}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid xs={6}>
            <TextField
              name="start_date"
              label="Start Date"
              type="date"
              value={formData.start_date}
              onChange={handleChange}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid xs={6}>
            <TextField
              name="end_date"
              label="End Date"
              type="date"
              value={formData.end_date}
              onChange={handleChange}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid xs={12}>
            <FormControl fullWidth required>
              <InputLabel id="pm-select-label">Project Manager</InputLabel>
              <Select
                labelId="pm-select-label"
                name="pm_id"
                value={formData.pm_id}
                label="Project Manager"
                onChange={handleChange}
              >
                {users.map(user => (
                  <MenuItem key={user.id} value={user.id}>{user.full_name || user.username}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave} variant="contained">Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ProjectDialog;
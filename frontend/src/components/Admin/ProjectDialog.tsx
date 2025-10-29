
import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, 
  Select, MenuItem, FormControl, InputLabel
} from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import { GridLegacy as Grid } from '@mui/material';

import type { Project, ProjectCreate, ProjectUpdate } from '../../schemas/project';
import type { User } from '../../schemas/user';
import type { Organization } from '../../schemas/organization';

const initialFormData: Omit<ProjectCreate, 'owner_org_id'> = { 
  name: '', 
  description: '', 
  start_date: '', 
  end_date: '', 
  pm_id: 0, 
};

interface ProjectDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (project: ProjectCreate | ProjectUpdate) => void;
  project: Project | null;
  users: User[];
  organizations: Organization[];
}

const ProjectDialog: React.FC<ProjectDialogProps> = ({ open, onClose, onSave, project, users, organizations }) => {
  const [formData, setFormData] = useState<Omit<ProjectCreate, 'owner_org_id'>>(initialFormData);

  useEffect(() => {
    if (project) {
      setFormData({
        name: project.name || '',
        description: project.description || '',
        start_date: project.start_date ? project.start_date.split('T')[0] : '',
        end_date: project.end_date ? project.end_date.split('T')[0] : '',
        pm_id: project.pm_id || 0,
      });
    } else {
      // Only set default pm_id if users are available
      if (users.length > 0) {
        setFormData({
          ...initialFormData,
          pm_id: users[0].id,
        });
      } else {
        setFormData(initialFormData);
      }
    }
  }, [project, open, users, organizations]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | SelectChangeEvent<number>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name!]: value }));
  };

  const handleSave = () => {
    onSave(formData);
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
            <TextField
              name="description"
              label="Description"
              value={formData.description}
              onChange={handleChange}
              fullWidth
              multiline
              rows={3}
            />
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
              required
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
              required
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


import React, { useState, useEffect } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, 
  Select, MenuItem, FormControl, InputLabel, Grid
} from '@mui/material';
import { Project } from '../../schemas/project';
import { User } from '../../schemas/user';
import { Organization } from '../../schemas/organization';

interface ProjectDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (project: any) => void;
  project: Project | null;
  users: User[];
  organizations: Organization[];
}

const ProjectDialog: React.FC<ProjectDialogProps> = ({ open, onClose, onSave, project, users, organizations }) => {
  const [formData, setFormData] = useState<any>({ 
    name: '', 
    description: '', 
    start_date: '', 
    end_date: '', 
    pm_id: '', 
    owner_org_id: '' 
  });

  useEffect(() => {
    if (project) {
      setFormData({
        name: project.name || '',
        description: project.description || '',
        start_date: project.start_date ? project.start_date.split('T')[0] : '',
        end_date: project.end_date ? project.end_date.split('T')[0] : '',
        pm_id: project.pm_id || '',
        owner_org_id: project.owner_org_id || '',
      });
    } else {
      setFormData({ name: '', description: '', start_date: '', end_date: '', pm_id: '', owner_org_id: '' });
    }
  }, [project, open]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name!]: value }));
  };

  const handleSave = () => {
    onSave(formData);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{project ? 'Edit Project' : 'Create Project'}</DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <TextField
              name="name"
              label="Project Name"
              value={formData.name}
              onChange={handleChange}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={12}>
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
          <Grid item xs={6}>
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
          <Grid item xs={6}>
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
          <Grid item xs={12}>
            <FormControl fullWidth required>
              <InputLabel id="pm-select-label">Project Manager</InputLabel>
              <Select
                labelId="pm-select-label"
                name="pm_id"
                value={formData.pm_id}
                label="Project Manager"
                onChange={handleChange as any}
              >
                {users.map(user => (
                  <MenuItem key={user.id} value={user.id}>{user.full_name || user.username}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <FormControl fullWidth required>
              <InputLabel id="org-select-label">Owning Organization</InputLabel>
              <Select
                labelId="org-select-label"
                name="owner_org_id"
                value={formData.owner_org_id}
                label="Owning Organization"
                onChange={handleChange as any}
              >
                {organizations.map(org => (
                  <MenuItem key={org.id} value={org.id}>{org.name}</MenuItem>
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

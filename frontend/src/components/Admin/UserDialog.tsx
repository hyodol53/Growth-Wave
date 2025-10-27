
import React, { useState, useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { User } from '../../schemas/user';
import { Organization } from '../../schemas/organization';

interface UserDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (user: any) => void; // Let's use `any` for now for simplicity, can be refined
  user: User | null;
  allOrganizations: Organization[];
}

const UserDialog: React.FC<UserDialogProps> = ({ open, onClose, onSave, user, allOrganizations }) => {
  const [formData, setFormData] = useState<any>({});

  useEffect(() => {
    if (user) {
      setFormData({
        email: user.email,
        full_name: user.full_name || '',
        username: user.username,
        role: user.role,
        organization_id: user.organization_id || '',
        password: '' // Password should not be displayed
      });
    } else {
      // Reset form for new user
      setFormData({
        email: '',
        full_name: '',
        username: '',
        role: 'employee',
        organization_id: '',
        password: ''
      });
    }
  }, [user, open]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>) => {
    const { name, value } = e.target;
    setFormData((prev: any) => ({ ...prev, [name as string]: value }));
  };

  const handleSelectChange = (e: any) => {
      const { name, value } = e.target;
      setFormData((prev: any) => ({ ...prev, [name as string]: value }));
  }

  const handleSave = () => {
    // Filter out empty password field for updates
    const dataToSave = { ...formData };
    if (user && !dataToSave.password) {
      delete dataToSave.password;
    }
    onSave(dataToSave);
  };

  const roles = ['employee', 'team_lead', 'dept_head', 'admin'];

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{user ? 'Edit User' : 'Add New User'}</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          name="email"
          label="Email Address"
          type="email"
          fullWidth
          variant="standard"
          value={formData.email || ''}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="username"
          label="Username"
          type="text"
          fullWidth
          variant="standard"
          value={formData.username || ''}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="full_name"
          label="Full Name"
          type="text"
          fullWidth
          variant="standard"
          value={formData.full_name || ''}
          onChange={handleChange}
        />
        <TextField
          margin="dense"
          name="password"
          label={user ? "New Password (optional)" : "Password"}
          type="password"
          fullWidth
          variant="standard"
          value={formData.password || ''}
          onChange={handleChange}
        />
        <FormControl fullWidth margin="dense" variant="standard">
          <InputLabel>Role</InputLabel>
          <Select
            name="role"
            value={formData.role || ''}
            onChange={handleSelectChange}
          >
            {roles.map((role) => (
              <MenuItem key={role} value={role}>{role}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth margin="dense" variant="standard">
          <InputLabel>Organization</InputLabel>
          <Select
            name="organization_id"
            value={formData.organization_id || ''}
            onChange={handleSelectChange}
          >
            <MenuItem value=""><em>None</em></MenuItem>
            {allOrganizations.map((org) => (
              <MenuItem key={org.id} value={org.id}>{org.name}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave}>Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default UserDialog;


import React, { useState, useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, TextField, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { Organization } from '../../schemas/organization';

interface OrganizationDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (organization: Omit<Organization, 'id'>) => void;
  organization: Organization | null;
  allOrganizations: Organization[];
}

const OrganizationDialog: React.FC<OrganizationDialogProps> = ({ open, onClose, onSave, organization, allOrganizations }) => {
  const [name, setName] = useState('');
  const [level, setLevel] = useState<number | string>('');
  const [parentId, setParentId] = useState<number | string>('');

  useEffect(() => {
    if (organization) {
      setName(organization.name);
      setLevel(organization.level);
      setParentId(organization.parent_id || '');
    } else {
      // Reset form for new organization
      setName('');
      setLevel('');
      setParentId('');
    }
  }, [organization, open]);

  const handleSave = () => {
    const orgData = {
      name,
      level: Number(level),
      parent_id: parentId ? Number(parentId) : null,
      department_grade: organization?.department_grade || null, // Not editable in this form for now
    };
    onSave(orgData);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{organization ? 'Edit Organization' : 'Add New Organization'}</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Organization Name"
          type="text"
          fullWidth
          variant="standard"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          margin="dense"
          label="Level (1: Center, 2: Office, 3: Team)"
          type="number"
          fullWidth
          variant="standard"
          value={level}
          onChange={(e) => setLevel(e.target.value)}
        />
        <FormControl fullWidth margin="dense" variant="standard">
          <InputLabel>Parent Organization</InputLabel>
          <Select
            value={parentId}
            onChange={(e) => setParentId(e.target.value as number)}
          >
            <MenuItem value=""><em>None (Root Level)</em></MenuItem>
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

export default OrganizationDialog;

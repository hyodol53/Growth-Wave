
import React, { useState, useEffect, useCallback } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, 
  Select, MenuItem, FormControl, InputLabel, TextField, IconButton, List, ListItem, ListItemText, ListItemSecondaryAction, CircularProgress, Alert
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import type { Project, ProjectMember } from '../../schemas/project';
import type { User } from '../../schemas/user';
import { getProjectMembers } from '../../services/api';

interface MemberSaveData {
  user_id: number;
  weight: number;
}

interface ProjectMemberDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (members: MemberSaveData[]) => void;
  project: Project | null;
  allUsers: User[];
}

const ProjectMemberDialog: React.FC<ProjectMemberDialogProps> = ({ open, onClose, onSave, project, allUsers }) => {
  const [members, setMembers] = useState<ProjectMember[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedUser, setSelectedUser] = useState('');

  const totalWeight = members.reduce((sum, member) => sum + member.participation_weight, 0);

  const fetchMembers = useCallback(async () => {
    if (!project) return;
    setLoading(true);
    setError(null);
    try {
      // This is an assumed API endpoint. If it fails, it will be caught.
      const response = await getProjectMembers(project.id);
      const membersWithProjectId = response.data.map(m => ({ ...m, project_id: project.id }));
      setMembers(membersWithProjectId);
    } catch (e) {
      console.error("Failed to fetch project members. This might be because the API endpoint doesn't exist yet.", e);
      setError("Could not load project members. The feature might be incomplete.");
      setMembers([]); // Start with an empty list if fetch fails
    }
    setLoading(false);
  }, [project]);

  useEffect(() => {
    if (open) {
      fetchMembers();
    }
  }, [open, fetchMembers]);

  const handleAddMember = () => {
    if (!selectedUser) return;
    const userId = parseInt(selectedUser, 10);
    if (!members.some(m => m.user_id === userId)) {
      setMembers([...members, { project_id: project!.id, user_id: userId, participation_weight: 0 }]);
    }
    setSelectedUser('');
  };

  const handleRemoveMember = (userId: number) => {
    setMembers(members.filter(m => m.user_id !== userId));
  };

  const handleWeightChange = (userId: number, weight: string) => {
    const newWeight = parseInt(weight, 10) || 0;
    setMembers(members.map(m => m.user_id === userId ? { ...m, participation_weight: newWeight } : m));
  };

  const handleSave = () => {
    if (totalWeight !== 100) {
      alert('Total participation weight must be exactly 100%.');
      return;
    }
    const membersToSave = members.map(({ user_id, participation_weight }) => ({ user_id, weight: participation_weight }));
    onSave(membersToSave);
  };

  const availableUsers = allUsers.filter(u => !members.some(m => m.user_id === u.id));

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Manage Members for "{project?.name}"</DialogTitle>
      <DialogContent>
        {loading ? (
          <CircularProgress />
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6">Add Member</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <FormControl sx={{ minWidth: 200 }}>
                <InputLabel>User</InputLabel>
                <Select value={selectedUser} onChange={e => setSelectedUser(e.target.value)} label="User">
                  {availableUsers.map(u => <MenuItem key={u.id} value={u.id}>{u.full_name || u.username}</MenuItem>)}
                </Select>
              </FormControl>
              <Button onClick={handleAddMember} variant="outlined">Add</Button>
            </Box>

            <Typography variant="h6">Current Members</Typography>
            <List>
              {members.map(member => (
                <ListItem key={member.user_id}>
                  <ListItemText primary={allUsers.find(u => u.id === member.user_id)?.full_name || `User ID: ${member.user_id}`} />
                  <ListItemSecondaryAction sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                     <TextField 
                        type="number"
                        label="Weight (%)"
                        value={member.participation_weight}
                        onChange={e => handleWeightChange(member.user_id, e.target.value)}
                        sx={{ width: 120 }}
                     />
                    <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveMember(member.user_id)}>
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
            <Box sx={{ mt: 2, p: 2, border: `1px solid ${totalWeight !== 100 ? 'red' : 'green'}`}}>
                <Typography variant="h6">Total Weight: {totalWeight}%</Typography>
                {totalWeight !== 100 && <Alert severity="warning">Total weight must be 100% to save.</Alert>}
            </Box>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave} variant="contained" disabled={totalWeight !== 100 || loading || !!error}>Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ProjectMemberDialog;

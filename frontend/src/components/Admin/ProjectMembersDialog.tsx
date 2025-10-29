
import React, { useState, useEffect, useCallback } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, List, ListItem, ListItemText,
  IconButton, Typography, Autocomplete, TextField, Box, CircularProgress
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { auth } from '../../services/api';
import type { Project } from '../../schemas/project';
import type { User } from '../../schemas/user';
import type { ProjectMemberDetail, ProjectMemberAdd } from '../../schemas/project_member';

interface ProjectMembersDialogProps {
  open: boolean;
  onClose: () => void;
  project: Project | null;
  allUsers: User[];
}

const ProjectMembersDialog: React.FC<ProjectMembersDialogProps> = ({ open, onClose, project, allUsers }) => {
  const [members, setMembers] = useState<ProjectMemberDetail[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMembers = useCallback(async () => {
    if (project) {
      try {
        setLoading(true);
        setError(null);
        const data = await auth.getProjectMembers(project.id);
        setMembers(data);
      } catch (err) {
        setError('Failed to fetch project members.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
  }, [project]);

  useEffect(() => {
    if (open) {
      fetchMembers();
    }
  }, [open, fetchMembers]);

  const handleAddMember = async () => {
    if (project && selectedUser) {
      try {
        setError(null);
        const memberIn: ProjectMemberAdd = {
          user_id: selectedUser.id,
          is_pm: false, // Defaulting is_pm to false, might need adjustment
        };
        await auth.addProjectMember(project.id, memberIn);
        setSelectedUser(null); // Reset autocomplete
        fetchMembers(); // Refresh list
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to add member.');
        console.error(err);
      }
    }
  };

  const handleRemoveMember = async (userId: number) => {
    if (project && window.confirm('Are you sure you want to remove this member?')) {
      try {
        setError(null);
        await auth.removeProjectMember(project.id, userId);
        fetchMembers(); // Refresh list
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to remove member.');
        console.error(err);
      }
    }
  };

  // Exclude users who are already members from the dropdown
  const userOptions = allUsers.filter(user => !members.some(member => member.user_id === user.id));

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Manage Members for "{project?.name}"</DialogTitle>
      <DialogContent>
        {error && <Typography color="error">{error}</Typography>}

        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, mt: 1 }}>
          <Autocomplete
            options={userOptions}
            getOptionLabel={(option) => `${option.full_name} (${option.email})`}
            value={selectedUser}
            onChange={(_event, newValue) => setSelectedUser(newValue)}
            renderInput={(params) => <TextField {...params} label="Add New Member" />}
            sx={{ flexGrow: 1, mr: 1 }}
            isOptionEqualToValue={(option, value) => option.id === value.id}
          />
          <Button onClick={handleAddMember} variant="contained" disabled={!selectedUser}>
            Add
          </Button>
        </Box>

        {loading ? <CircularProgress /> : (
          <List>
            {members.map((member) => (
              <ListItem
                key={member.user_id}
                secondaryAction={
                  <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveMember(member.user_id)}>
                    <DeleteIcon />
                  </IconButton>
                }
              >
                <ListItemText
                  primary={member.full_name}
                  secondary={`Weight: ${member.participation_weight}% ${member.is_pm ? '(PM)' : ''}`}
                />
              </ListItem>
            ))}
          </List>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ProjectMembersDialog;

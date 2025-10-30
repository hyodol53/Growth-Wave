
import React, { useState, useEffect, useCallback } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, List, ListItem, ListItemText, IconButton, TextField, Box } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import api from '../../services/api';
import type { Project, User, ProjectMemberDetails } from '../../schemas';

interface ProjectMembersDialogProps {
    open: boolean;
    onClose: () => void;
    project: Project;
    users: User[];
}

const ProjectMembersDialog: React.FC<ProjectMembersDialogProps> = ({ open, onClose, project, users }) => {
    const [members, setMembers] = useState<ProjectMemberDetails[]>([]);
    const [selectedUser, setSelectedUser] = useState<string>('');

    const fetchMembers = useCallback(async () => {
        try {
            const { data } = await api.projects.getProjectMembers(project.id);
            setMembers(data);
        } catch (error) {
            console.error("Failed to fetch project members", error);
        }
    }, [project.id]);

    useEffect(() => {
        if (open) {
            fetchMembers();
        }
    }, [open, fetchMembers]);

    const handleAddMember = async () => {
        const userId = parseInt(selectedUser, 10);
        if (isNaN(userId)) return;

        try {
            await api.projects.addProjectMember(project.id, userId);
            fetchMembers();
            setSelectedUser('');
        } catch (error) {
            console.error("Failed to add project member", error);
        }
    };

    const handleRemoveMember = async (memberId: number) => {
        try {
            await api.projects.removeProjectMember(project.id, memberId);
            fetchMembers();
        } catch (error) {
            console.error("Failed to remove project member", error);
        }
    };

    const memberIds = new Set(members.map(m => m.user_id));
    const availableUsers = users.filter(u => !memberIds.has(u.id));

    return (
        <Dialog open={open} onClose={onClose} fullWidth>
            <DialogTitle>Manage Members for {project.name}</DialogTitle>
            <DialogContent>
                <List>
                    {members.map(member => (
                        <ListItem key={member.user_id} secondaryAction={
                            <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveMember(member.user_id)}>
                                <DeleteIcon />
                            </IconButton>
                        }>
                            <ListItemText primary={member.full_name} secondary={`Weight: ${member.participation_weight}%`} />
                        </ListItem>
                    ))}
                </List>
                <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                    <TextField
                        select
                        label="Select User"
                        value={selectedUser}
                        onChange={(e) => setSelectedUser(e.target.value)}
                        SelectProps={{ native: true }}
                        fullWidth
                    >
                        <option value=""></option>
                        {availableUsers.map(user => (
                            <option key={user.id} value={user.id}>
                                {user.full_name}
                            </option>
                        ))}
                    </TextField>
                    <Button onClick={handleAddMember} variant="contained">Add</Button>
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
};

export default ProjectMembersDialog;

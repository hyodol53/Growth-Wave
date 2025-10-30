import React, { useState, useEffect, useCallback } from 'react';
import { Box, Typography, Button, CircularProgress, Alert } from '@mui/material';
import { DataGrid, GridActionsCellItem, type GridColDef } from '@mui/x-data-grid';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import PeopleIcon from '@mui/icons-material/People';
import * as api from '../../services/api';
import type { Project, User, Organization, ProjectCreate, ProjectUpdate } from '../../schemas';
import ProjectDialog from '../../components/Admin/ProjectDialog';
import ProjectMembersDialog from '../../components/Admin/ProjectMembersDialog';

const ProjectManagementPage: React.FC = () => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [organizations, setOrganizations] = useState<Organization[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [isProjectDialogOpen, setIsProjectDialogOpen] = useState(false);
    const [editingProject, setEditingProject] = useState<Project | null>(null);
    const [isMembersDialogOpen, setIsMembersDialogOpen] = useState(false);
    const [selectedProjectForMembers, setSelectedProjectForMembers] = useState<Project | null>(null);

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const [projectsRes, usersRes, orgsRes] = await Promise.all([
                api.projects.getProjects(),
                api.users.getUsers(),
                api.organizations.getOrganizations(),
            ]);
            setProjects(projectsRes.data);
            setUsers(usersRes.data);
            setOrganizations(orgsRes.data);
        } catch (err) {
            setError('Failed to fetch data.');
        }
        finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const handleOpenProjectDialog = (project: Project | null) => {
        setEditingProject(project);
        setIsProjectDialogOpen(true);
    };

    const handleCloseProjectDialog = () => {
        setIsProjectDialogOpen(false);
        setEditingProject(null);
    };

    const handleSaveProject = async (projectData: ProjectCreate | ProjectUpdate) => {
        try {
            if (editingProject) {
                await api.projects.updateProject(editingProject.id, projectData as ProjectUpdate);
            } else {
                await api.projects.createProject(projectData as ProjectCreate);
            }
            fetchData();
            handleCloseProjectDialog();
        } catch (err) {
            setError('Failed to save project.');
        }
    };

    const handleDeleteProject = async (projectId: number) => {
        if (window.confirm('Are you sure you want to delete this project?')) {
            try {
                await api.projects.deleteProject(projectId);
                fetchData();
            } catch (err) {
                setError('Failed to delete project.');
            }
        }
    };

    const handleOpenMembersDialog = (project: Project) => {
        setSelectedProjectForMembers(project);
        setIsMembersDialogOpen(true);
    };

    const handleCloseMembersDialog = () => {
        setIsMembersDialogOpen(false);
        setSelectedProjectForMembers(null);
    };

    const columns: GridColDef[] = [
        { field: 'name', headerName: 'Project Name', flex: 1 },
        { field: 'description', headerName: 'Description', flex: 2 },
        {
            field: 'pm_id',
            headerName: 'Project Manager',
            flex: 1,
            valueGetter: (params: any) => users.find(u => u.id === params.value)?.full_name || '',
        },
        {
            field: 'actions',
            type: 'actions',
            headerName: 'Actions',
            width: 150,
            getActions: (params) => [
                <GridActionsCellItem icon={<PeopleIcon />} label="Manage Members" onClick={() => handleOpenMembersDialog(params.row as Project)} />,
                <GridActionsCellItem icon={<EditIcon />} label="Edit" onClick={() => handleOpenProjectDialog(params.row as Project)} />,
                <GridActionsCellItem icon={<DeleteIcon />} label="Delete" onClick={() => handleDeleteProject(params.id as number)} />,
            ],
        },
    ];

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>Project Management</Typography>
            {error && <Alert severity="error">{error}</Alert>}
            <Button variant="contained" onClick={() => handleOpenProjectDialog(null)} disabled={loading}>
                Add Project
            </Button>
            <Box sx={{ height: 600, width: '100%', mt: 2 }}>
                {loading ? <CircularProgress /> : (
                    <DataGrid
                        rows={projects}
                        columns={columns}
                        pageSizeOptions={[10, 25, 100]}
                    />
                )}
            </Box>
            <ProjectDialog
                open={isProjectDialogOpen}
                onClose={handleCloseProjectDialog}
                onSave={handleSaveProject}
                project={editingProject}
                users={users}
                organizations={organizations}
            />
            {selectedProjectForMembers && (
                <ProjectMembersDialog
                    open={isMembersDialogOpen}
                    onClose={handleCloseMembersDialog}
                    project={selectedProjectForMembers}
                    users={users}
                />
            )}
        </Box>
    );
};

export default ProjectManagementPage;
import React, { useState, useEffect, useCallback } from 'react';
import { Box, Typography, Button, CircularProgress, Alert, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { DataGrid, GridActionsCellItem, type GridColDef, type GridRenderCellParams } from '@mui/x-data-grid';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import PeopleIcon from '@mui/icons-material/People';
import * as api from '../../services/api';
import type { Project, User, Organization, ProjectCreate, ProjectUpdate, EvaluationPeriod } from '../../schemas';
import ProjectDialog from '../../components/Admin/ProjectDialog';
import ProjectMembersDialog from '../../components/Admin/ProjectMembersDialog';

const ProjectManagementPage: React.FC = () => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [organizations, setOrganizations] = useState<Organization[]>([]);
    const [evaluationPeriods, setEvaluationPeriods] = useState<EvaluationPeriod[]>([]);
    const [selectedEvaluationPeriod, setSelectedEvaluationPeriod] = useState<number | ''>('');

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [isProjectDialogOpen, setIsProjectDialogOpen] = useState(false);
    const [editingProject, setEditingProject] = useState<Project | null>(null);
    const [isMembersDialogOpen, setIsMembersDialogOpen] = useState(false);
    const [selectedProjectForMembers, setSelectedProjectForMembers] = useState<Project | null>(null);

    const fetchInitialData = useCallback(async () => {
        setLoading(true);
        try {
            const [usersRes, orgsRes, periodsRes] = await Promise.all([
                api.users.getUsers(),
                api.organizations.getOrganizations(),
                api.evaluationPeriods.getEvaluationPeriods(),
            ]);
            setUsers(usersRes.data);
            setOrganizations(orgsRes.data);
            setEvaluationPeriods(periodsRes.data);
            if (periodsRes.data.length > 0) {
                const activePeriod = periodsRes.data.find(p => p.is_active) || periodsRes.data[0];
                setSelectedEvaluationPeriod(activePeriod.id);
            }
        } catch (err) {
            setError('Failed to fetch initial data.');
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchProjects = useCallback(async (periodId: number) => {
        setLoading(true);
        try {
            const projectsRes = await api.projects.getProjects({ evaluation_period_id: periodId });
            setProjects(projectsRes.data);
        } catch (err) {
            setError('Failed to fetch projects for the selected period.');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchInitialData();
    }, [fetchInitialData]);

    useEffect(() => {
        if (selectedEvaluationPeriod) {
            fetchProjects(selectedEvaluationPeriod);
        } else {
            setProjects([]);
        }
    }, [selectedEvaluationPeriod, fetchProjects]);


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
            if (selectedEvaluationPeriod) {
                fetchProjects(selectedEvaluationPeriod);
            }
            handleCloseProjectDialog();
        } catch (err) {
            setError('Failed to save project.');
        }
    };

    const handleDeleteProject = async (projectId: number) => {
        if (window.confirm('Are you sure you want to delete this project?')) {
            try {
                await api.projects.deleteProject(projectId);
                if (selectedEvaluationPeriod) {
                    fetchProjects(selectedEvaluationPeriod);
                }
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
        {
            field: 'pm_id',
            headerName: 'Project Manager',
            flex: 1,
            renderCell: (params: GridRenderCellParams<any, User>) => users.find(u => u.id === params.row.pm_id)?.full_name || '',
        },
        { field: 'start_date', headerName: 'Start Date', flex: 1 },
        { field: 'end_date', headerName: 'End Date', flex: 1 },
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
            
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <FormControl sx={{ m: 1, minWidth: 240 }}>
                    <InputLabel id="evaluation-period-select-label">Evaluation Period</InputLabel>
                    <Select
                        labelId="evaluation-period-select-label"
                        id="evaluation-period-select"
                        value={selectedEvaluationPeriod}
                        label="Evaluation Period"
                        onChange={(e) => setSelectedEvaluationPeriod(e.target.value as number)}
                    >
                        {evaluationPeriods.map((period) => (
                            <MenuItem key={period.id} value={period.id}>
                                {period.name} ({period.is_active ? 'Active' : 'Inactive'})
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <Button variant="contained" onClick={() => handleOpenProjectDialog(null)} disabled={loading || !selectedEvaluationPeriod}>
                    Add Project
                </Button>
            </Box>

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
                evaluationPeriods={evaluationPeriods}
                selectedEvaluationPeriodId={selectedEvaluationPeriod || undefined}
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
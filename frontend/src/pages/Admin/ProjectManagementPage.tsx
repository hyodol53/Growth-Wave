
import React, { useState, useEffect, useCallback } from 'react';
import { Box, Container, Typography, Button, Paper } from '@mui/material';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import type { GridColDef } from '@mui/x-data-grid';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import GroupAddIcon from '@mui/icons-material/GroupAdd';

import { auth } from '../../services/api';
import type { Project, ProjectCreate, ProjectUpdate } from '../../schemas/project';
import type { User } from '../../schemas/user';
import type { Organization } from '../../schemas/organization';

import ProjectDialog from '../../components/Admin/ProjectDialog';
import ProjectMemberDialog from '../../components/Admin/ProjectMemberDialog';

interface MemberSaveData {
  user_id: number;
  weight: number;
}

const ProjectManagementPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Dialog states
  const [isProjectDialogOpen, setIsProjectDialogOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [isMemberDialogOpen, setIsMemberDialogOpen] = useState(false);
  const [managingMembersFor, setManagingMembersFor] = useState<Project | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const [projectsData, usersData, orgsData] = await Promise.all([
        auth.getProjects(),
        auth.getUsers(),
        auth.getOrganizations(),
      ]);
      setProjects(projectsData);
      setUsers(usersData);
      setOrganizations(orgsData);
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // --- Handlers for Dialogs ---
  const handleOpenProjectDialog = (project: Project | null) => {
    setEditingProject(project);
    setIsProjectDialogOpen(true);
  };
  const handleCloseProjectDialog = () => {
    setEditingProject(null);
    setIsProjectDialogOpen(false);
  };

  const handleOpenMemberDialog = (project: Project) => {
    setManagingMembersFor(project);
    setIsMemberDialogOpen(true);
  };
  const handleCloseMemberDialog = () => {
    setManagingMembersFor(null);
    setIsMemberDialogOpen(false);
  };

  // --- API Action Handlers ---
  const handleSaveProject = async (data: ProjectCreate | ProjectUpdate) => {
    try {
      if (editingProject) {
        await auth.updateProject(editingProject.id, data);
      } else {
        await auth.createProject(data as ProjectCreate);
      }
      handleCloseProjectDialog();
      fetchData();
    } catch (error) {
      console.error("Failed to save project", error);
    }
  };

  const handleDeleteProject = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await auth.deleteProject(id);
        fetchData(); // Refresh data
      } catch (error) {
        console.error('Failed to delete project', error);
      }
    }
  };

  const handleSaveMembers = async (members: MemberSaveData[]) => {
    if (!managingMembersFor) return;
    try {
      await auth.setProjectMemberWeights({ 
        project_id: managingMembersFor.id, 
        weights: members
      });
      handleCloseMemberDialog();
      // No need to fetchData() as this doesn't change the project list view
    } catch (error) {
      console.error('Failed to save project members', error);
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Project Name', width: 250 },
    {
      field: 'pm_id',
      headerName: 'Project Manager',
      width: 180,
      valueGetter: (_value, row) => users.find(u => u.id === row.pm_id)?.full_name || 'N/A',
    },
    {
      field: 'owner_org_id',
      headerName: 'Owning Organization',
      width: 200,
      valueGetter: (_value, row) => organizations.find(o => o.id === row.owner_org_id)?.name || 'N/A',
    },
    { field: 'start_date', headerName: 'Start Date', width: 120 },
    { field: 'end_date', headerName: 'End Date', width: 120 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 150,
      getActions: (params) => [
        <GridActionsCellItem icon={<EditIcon />} label="Edit" onClick={() => handleOpenProjectDialog(params.row as Project)} />,
        <GridActionsCellItem icon={<DeleteIcon />} label="Delete" onClick={() => handleDeleteProject(params.id as number)} />,
        <GridActionsCellItem icon={<GroupAddIcon />} label="Manage Members" onClick={() => handleOpenMemberDialog(params.row as Project)} />,
      ],
    },
  ];

  return (
    <Container maxWidth="xl">
      <ProjectDialog 
        open={isProjectDialogOpen}
        onClose={handleCloseProjectDialog}
        onSave={handleSaveProject}
        project={editingProject}
        users={users}
        organizations={organizations}
      />
      {managingMembersFor && (
        <ProjectMemberDialog 
          open={isMemberDialogOpen}
          onClose={handleCloseMemberDialog}
          onSave={handleSaveMembers}
          project={managingMembersFor}
          allUsers={users}
        />
      )}

      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Project Management
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Button variant="contained" onClick={() => handleOpenProjectDialog(null)}>
            Create Project
          </Button>
        </Box>
        <Paper sx={{ height: 700, width: '100%' }}>
          <DataGrid
            rows={projects}
            columns={columns}
            loading={loading}
            initialState={{
              pagination: {
                paginationModel: {
                  pageSize: 10,
                },
              },
            }}
            pageSizeOptions={[10, 20, 50]}
            checkboxSelection
            disableRowSelectionOnClick
          />
        </Paper>
      </Box>
    </Container>
  );
};

export default ProjectManagementPage;

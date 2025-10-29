import React, { useState, useEffect, useCallback } from 'react';
import { Box, Container, Typography, Button, Paper } from '@mui/material';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import type { GridColDef } from '@mui/x-data-grid';
import PeopleIcon from '@mui/icons-material/People';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

import { auth } from '../../services/api';
import type { Project, ProjectCreate, ProjectUpdate } from '../../schemas/project';
import type { User } from '../../schemas/user';
import type { Organization } from '../../schemas/organization';

import ProjectDialog from '../../components/Admin/ProjectDialog';
import ProjectMembersDialog from '../../components/Admin/ProjectMembersDialog';

const ProjectManagementPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Dialog states
  const [isProjectDialogOpen, setIsProjectDialogOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [isMembersDialogOpen, setIsMembersDialogOpen] = useState(false);
  const [selectedProjectForMembers, setSelectedProjectForMembers] = useState<Project | null>(null);

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
      console.error("데이터를 불러오는데 실패했습니다.", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // --- Handlers for Project Dialog ---
  const handleOpenProjectDialog = (project: Project | null) => {
    setEditingProject(project);
    setIsProjectDialogOpen(true);
  };
  const handleCloseProjectDialog = () => {
    setEditingProject(null);
    setIsProjectDialogOpen(false);
  };

  // --- Handlers for Members Dialog ---
  const handleOpenMembersDialog = (project: Project) => {
    setSelectedProjectForMembers(project);
    setIsMembersDialogOpen(true);
  };

  const handleCloseMembersDialog = () => {
    setSelectedProjectForMembers(null);
    setIsMembersDialogOpen(false);
    // Optionally refresh data if weights might affect other views
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
    if (window.confirm('이 프로젝트를 정말로 삭제하시겠습니까?')) {
      try {
        await auth.deleteProject(id);
        fetchData(); // Refresh data
      } catch (error) {
        console.error('프로젝트 삭제에 실패했습니다.', error);
      }
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: '프로젝트 이름', width: 250 },
    {
      field: 'pm_id',
      headerName: '프로젝트 매니저',
      width: 180,
      valueGetter: (_value, row) => users.find(u => u.id === row.pm_id)?.full_name || '없음',
    },

    { field: 'start_date', headerName: '시작일', width: 120 },
    { field: 'end_date', headerName: '종료일', width: 120 },
    {
      field: 'actions',
      type: 'actions',
      headerName: '작업',
      width: 150,
      getActions: (params) => [
        <GridActionsCellItem icon={<PeopleIcon />} label="멤버 관리" onClick={() => handleOpenMembersDialog(params.row as Project)} />,
        <GridActionsCellItem icon={<EditIcon />} label="수정" onClick={() => handleOpenProjectDialog(params.row as Project)} />,
        <GridActionsCellItem icon={<DeleteIcon />} label="삭제" onClick={() => handleDeleteProject(params.id as number)} />,
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

      <ProjectMembersDialog
        open={isMembersDialogOpen}
        onClose={handleCloseMembersDialog}
        project={selectedProjectForMembers}
        allUsers={users}
      />

      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          프로젝트 관리
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Button variant="contained" onClick={() => handleOpenProjectDialog(null)} disabled={loading}>
            프로젝트 생성
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
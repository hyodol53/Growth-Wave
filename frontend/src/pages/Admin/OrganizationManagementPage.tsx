import React, { useState, useEffect, useCallback } from 'react';
import { Box, Container, Typography, Paper, Button, IconButton } from '@mui/material';
import { GridLegacy as Grid } from '@mui/material';
import { SimpleTreeView } from '@mui/x-tree-view/SimpleTreeView';
import { TreeItem, type TreeItemProps } from '@mui/x-tree-view/TreeItem';
import { styled } from '@mui/material/styles';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import type { GridColDef } from '@mui/x-data-grid';
import { auth } from '../../services/api';
import type { Organization } from '../../schemas/organization';
import type { User, UserCreate, UserUpdate } from '../../schemas/user';
import OrganizationDialog from '../../components/Admin/OrganizationDialog';
import UserDialog from '../../components/Admin/UserDialog';
import OrgSync from '../../components/Admin/OrgSync';

// Interface for the hierarchical node structure
interface OrgTreeNode {
  id: string;
  name: string;
  children: OrgTreeNode[];
  original: Organization;
}

// Custom TreeItem to include action buttons
const StyledTreeItem = styled((props: TreeItemProps & { onEdit: () => void; onDelete: () => void }) => {
    const { onEdit, onDelete, ...other } = props;
    return (
      <TreeItem
        {...other}
        label={
          <Box sx={{ display: 'flex', alignItems: 'center', p: 0.5, pr: 0 }}>
            <Typography variant="body2" sx={{ flexGrow: 1 }}>
              {props.label}
            </Typography>
            <IconButton size="small" onClick={(e) => { e.stopPropagation(); onEdit(); }}><EditIcon fontSize="inherit" /></IconButton>
            <IconButton size="small" onClick={(e) => { e.stopPropagation(); onDelete(); }}><DeleteIcon fontSize="inherit" /></IconButton>
          </Box>
        }
      />
    );
  })({});

const OrganizationManagementPage: React.FC = () => {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [orgTree, setOrgTree] = useState<OrgTreeNode[]>([]);
  const [selectedOrgId, setSelectedOrgId] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  
  const [isOrgDialogOpen, setIsOrgDialogOpen] = useState(false);
  const [editingOrg, setEditingOrg] = useState<Organization | null>(null);
  const [isUserDialogOpen, setIsUserDialogOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const [orgsData, usersData] = await Promise.all([
        auth.getOrganizations(),
        auth.getUsers(),
      ]);
      setOrganizations(orgsData);
      setUsers(usersData);
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    const buildTree = (items: Organization[], parentId: number | null = null): OrgTreeNode[] => {
      return items
        .filter(item => item.parent_id === parentId)
        .map(item => ({
          id: String(item.id),
          name: item.name,
          children: buildTree(items, item.id),
          original: item,
        }));
    };
    setOrgTree(buildTree(organizations));
  }, [organizations]);

  // --- Handlers ---
  const handleOrgSelect = (_event: React.SyntheticEvent| null , nodeId: string | null) => {
    if ( nodeId){
      const orgId = parseInt(nodeId, 10);
      setSelectedOrgId(orgId);
    }    
  };

  // Org Dialog
  const handleOpenOrgDialog = (org: Organization | null) => { setEditingOrg(org); setIsOrgDialogOpen(true); };
  const handleCloseOrgDialog = () => { setEditingOrg(null); setIsOrgDialogOpen(false); };

  // User Dialog
  const handleOpenUserDialog = (user: User | null) => { setEditingUser(user); setIsUserDialogOpen(true); };
  const handleCloseUserDialog = () => { setEditingUser(null); setIsUserDialogOpen(false); };

  // --- API Actions ---
  const handleSaveOrganization = async (data: Omit<Organization, 'id'>) => {
    try {
      if (editingOrg) {
        await auth.updateOrganization(editingOrg.id, data);
      } else {
        await auth.createOrganization(data);
      }
      handleCloseOrgDialog();
      fetchData();
    } catch (error) { console.error("Failed to save organization", error); }
  };

  const handleDeleteOrganization = async (orgId: number) => {
    if (window.confirm("이 조직을 정말로 삭제하시겠습니까?")) {
      try {
        await auth.deleteOrganization(orgId);
        fetchData();
      } catch (error) { console.error("Failed to delete organization", error); }
    }
  };

  const handleSaveUser = async (data: UserCreate | UserUpdate) => {
    try {
      if (editingUser) {
        await auth.updateUser(editingUser.id, data);
      } else {
        await auth.createUser(data as UserCreate);
      }
      handleCloseUserDialog();
      fetchData();
    } catch (error) { console.error("Failed to save user", error); }
  };

  const handleDeleteUser = async (userId: number) => {
    if (window.confirm("이 사용자를 정말로 삭제하시겠습니까?")) {
      try {
        await auth.deleteUser(userId);
        fetchData();
      } catch (error) { console.error("Failed to delete user", error); }
    }
  };

  // --- Render Logic ---
  const renderTree = (nodes: OrgTreeNode[]) => (
    nodes.map((node) => (
      <StyledTreeItem 
        key={node.id} 
        itemId={node.id} 
        label={node.name}
        onEdit={() => handleOpenOrgDialog(node.original)}
        onDelete={() => handleDeleteOrganization(node.original.id)}
      >
        {Array.isArray(node.children) ? renderTree(node.children) : null}
      </StyledTreeItem>
    ))
  );

  const userColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'full_name', headerName: '이름', width: 150 },
    { field: 'username', headerName: '사용자 이름', width: 130 },
    { field: 'email', headerName: '이메일', width: 180 },
    { field: 'role', headerName: '역할', width: 110 },
    {
      field: 'organization',
      headerName: '조직',
      width: 130,
      valueGetter: (_value, row) => organizations.find(org => org.id === row.organization_id)?.name || '없음',
    },
    {
        field: 'actions',
        type: 'actions',
        headerName: '작업',
        width: 100,
        getActions: (params) => [
            <GridActionsCellItem icon={<EditIcon />} label="수정" onClick={() => handleOpenUserDialog(params.row as User)} />,
            <GridActionsCellItem icon={<DeleteIcon />} label="삭제" onClick={() => handleDeleteUser(params.id as number)} />,
        ]
    }
  ];

  const filteredUsers = selectedOrgId
    ? users.filter(user => user.organization_id === selectedOrgId)
    : users;

  return (
    <Container maxWidth="xl">
      <OrganizationDialog 
        open={isOrgDialogOpen}
        onClose={handleCloseOrgDialog}
        onSave={handleSaveOrganization}
        organization={editingOrg}
        allOrganizations={organizations}
      />
      <UserDialog 
        open={isUserDialogOpen}
        onClose={handleCloseUserDialog}
        onSave={handleSaveUser}
        user={editingUser}
        allOrganizations={organizations}
      />
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          조직 및 사용자 관리
        </Typography>
        <OrgSync onSyncSuccess={fetchData} />
        <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
            <Button variant="contained" onClick={() => handleOpenOrgDialog(null)}>조직 추가</Button>
            <Button variant="contained" onClick={() => handleOpenUserDialog(null)}>사용자 추가</Button>
        </Box>
        <Grid container spacing={3}>
          <Grid xs={12} md={4}>
            <Paper sx={{ p: 2, minHeight: 600 }}>
              <Typography variant="h6" gutterBottom>조직</Typography>
              <SimpleTreeView
                aria-label="조직 트리"
                slots={{ 
                  collapseIcon: ExpandMoreIcon, 
                  expandIcon: ChevronRightIcon 
                }}
                sx={{ flexGrow: 1, overflowY: 'auto' }}
                onSelectedItemsChange={handleOrgSelect}
              >
                {renderTree(orgTree)}
              </SimpleTreeView>
            </Paper>
          </Grid>
          <Grid xs={12} md={8}>
            <Paper sx={{ height: 650, width: '100%' }}>
              <Typography variant="h6" gutterBottom sx={{ p: 2 }}>
                사용자 {selectedOrgId ? `(${organizations.find(o => o.id === selectedOrgId)?.name})` : ''}
              </Typography>
              <DataGrid
                rows={filteredUsers}
                columns={userColumns}
                loading={loading}
                initialState={{
                    pagination: {
                      paginationModel: {
                        pageSize: 10,
                      },
                    },
                  }}
                pageSizeOptions={[5, 10, 20]}
                checkboxSelection
                disableRowSelectionOnClick
              />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default OrganizationManagementPage;
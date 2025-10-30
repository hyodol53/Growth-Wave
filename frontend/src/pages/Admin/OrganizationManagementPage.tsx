// @ts-nocheck
import React, { useState, useEffect, useCallback } from 'react';
import { Box, Typography, Paper, Button, IconButton, Alert } from '@mui/material';
import Grid from '@mui/material/Grid';
import { SimpleTreeView } from '@mui/x-tree-view/SimpleTreeView';
import { TreeItem, type TreeItemProps } from '@mui/x-tree-view/TreeItem';
import { styled } from '@mui/material/styles';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import type { GridColDef } from '@mui/x-data-grid';
import * as api from '../../services/api';
import type { Organization, OrganizationCreate, OrganizationUpdate } from '../../schemas/organization';
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
  const [error, setError] = useState<string | null>(null);
  
  const [isOrgDialogOpen, setIsOrgDialogOpen] = useState(false);
  const [editingOrg, setEditingOrg] = useState<Organization | null>(null);
  const [isUserDialogOpen, setIsUserDialogOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [orgsRes, usersRes] = await Promise.all([
        api.organizations.getOrganizations(),
        api.users.getUsers(),
      ]);
      setOrganizations(orgsRes.data);
      setUsers(usersRes.data);
    } catch (err) {
      setError('Failed to fetch data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    const buildOrgTree = (orgs: Organization[]): OrgTreeNode[] => {
        const orgMap = new Map<number, OrgTreeNode>();
        const roots: OrgTreeNode[] = [];

        orgs.forEach(org => {
            orgMap.set(org.id, {
                id: org.id.toString(),
                name: org.name,
                children: [],
                original: org,
            });
        });

        orgs.forEach(org => {
            if (org.parent_id && orgMap.has(org.parent_id)) {
                orgMap.get(org.parent_id)!.children.push(orgMap.get(org.id)!);
            } else {
                roots.push(orgMap.get(org.id)!);
            }
        });
        return roots;
    };
    setOrgTree(buildOrgTree(organizations));
  }, [organizations]);


  const handleOpenOrgDialog = (org: Organization | null) => {
    setEditingOrg(org);
    setIsOrgDialogOpen(true);
  };

  const handleCloseOrgDialog = () => {
    setIsOrgDialogOpen(false);
    setEditingOrg(null);
  };

  const handleSaveOrganization = async (orgData: OrganizationCreate | OrganizationUpdate) => {
    try {
      setError(null);
      if (editingOrg) {
        await api.organizations.updateOrganization(editingOrg.id, orgData as OrganizationUpdate);
      } else {
        await api.organizations.createOrganization(orgData as OrganizationCreate);
      }
      fetchData();
      handleCloseOrgDialog();
    } catch (err) {
      setError('Failed to save organization.');
    }
  };

  const handleDeleteOrganization = async (orgId: number) => {
    if (window.confirm('Are you sure you want to delete this organization? This might affect its members.')) {
      try {
        setError(null);
        await api.organizations.deleteOrganization(orgId);
        fetchData();
      } catch (err) {
        setError('Failed to delete organization.');
      }
    }
  };

  const handleOpenUserDialog = (user: User | null) => {
    setEditingUser(user);
    setIsUserDialogOpen(true);
  };

  const handleCloseUserDialog = () => {
    setIsUserDialogOpen(false);
    setEditingUser(null);
  };

  const handleSaveUser = async (userData: UserCreate | UserUpdate) => {
    try {
      setError(null);
      if (editingUser) {
        await api.users.updateUser(editingUser.id, userData as UserUpdate);
      } else {
        await api.users.createUser(userData as UserCreate);
      }
      fetchData();
      handleCloseUserDialog();
    } catch (err) {
      setError('Failed to save user.');
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        setError(null);
        await api.users.deleteUser(userId);
        fetchData();
      } catch (err) {
        setError('Failed to delete user.');
      }
    }
  };

  const handleOrgSelect = (_event: React.SyntheticEvent | null, itemIds: string | string[] | null) => {
    const newId = Array.isArray(itemIds) ? itemIds[0] : itemIds;
    setSelectedOrgId(newId ? parseInt(newId, 10) : null);
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
    { field: 'id', headerName: 'ID', flex: 0.1, minWidth: 70 },
    { field: 'full_name', headerName: '이름', flex: 0.2, minWidth: 150 },
    { field: 'username', headerName: '사용자 이름', flex: 0.2, minWidth: 130 },
    { field: 'email', headerName: '이메일', flex: 0.3, minWidth: 180 },
    { field: 'role', headerName: '역할', flex: 0.15, minWidth: 110 },
    {
      field: 'organization',
      headerName: '조직',
      flex: 0.15,
      minWidth: 130,
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
    <Box>
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
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
            <Button variant="contained" onClick={() => handleOpenOrgDialog(null)}>조직 추가</Button>
            <Button variant="contained" onClick={() => handleOpenUserDialog(null)}>사용자 추가</Button>
        </Box>
        <Paper sx={{ p: 2 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom>조직</Typography>
              <Box sx={{ height: 600, overflowY: 'auto', border: '1px solid #ddd', borderRadius: '4px' }}>
                <SimpleTreeView
                  aria-label="조직 트리"
                  slots={{ 
                    collapseIcon: ExpandMoreIcon, 
                    expandIcon: ChevronRightIcon 
                  }}
                  sx={{ flexGrow: 1, p: 1 }}
                  onSelectedItemsChange={handleOrgSelect}
                >
                  {renderTree(orgTree)}
                </SimpleTreeView>
              </Box>
            </Grid>
            <Grid item xs={12} md={8}>
              <Typography variant="h6" gutterBottom>
                사용자 {selectedOrgId ? `(${organizations.find(o => o.id === selectedOrgId)?.name})` : ''}
              </Typography>
              <Box sx={{ height: 600, width: '100%' }}>
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
              </Box>
            </Grid>
          </Grid>
        </Paper>
        <Box sx={{ mt: 3 }}>
          <OrgSync onSyncSuccess={fetchData} />
        </Box>
      </Box>
    </Box>
  );
};

export default OrganizationManagementPage;

import React, { useState, useEffect, useCallback } from 'react';
import { Box, Container, Typography, Grid, Paper, Button, IconButton } from '@mui/material';
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem, TreeItemProps } from '@mui/x-tree-view/TreeItem';
import { styled } from '@mui/material/styles';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { DataGrid, GridColDef, GridActionsCellItem } from '@mui/x-data-grid';
import { auth } from '../../services/api';
import { Organization } from '../../schemas/organization';
import { User } from '../../schemas/user';
import OrganizationDialog from '../../components/Admin/OrganizationDialog';
import UserDialog from '../../components/Admin/UserDialog';

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
  const handleOrgSelect = (event: React.SyntheticEvent, nodeId: string) => {
    const orgId = parseInt(nodeId, 10);
    setSelectedOrgId(orgId);
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
    if (window.confirm("Are you sure you want to delete this organization?")) {
      try {
        await auth.deleteOrganization(orgId);
        fetchData();
      } catch (error) { console.error("Failed to delete organization", error); }
    }
  };

  const handleSaveUser = async (data: any) => {
    try {
      if (editingUser) {
        await auth.updateUser(editingUser.id, data);
      } else {
        await auth.createUser(data);
      }
      handleCloseUserDialog();
      fetchData();
    } catch (error) { console.error("Failed to save user", error); }
  };

  const handleDeleteUser = async (userId: number) => {
    if (window.confirm("Are you sure you want to delete this user?")) {
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
        nodeId={node.id} 
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
    { field: 'full_name', headerName: 'Full Name', width: 150 },
    { field: 'username', headerName: 'Username', width: 130 },
    { field: 'email', headerName: 'Email', width: 180 },
    { field: 'role', headerName: 'Role', width: 110 },
    {
      field: 'organization',
      headerName: 'Organization',
      width: 130,
      valueGetter: (value, row) => organizations.find(org => org.id === row.organization_id)?.name || 'N/A',
    },
    {
        field: 'actions',
        type: 'actions',
        headerName: 'Actions',
        width: 100,
        getActions: (params) => [
            <GridActionsCellItem icon={<EditIcon />} label="Edit" onClick={() => handleOpenUserDialog(params.row as User)} />,
            <GridActionsCellItem icon={<DeleteIcon />} label="Delete" onClick={() => handleDeleteUser(params.id as number)} />,
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
          Organization and User Management
        </Typography>
        <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
            <Button variant="contained" onClick={() => handleOpenOrgDialog(null)}>Add Organization</Button>
            <Button variant="contained" onClick={() => handleOpenUserDialog(null)}>Add User</Button>
        </Box>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2, minHeight: 600 }}>
              <Typography variant="h6" gutterBottom>Organizations</Typography>
              <TreeView
                aria-label="organization tree"
                defaultCollapseIcon={<ExpandMoreIcon />}
                defaultExpandIcon={<ChevronRightIcon />}
                sx={{ flexGrow: 1, overflowY: 'auto' }}
                onNodeSelect={handleOrgSelect}
              >
                {renderTree(orgTree)}
              </TreeView>
            </Paper>
          </Grid>
          <Grid item xs={12} md={8}>
            <Paper sx={{ height: 650, width: '100%' }}>
              <Typography variant="h6" gutterBottom sx={{ p: 2 }}>
                Users {selectedOrgId ? `in "${organizations.find(o => o.id === selectedOrgId)?.name}"` : ''}
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
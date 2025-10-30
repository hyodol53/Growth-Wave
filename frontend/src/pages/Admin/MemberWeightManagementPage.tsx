
import React, { useState, useEffect } from 'react';

import { Box, Typography, CircularProgress, Alert, List, ListItem, ListItemText, Button } from '@mui/material';

import api from '../../services/api';

import type { User } from '../../schemas';

import UserProjectWeightsDialog from '../../components/Admin/UserProjectWeightsDialog';



const MemberWeightManagementPage: React.FC = () => {

    const [users, setUsers] = useState<User[]>([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState<string | null>(null);

    const [selectedUser, setSelectedUser] = useState<User | null>(null);

    const [isDialogOpen, setIsDialogOpen] = useState(false);



    const fetchData = async () => {

        try {

            setLoading(true);

            const { data } = await api.users.getMySubordinates();

            setUsers(data);

        } catch (err) {

            setError('Failed to load subordinates.');

        } finally {

            setLoading(false);

        }

    };



    useEffect(() => {

        fetchData();

    }, []);



    const handleOpenDialog = (user: User) => {

        setSelectedUser(user);

        setIsDialogOpen(true);

    };



    const handleCloseDialog = () => {

        setSelectedUser(null);

        setIsDialogOpen(false);

        fetchData(); // Refresh data on close

    };



    if (loading) return <CircularProgress />;

    if (error) return <Alert severity="error">{error}</Alert>;



    return (

        <Box sx={{ p: 3 }}>

            <Typography variant="h4" gutterBottom>프로젝트 투입률 설정</Typography>

            <List>

                {users.map(user => (

                    <ListItem key={user.id} secondaryAction={

                        <Button variant="outlined" onClick={() => handleOpenDialog(user)}>

                            투입률 관리

                        </Button>

                    }>

                        <ListItemText primary={user.full_name} secondary={user.email} />

                    </ListItem>

                ))}

            </List>

            {selectedUser && (

                <UserProjectWeightsDialog

                    open={isDialogOpen}

                    onClose={handleCloseDialog}

                    user={selectedUser}

                />

            )}

        </Box>

    );

};



export default MemberWeightManagementPage;



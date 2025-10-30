
import React, { useState, useEffect, useCallback } from 'react';

import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Typography } from '@mui/material';

import api from '../../services/api';

import type { User } from '../../schemas';

import type { UserProjectWeight } from '../../schemas';



interface UserProjectWeightsDialogProps {

    open: boolean;

    onClose: () => void;

    user: User | null;

}



const UserProjectWeightsDialog: React.FC<UserProjectWeightsDialogProps> = ({ open, onClose, user }) => {

    const [weights, setWeights] = useState<UserProjectWeight[]>([]);

    const [loading, setLoading] = useState(false);



    const fetchWeights = useCallback(async () => {

      if (user) {

        setLoading(true);

        try {

          const { data } = await api.users.getUserProjectWeights(user.id);

          setWeights(data);

        } catch (err) {

          console.error('Failed to fetch project weights', err);

        } finally {

          setLoading(false);

        }

      }

    }, [user]);



    useEffect(() => {

        if (open) {

            fetchWeights();

        }

    }, [open, fetchWeights]);



    const handleWeightChange = (projectId: number, value: string) => {

        const newWeights = weights.map(w =>

            w.project_id === projectId ? { ...w, participation_weight: parseInt(value, 10) || 0 } : w

        );

        setWeights(newWeights);

    };



    const handleSave = async () => {

        if (user) {

            try {

                await api.users.updateUserProjectWeights(user.id, { weights });

                onClose();

            } catch (err) {

                console.error('Failed to update project weights', err);

            }

        }

    };



    const totalWeight = weights.reduce((sum, w) => sum + w.participation_weight, 0);



    return (

        <Dialog open={open} onClose={onClose} fullWidth>

            <DialogTitle>Manage Project Weights for {user?.full_name}</DialogTitle>

            <DialogContent>

                {loading ? <Typography>Loading...</Typography> : (

                    <Box component="form" noValidate autoComplete="off">

                        {weights.map(w => (

                            <TextField

                                key={w.project_id}

                                label={w.project_name}

                                type="number"

                                value={w.participation_weight}

                                onChange={(e) => handleWeightChange(w.project_id, e.target.value)}

                                fullWidth

                                margin="normal"

                            />

                        ))}

                        <Typography color={totalWeight !== 100 ? 'error' : 'textPrimary'}>

                            Total Weight: {totalWeight}%

                        </Typography>

                    </Box>

                )}

            </DialogContent>

            <DialogActions>

                <Button onClick={onClose}>Cancel</Button>

                <Button onClick={handleSave} variant="contained" disabled={totalWeight !== 100}>Save</Button>

            </DialogActions>

        </Dialog>

    );

};



export default UserProjectWeightsDialog;



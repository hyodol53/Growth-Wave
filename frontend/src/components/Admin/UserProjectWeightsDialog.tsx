
import React, { useState, useEffect, useCallback } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, Box, Typography, 
  TextField, List, ListItem, ListItemText, CircularProgress, Alert
} from '@mui/material';

import { auth } from '../../services/api';
import type { UserProjectWeight, UserProjectWeightsUpdate } from '../../services/api';
import type { User } from '../../schemas/user';

interface UserProjectWeightsDialogProps {
  open: boolean;
  onClose: () => void;
  user: User | null;
}

const UserProjectWeightsDialog: React.FC<UserProjectWeightsDialogProps> = ({ open, onClose, user }) => {
  const [weights, setWeights] = useState<UserProjectWeight[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalWeight = weights.reduce((sum, item) => sum + item.participation_weight, 0);

  const fetchWeights = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const data = await auth.getUserProjectWeights(user.id);
      setWeights(data);
    } catch (e) {
      console.error("Failed to fetch user project weights", e);
      setError("Could not load user project weights.");
      setWeights([]);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    if (open && user) {
      fetchWeights();
    }
  }, [open, user, fetchWeights]);

  const handleWeightChange = (projectId: number, weight: string) => {
    const newWeight = parseInt(weight, 10) || 0;
    setWeights(weights.map(w => w.project_id === projectId ? { ...w, participation_weight: newWeight } : w));
  };

  const handleSave = async () => {
    if (!user || totalWeight !== 100) {
      alert('Total participation weight must be exactly 100%.');
      return;
    }

    const weightsToSave: UserProjectWeightsUpdate = {
      weights: weights.map(({ project_id, participation_weight }) => ({ project_id, participation_weight }))
    };

    setLoading(true);
    try {
      await auth.updateUserProjectWeights(user.id, weightsToSave);
      onClose();
    } catch (e) {
      console.error("Failed to update weights", e);
      setError("An error occurred while saving. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Manage Project Weights for "{user?.full_name}"</DialogTitle>
      <DialogContent>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}><CircularProgress /></Box>
        ) : error ? (
          <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>
        ) : (
          <Box sx={{ mt: 2 }}>
            <List>
              {weights.map(item => (
                <ListItem key={item.project_id}>
                  <ListItemText primary={item.project_name} />
                  <TextField 
                      type="number"
                      label="Weight (%)"
                      value={item.participation_weight}
                      onChange={e => handleWeightChange(item.project_id, e.target.value)}
                      sx={{ width: 120 }}
                      inputProps={{ min: 0, max: 100 }}
                  />
                </ListItem>
              ))}
            </List>
            {weights.length === 0 && (
                <Typography sx={{ textAlign: 'center', my: 2 }}>This user is not assigned to any projects.</Typography>
            )}
            <Box sx={{ mt: 2, p: 2, borderRadius: 1, border: `1px solid ${totalWeight !== 100 ? 'red' : 'green'}`}}>
                <Typography variant="h6">Total Weight: {totalWeight}%</Typography>
                {totalWeight !== 100 && <Alert severity="warning" sx={{mt: 1}}>Total weight must be 100% to save.</Alert>}
            </Box>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button 
          onClick={handleSave} 
          variant="contained" 
          disabled={totalWeight !== 100 || loading || !!error || weights.length === 0}
        >
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default UserProjectWeightsDialog;

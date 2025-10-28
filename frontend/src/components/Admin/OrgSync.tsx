import React, { useState, useCallback } from 'react';
import { Box, Button, Input, Typography, CircularProgress, Alert } from '@mui/material';
import { auth } from '../../services/api';

interface OrgSyncProps {
  onSyncSuccess: () => void;
}

const OrgSync: React.FC<OrgSyncProps> = ({ onSyncSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError(null);
      setSuccess(null);
    }
  };

  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setError('Please select a JSON file first.');
      return;
    }

    setIsUploading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await auth.syncOrganizationsWithJson(selectedFile);
      
      // Construct a user-friendly success message from the result object
      const orgs = result.organizations || { created: 0, updated: 0 };
      const users = result.users || { created: 0, updated: 0 };
      const successMsg = `Sync successful! Orgs (Created: ${orgs.created}, Updated: ${orgs.updated}), Users (Created: ${users.created}, Updated: ${users.updated}).`;

      setSuccess(successMsg);
      setSelectedFile(null);
      // Notify parent component to refetch data
      onSyncSuccess();
    } catch (err: any) {
      console.error('Sync failed:', err);
      setError(err.response?.data?.detail || 'An unknown error occurred during synchronization.');
    } finally {
      setIsUploading(false);
    }
  }, [selectedFile, onSyncSuccess]);

  return (
    <Box sx={{ border: '1px dashed grey', p: 2, borderRadius: 1, mt: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        Sync with JSON
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Upload a JSON file to synchronize the entire organization chart and user list.
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Input
          type="file"
          onChange={handleFileChange}
          inputProps={{ accept: '.json' }}
          disableUnderline
        />
        <Button
          variant="contained"
          color="secondary"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
          startIcon={isUploading ? <CircularProgress size={20} color="inherit" /> : null}
        >
          {isUploading ? 'Syncing...' : 'Sync Now'}
        </Button>
      </Box>
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
    </Box>
  );
};

export default OrgSync;

import React, { useState } from 'react';
import { Box, Typography, List, ListItem, ListItemText, IconButton, TextField, Button, Select, MenuItem, FormControl, InputLabel, CircularProgress, Alert } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import type { ExternalAccount, ExternalAccountCreate } from '../../schemas';
import api from '../../services/api';

interface Props {
  accounts: ExternalAccount[];
  onAccountUpdate: () => void;
}

const ExternalAccountsManager: React.FC<Props> = ({ accounts, onAccountUpdate }) => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [provider, setProvider] = useState<'jira' | 'bitbucket'>('jira');
  const [accountId, setAccountId] = useState('');
  const [credentials, setCredentials] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async (id: number) => {
    if (window.confirm('정말로 이 계정 연동을 해제하시겠습니까?')) {
      try {
        await api.externalAccounts.deleteAccount(id);
        onAccountUpdate(); // Refresh the list
      } catch (err) {
        setError('계정 삭제에 실패했습니다.');
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const data: ExternalAccountCreate = { provider, account_id: accountId, credentials };
    try {
      await api.externalAccounts.createAccount(data);
      onAccountUpdate(); // Refresh the list
      // Reset form
      setShowAddForm(false);
      setProvider('jira');
      setAccountId('');
      setCredentials('');
    } catch (err) {
      setError('계정 추가에 실패했습니다. 입력 정보를 확인해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>외부 계정 연동 관리</Typography>
      {accounts.length === 0 && <Typography variant="body2" color="text.secondary">연동된 계정이 없습니다. 회고록을 생성하려면 계정을 추가하세요.</Typography>}
      <List dense>
        {accounts.map((acc) => (
          <ListItem
            key={acc.id}
            secondaryAction={
              <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(acc.id)}>
                <DeleteIcon />
              </IconButton>
            }
          >
            <ListItemText primary={acc.provider.toUpperCase()} secondary={acc.account_id} />
          </ListItem>
        ))}
      </List>

      <Button
        startIcon={<AddCircleOutlineIcon />}
        onClick={() => setShowAddForm(!showAddForm)}
        sx={{ mt: 1 }}
      >
        {showAddForm ? '취소' : '새 계정 추가'}
      </Button>

      {showAddForm && (
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <FormControl fullWidth margin="normal">
            <InputLabel>Provider</InputLabel>
            <Select
              value={provider}
              label="Provider"
              onChange={(e) => setProvider(e.target.value as 'jira' | 'bitbucket')}
            >
              <MenuItem value="jira">Jira</MenuItem>
              <MenuItem value="bitbucket">Bitbucket</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            margin="normal"
            label="계정 ID (이메일 또는 사용자명)"
            value={accountId}
            onChange={(e) => setAccountId(e.target.value)}
            required
          />
          <TextField
            fullWidth
            margin="normal"
            label="API 토큰 또는 인증 정보"
            type="password"
            value={credentials}
            onChange={(e) => setCredentials(e.target.value)}
            required
          />
          <Button type="submit" variant="contained" disabled={loading} sx={{ mt: 1 }}>
            {loading ? <CircularProgress size={24} /> : '연동하기'}
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default ExternalAccountsManager;

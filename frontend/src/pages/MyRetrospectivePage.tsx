import React, { useState, useEffect, useCallback } from 'react';
import { Box, Typography, Paper, CircularProgress, Alert } from '@mui/material';
import ExternalAccountsManager from '../components/retrospective/ExternalAccountsManager';
import RetrospectiveGenerator from '../components/retrospective/RetrospectiveGenerator';
import RetrospectiveEditor from '../components/retrospective/RetrospectiveEditor';
import RetrospectiveList from '../components/retrospective/RetrospectiveList';
import api from '../services/api';
import type { ExternalAccount, Retrospective, RetrospectiveCreate, RetrospectiveUpdate, GenerateRetrospectivePayload } from '../schemas';

const MyRetrospectivePage: React.FC = () => {
  // State Management
  const [accounts, setAccounts] = useState<ExternalAccount[]>([]);
  const [retrospectives, setRetrospectives] = useState<Retrospective[]>([]);
  const [selectedRetrospective, setSelectedRetrospective] = useState<Retrospective | null>(null);
  const [newDraftContent, setNewDraftContent] = useState<string | null>(null);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  // Data Fetching Callbacks
  const fetchAccounts = useCallback(async () => {
    try {
      const response = await api.externalAccounts.getAccounts();
      setAccounts(response.data);
    } catch (err) {
      setError('외부 계정 목록을 불러오는 데 실패했습니다.');
    }
  }, []);

  const fetchRetrospectives = useCallback(async () => {
    try {
      const response = await api.retrospectives.getList();
      setRetrospectives(response.data);
    } catch (err) {
      setError('회고록 목록을 불러오는 데 실패했습니다.');
    }
  }, []);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      await Promise.all([fetchAccounts(), fetchRetrospectives()]);
      setLoading(false);
    };
    loadData();
  }, [fetchAccounts, fetchRetrospectives]);

  // Event Handlers
  const handleGenerateDraft = async (payload: GenerateRetrospectivePayload) => {
    setGenerating(true);
    setError(null);
    try {
      const response = await api.retrospectives.generate(payload);
      setSelectedRetrospective(null); // Clear any selected retrospective
      setNewDraftContent(response.data.content);
    } catch (err) {
      setError('AI 회고록 초안 생성에 실패했습니다.');
      setNewDraftContent(null);
    } finally {
      setGenerating(false);
    }
  };

  const handleSaveRetrospective = async (data: RetrospectiveCreate | (RetrospectiveUpdate & { id?: number })) => {
    setError(null);
    try {
      if ('id' in data && data.id) {
        // Update existing
        await api.retrospectives.update(data.id, data as RetrospectiveUpdate);
      } else {
        // Create new
        await api.retrospectives.create(data as RetrospectiveCreate);
      }
      await fetchRetrospectives(); // Refresh list
      setSelectedRetrospective(null);
      setNewDraftContent(null);
    } catch (err) {
      setError('회고록 저장에 실패했습니다.');
    }
  };

  const handleDeleteRetrospective = async (id: number) => {
    setError(null);
    try {
      await api.retrospectives.delete(id);
      await fetchRetrospectives(); // Refresh list
      if (selectedRetrospective?.id === id) {
        setSelectedRetrospective(null);
      }
    } catch (err) {
      setError('회고록 삭제에 실패했습니다.');
    }
  };

  const handleSelectRetrospective = (retrospective: Retrospective | null) => {
    setSelectedRetrospective(retrospective);
    setNewDraftContent(null); // Clear draft when selecting an existing one
  };

  const handleAddNew = () => {
    setSelectedRetrospective(null);
    setNewDraftContent(''); // Start a blank new draft
  };

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        나의 성장 회고록
      </Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
        {/* Left Column */}
        <Box sx={{ width: { xs: '100%', md: '33.33%' } }}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <ExternalAccountsManager
              accounts={accounts}
              onAccountUpdate={fetchAccounts}
            />
          </Paper>
          <Paper sx={{ p: 2 }}>
            <RetrospectiveList
              retrospectives={retrospectives}
              onSelect={handleSelectRetrospective}
              onDelete={handleDeleteRetrospective}
              onAddNew={handleAddNew}
              selectedId={selectedRetrospective?.id}
            />
          </Paper>
        </Box>

        {/* Right Column */}
        <Box sx={{ width: { xs: '100%', md: '66.67%' } }}>
          <Paper sx={{ p: 2 }}>
            <RetrospectiveGenerator
              onGenerate={handleGenerateDraft}
              isGenerating={generating}
              hasAccounts={accounts.length > 0}
            />
            <Box sx={{ mt: 3 }}>
              <RetrospectiveEditor
                key={selectedRetrospective?.id || 'new'}
                retrospective={selectedRetrospective}
                draftContent={newDraftContent}
                onSave={handleSaveRetrospective}
              />
            </Box>
          </Paper>
        </Box>
      </Box>
    </Box>
  );
};

export default MyRetrospectivePage;

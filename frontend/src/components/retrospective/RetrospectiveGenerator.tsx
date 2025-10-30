import React, { useState } from 'react';
import { Box, Typography, Button, TextField, CircularProgress, Alert } from '@mui/material';
import type { GenerateRetrospectivePayload } from '../../schemas';

interface Props {
  onGenerate: (payload: GenerateRetrospectivePayload) => void;
  isGenerating: boolean;
  hasAccounts: boolean;
}

const RetrospectiveGenerator: React.FC<Props> = ({ onGenerate, isGenerating, hasAccounts }) => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!startDate || !endDate) {
      setError('시작일과 종료일을 모두 선택해주세요.');
      return;
    }
    setError('');
    onGenerate({ start_date: startDate, end_date: endDate });
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>AI 회고록 초안 생성</Typography>
      {!hasAccounts && (
        <Alert severity="warning">
          AI 초안을 생성하려면 먼저 외부 계정을 하나 이상 연동해야 합니다.
        </Alert>
      )}
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <TextField
          label="시작일"
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          InputLabelProps={{ shrink: true }}
          disabled={!hasAccounts || isGenerating}
        />
        <TextField
          label="종료일"
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          InputLabelProps={{ shrink: true }}
          disabled={!hasAccounts || isGenerating}
        />
      </Box>
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      <Button
        variant="contained"
        onClick={handleSubmit}
        disabled={!hasAccounts || isGenerating}
        sx={{ mt: 2 }}
      >
        {isGenerating ? <CircularProgress size={24} /> : 'AI 초안 생성하기'}
      </Button>
    </Box>
  );
};

export default RetrospectiveGenerator;

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
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError(null);
      setSuccess(null);
    }
  };

  const handleSelectFileClick = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setError('먼저 JSON 파일을 선택해주세요.');
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
      const successMsg = `동기화 성공! 조직 (생성: ${orgs.created}개, 업데이트: ${orgs.updated}개), 사용자 (생성: ${users.created}명, 업데이트: ${users.updated}명).`;

      setSuccess(successMsg);
      setSelectedFile(null);
      // Notify parent component to refetch data
      onSyncSuccess();
    } catch (err: any) {
      console.error('Sync failed:', err);
      setError(err.response?.data?.detail || '동기화 중 알 수 없는 오류가 발생했습니다.');
    } finally {
      setIsUploading(false);
    }
  }, [selectedFile, onSyncSuccess]);

  return (
    <Box sx={{ border: '1px dashed grey', p: 2, borderRadius: 1 }}>
      <Typography variant="h6" gutterBottom>
        JSON으로 동기화
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        JSON 파일을 업로드하여 전체 조직도와 사용자 목록을 동기화합니다.
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Button variant="outlined" onClick={handleSelectFileClick}>
          파일 선택
        </Button>
        <input
          type="file"
          accept=".json"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <Typography variant="body2" sx={{ flexGrow: 1 }}>
          {selectedFile ? selectedFile.name : '선택된 파일 없음'}
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
          startIcon={isUploading ? <CircularProgress size={20} color="inherit" /> : null}
        >
          {isUploading ? '동기화 중...' : '지금 동기화'}
        </Button>
      </Box>
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
    </Box>
  );
};

export default OrgSync;


import React, { useState, useEffect } from 'react';
import { Box, Typography, TextField, Button, CircularProgress } from '@mui/material';
import type { Retrospective, RetrospectiveCreate, RetrospectiveUpdate } from '../../schemas';

interface Props {
  retrospective: Retrospective | null;
  draftContent: string | null;
  onSave: (data: RetrospectiveCreate | (RetrospectiveUpdate & { id: number })) => void;
}

const RetrospectiveEditor: React.FC<Props> = ({ retrospective, draftContent, onSave }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (retrospective) {
      setTitle(retrospective.title);
      setContent(retrospective.content);
    } else if (draftContent !== null) {
      // New draft from AI
      setTitle('AI 생성 회고록 초안');
      setContent(draftContent);
    } else {
      // Blank new post
      setTitle('');
      setContent('');
    }
  }, [retrospective, draftContent]);

  const handleSave = async () => {
    setLoading(true);
    const data = {
      id: retrospective?.id,
      title,
      content,
    };
    // Type assertion is safe here because onSave handles create vs update
    await onSave(data as RetrospectiveCreate & { id: number });
    setLoading(false);
  };
  
  const isEditing = retrospective || draftContent !== null;

  if (!isEditing) {
      return (
        <Box sx={{ p: 3, textAlign: 'center', border: '1px dashed grey', borderRadius: 1 }}>
            <Typography color="text.secondary">
                왼쪽 목록에서 회고록을 선택하거나, 새로 작성 또는 AI 초안을 생성해주세요.
            </Typography>
        </Box>
      )
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        {retrospective ? '회고록 수정' : '새 회고록 작성'}
      </Typography>
      <TextField
        fullWidth
        label="제목"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        margin="normal"
      />
      <TextField
        fullWidth
        label="내용"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        margin="normal"
        multiline
        rows={15}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSave}
        disabled={loading || !title || !content}
        sx={{ mt: 2 }}
      >
        {loading ? <CircularProgress size={24} /> : (retrospective ? '수정 완료' : '저장하기')}
      </Button>
    </Box>
  );
};

export default RetrospectiveEditor;

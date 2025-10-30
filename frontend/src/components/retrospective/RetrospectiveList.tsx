import React from 'react';
import { Box, Typography, List, ListItem, ListItemButton, ListItemText, IconButton, Button } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import type { Retrospective } from '../../schemas';

interface Props {
  retrospectives: Retrospective[];
  onSelect: (retrospective: Retrospective) => void;
  onDelete: (id: number) => void;
  onAddNew: () => void;
  selectedId?: number | null;
}

const RetrospectiveList: React.FC<Props> = ({ retrospectives, onSelect, onDelete, onAddNew, selectedId }) => {
  
  const handleDeleteClick = (e: React.MouseEvent, id: number) => {
    e.stopPropagation(); // Prevent ListItemButton's onClick from firing
    if (window.confirm('정말로 이 회고록을 삭제하시겠습니까?')) {
      onDelete(id);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography variant="h6">내 회고록 목록</Typography>
        <Button size="small" startIcon={<AddIcon />} onClick={onAddNew}>
          새로 작성
        </Button>
      </Box>
      {retrospectives.length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          작성된 회고록이 없습니다. AI 초안을 생성하거나 새로 작성해보세요.
        </Typography>
      ) : (
        <List dense>
          {retrospectives.map((retro) => (
            <ListItem
              key={retro.id}
              disablePadding
              secondaryAction={
                <IconButton edge="end" aria-label="delete" onClick={(e) => handleDeleteClick(e, retro.id)}>
                  <DeleteIcon />
                </IconButton>
              }
            >
              <ListItemButton selected={selectedId === retro.id} onClick={() => onSelect(retro)}>
                <ListItemText
                  primary={retro.title}
                  secondary={`최종 수정: ${new Date(retro.updated_at || retro.created_at).toLocaleDateString()}`}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default RetrospectiveList;

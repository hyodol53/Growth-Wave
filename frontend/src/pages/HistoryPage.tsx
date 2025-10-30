// @ts-nocheck
import React, { useState, useEffect } from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Container,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import api from '../services/api';
import type { UserHistoryEntry, ProjectHistoryItem } from '../schemas/user';

const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<Record<string, UserHistoryEntry> | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const historyRes = await api.users.getUserHistory();
        setHistory(historyRes.data.history);
      } catch (err) {
        setError('Failed to load history data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const renderProjectItem = (project: ProjectHistoryItem) => (
    <ListItem key={project.project_id}>
      <ListItemText
        primary={project.project_name}
        secondary={`참여 비중: ${project.participation_weight}%`}
      />
    </ListItem>
  );

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  const sortedPeriods = history ? Object.keys(history).sort((a, b) => b.localeCompare(a)) : [];

  if (sortedPeriods.length === 0) {
    return <Typography>평가 이력이 없습니다.</Typography>;
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          내 평가 이력
        </Typography>
        {sortedPeriods.map((period) => {
          const entry = history![period as keyof typeof history];
          const finalEval = entry.final_evaluation;

          return (
            <Accordion key={period} defaultExpanded={period === sortedPeriods[0]}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">{entry.evaluation_period}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6} sx={{ display: 'flex' }}>
                    <Paper sx={{ p: 2, width: '100%' }}>
                      <Typography variant="h6" gutterBottom>평가 결과</Typography>
                      <Typography variant="body1">
                        <strong>최종 등급:</strong> {finalEval?.grade || '등급 없음'}
                      </Typography>
                      {finalEval && (
                         <>
                          <Divider sx={{ my: 1 }} />
                          <Typography variant="body2">PM 평가 점수: {finalEval.pm_score.toFixed(2)}</Typography>
                         </>
                       )}
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={6} sx={{ display: 'flex' }}>
                    <Paper sx={{ p: 2, width: '100%' }}>
                      <Typography variant="h6" gutterBottom>프로젝트</Typography>
                      <List dense>
                        {entry.projects.length > 0 ? (
                          entry.projects.map(renderProjectItem)
                        ) : (
                          <ListItem><ListItemText primary="이 기간에 참여한 프로젝트가 없습니다." /></ListItem>
                        )}
                      </List>
                    </Paper>
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          );
        })}
      </Box>
    </Container>
  );
};

export default HistoryPage;

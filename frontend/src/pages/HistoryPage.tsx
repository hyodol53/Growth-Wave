import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Container, Accordion, AccordionSummary, AccordionDetails,
  CircularProgress, Alert, Paper, List, ListItem, ListItemText, Divider
} from '@mui/material';
import { GridLegacy as Grid } from '@mui/material';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { getUserHistory } from '../services/api';
import type { UserHistoryResponse, ProjectHistoryItem } from '../schemas/user';
import { AxiosError } from 'axios';

const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<UserHistoryResponse['history'] | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const historyRes = await getUserHistory();
        setHistory(historyRes.data.history);
      } catch (err) {
        if (err instanceof AxiosError) {
          setError(err.response?.data?.detail || '이력 데이터를 불러오는데 실패했습니다.');
        } else {
          setError('예상치 못한 오류가 발생했습니다.');
        }
        console.error(err);
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
          const entry = history![period];
          const finalEval = entry.final_evaluation;

          return (
            <Accordion key={period} defaultExpanded={period === sortedPeriods[0]}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">{period}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
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
                  <Grid xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
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
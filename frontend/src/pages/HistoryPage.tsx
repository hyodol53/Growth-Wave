import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Container, Accordion, AccordionSummary, AccordionDetails,
  CircularProgress, Alert, Paper, List, ListItem, ListItemText, Divider
} from '@mui/material';
import { GridLegacy as Grid } from '@mui/material';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { getUserHistory, auth } from '../services/api';
import type { User, UserHistoryResponse, ProjectHistoryItem } from '../schemas/user';
import { UserRole } from '../schemas/user';
import { AxiosError } from 'axios';

const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<UserHistoryResponse | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [historyRes, userRes] = await Promise.all([
          getUserHistory(),
          auth.getCurrentUser()
        ]);
        setHistory(historyRes.data);
        setCurrentUser(userRes);
      } catch (err) {
        if (err instanceof AxiosError) {
          setError(err.response?.data?.detail || 'Failed to fetch history data.');
        } else {
          setError('An unexpected error occurred.');
        }
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const isManager = currentUser?.role === UserRole.ADMIN || currentUser?.role === UserRole.DEPT_HEAD;

  const renderProjectItem = (project: ProjectHistoryItem) => (
    <ListItem key={project.project_id}>
      <ListItemText
        primary={project.project_name}
        secondary={`Participation: ${project.participation_weight}%`}
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
    return <Typography>No evaluation history found.</Typography>;
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          My Evaluation History
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
                      <Typography variant="h6" gutterBottom>Evaluation Result</Typography>
                      <Typography variant="body1">
                        <strong>Final Grade:</strong> {finalEval?.grade || 'Not Graded'}
                      </Typography>
                      {isManager && finalEval && (
                         <>
                           <Divider sx={{ my: 1 }} />
                           <Typography variant="body2">Peer Score: {finalEval.peer_score.toFixed(2)}</Typography>
                           <Typography variant="body2">PM Score: {finalEval.pm_score.toFixed(2)}</Typography>
                           <Typography variant="body2">Qualitative Score: {finalEval.qualitative_score.toFixed(2)}</Typography>
                           <Typography variant="body2" sx={{fontWeight: 'bold'}}>Final Score: {finalEval.final_score.toFixed(2)}</Typography>
                         </>
                      )}
                       {!isManager && finalEval && (
                         <>
                          <Divider sx={{ my: 1 }} />
                          <Typography variant="body2">PM Score: {finalEval.pm_score.toFixed(2)}</Typography>
                         </>
                       )}
                    </Paper>
                  </Grid>
                  <Grid xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="h6" gutterBottom>Projects</Typography>
                      <List dense>
                        {entry.projects.length > 0 ? (
                          entry.projects.map(renderProjectItem)
                        ) : (
                          <ListItem><ListItemText primary="No projects in this period." /></ListItem>
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
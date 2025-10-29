
import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Card, CardContent, CardActions, Button } from '@mui/material';
import { GridLegacy as Grid } from '@mui/material';
import * as api from '../services/api';
import type { User, ProjectHistoryItem } from '../schemas/user';
import type { ProjectMemberDetails } from '../schemas/project';
import type { PeerEvaluationCreate, PmEvaluationCreate, QualitativeEvaluationCreate } from '../schemas/evaluation';
import QualitativeEvaluationDialog from '../components/QualitativeEvaluationDialog';
import PmEvaluationDialog from '../components/PmEvaluationDialog';
import PeerEvaluationDialog from '../components/PeerEvaluationDialog';

interface EvaluationTask {
    type: 'PEER' | 'PM' | 'QUALITATIVE';
    title: string;
    description: string;
    targetCount: number;
    action: () => void;
}

// Helper type for project data with members
interface ProjectWithMembers {
    id: number;
    name: string;
    members: ProjectMemberDetails[];
}

const MyEvaluationsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<EvaluationTask[]>([]);
  
  // Data from API
  const [subordinates, setSubordinates] = useState<User[]>([]);
  // const [projectsWithMembers, setProjectsWithMembers] = useState<ProjectWithMembers[]>([]);

  // Dialog states
  const [qualitativeOpen, setQualitativeOpen] = useState(false);
  const [pmOpen, setPmOpen] = useState(false);
  const [peerOpen, setPeerOpen] = useState(false);
  
  // Data for dialogs
  const [activeProject, setActiveProject] = useState<ProjectWithMembers | null>(null);

  useEffect(() => {
    const fetchInitialData = async () => {
        try {
            setLoading(true);
            const userRes = await api.auth.getCurrentUser();
            setCurrentUser(userRes);

            const newTasks: EvaluationTask[] = [];

            // 1. Fetch subordinates for Qualitative Evaluation
            if (userRes.role === 'team_lead' || userRes.role === 'dept_head') {
                const subRes = await api.getMySubordinates();
                const subordinatesData = subRes.data;
                setSubordinates(subordinatesData);
                if (subordinatesData.length > 0) {
                    newTasks.push({
                        type: 'QUALITATIVE',
                        title: '정성평가',
                        description: `내 부서/팀원 ${subordinatesData.length}명에 대한 정성평가를 진행합니다.`,
                        targetCount: subordinatesData.length,
                        action: () => setQualitativeOpen(true)
                    });
                }
            }

            // 2. Fetch user's projects and their members for Peer and PM evaluations
            const historyRes = await api.getUserHistory();
            const myProjects = historyRes.data;
            const allProjects = myProjects.history.flatMap(entry => entry.projects);

            const projectsData: ProjectWithMembers[] = await Promise.all(
                allProjects.map(async (proj: ProjectHistoryItem) => {
                    const membersRes = await api.getProjectMembers(proj.project_id);
                    return {
                        id: proj.project_id,
                        name: proj.project_name,
                        members: membersRes.data,
                    };
                })
            );
            // setProjectsWithMembers(projectsData);

            // 3. Create evaluation tasks based on fetched project data
            for (const project of projectsData) {
                const meAsMember = project.members.find(m => m.user_id === userRes.id);
                if (!meAsMember) continue;

                // Task for Peer Evaluation
                const peerEvaluatees = project.members.filter(m => m.user_id !== userRes.id);
                if (peerEvaluatees.length > 0) {
                    newTasks.push({
                        type: 'PEER',
                        title: `동료평가 (${project.name})`,
                        description: `${project.name} 동료 ${peerEvaluatees.length}명에 대한 동료평가를 진행합니다.`,
                        targetCount: peerEvaluatees.length,
                        action: () => { setActiveProject(project); setPeerOpen(true); }
                    });
                }

                // Task for PM Evaluation (if user is PM of this project)
                if (meAsMember.is_pm) {
                    const pmEvaluatees = project.members.filter(m => m.user_id !== userRes.id);
                     if (pmEvaluatees.length > 0) {
                        newTasks.push({
                            type: 'PM',
                            title: `PM 평가 (${project.name})`,
                            description: `${project.name} 멤버 ${pmEvaluatees.length}명에 대한 PM평가를 진행합니다.`,
                            targetCount: pmEvaluatees.length,
                            action: () => { setActiveProject(project); setPmOpen(true); }
                        });
                    }
                }
            }

            setTasks(newTasks);

        } catch (error) {
            console.error("Failed to fetch initial data", error);
        } finally {
            setLoading(false);
        }
    };

    fetchInitialData();
  }, []);

  const handleSubmitQualitative = async (data: QualitativeEvaluationCreate) => {
    try {
        await api.createQualitativeEvaluations(data);
        alert('정성평가가 성공적으로 제출되었습니다.');
        setQualitativeOpen(false);
    } catch (err) {
        alert('정성평가 제출에 실패했습니다.');
        console.error(err);
    }
  };

  const handleSubmitPm = async (data: PmEvaluationCreate) => {
    try {
        await api.createPmEvaluations(data);
        alert('PM 평가가 성공적으로 제출되었습니다.');
        setPmOpen(false);
    } catch (err) {
        alert('PM 평가 제출에 실패했습니다.');
        console.error(err);
    }
  };

  const handleSubmitPeer = async (data: PeerEvaluationCreate) => {
    try {
        await api.createPeerEvaluations(data);
        alert('동료평가가 성공적으로 제출되었습니다.');
        setPeerOpen(false);
    } catch (err) {
        alert('동료평가 제출에 실패했습니다.');
        console.error(err);
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom>내 평가 (2025-H1)</Typography>
      <Typography variant="subtitle1" gutterBottom>진행해야 할 평가 목록</Typography>
      
      {loading ? (
        <CircularProgress />
      ) : (
        <Grid container spacing={3} sx={{ mt: 2 }}>
            {tasks.length > 0 ? tasks.map((task, index) => (
                <Grid xs={12} md={6} lg={4} key={index}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6">{task.title}</Typography>
                            <Typography color="text.secondary" sx={{mt: 1}}>{task.description}</Typography>
                        </CardContent>
                        <CardActions>
                            <Button size="small" variant="contained" onClick={task.action}>평가 시작하기</Button>
                        </CardActions>
                    </Card>
                </Grid>
            )) : (
                <Grid xs={12}>
                    <Typography sx={{p: 3}}>진행해야 할 평가가 없습니다.</Typography>
                </Grid>
            )}
        </Grid>
      )}

      {/* Dialogs */}
      <QualitativeEvaluationDialog 
        open={qualitativeOpen}
        onClose={() => setQualitativeOpen(false)}
        onSubmit={handleSubmitQualitative}
        evaluatees={subordinates}
      />
      {activeProject && currentUser && (
          <>
            <PmEvaluationDialog 
                open={pmOpen}
                onClose={() => setPmOpen(false)}
                onSubmit={handleSubmitPm}
                project={activeProject}
                evaluatees={activeProject.members.filter(m => m.user_id !== currentUser.id)}
            />
            <PeerEvaluationDialog
                open={peerOpen}
                onClose={() => setPeerOpen(false)}
                onSubmit={handleSubmitPeer}
                project={activeProject}
                evaluatees={activeProject.members.filter(m => m.user_id !== currentUser.id)}
            />
          </>
      )}
    </Box>
  );
};

export default MyEvaluationsPage;

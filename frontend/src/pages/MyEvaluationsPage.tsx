import React, { useState, useEffect } from 'react';
import type { SelectChangeEvent } from '@mui/material';
import { Box, Typography, CircularProgress, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import * as api from '../services/api';
import type { User } from '../schemas/user';
import type { MyEvaluationTask, PeerEvaluationData, PmEvaluationData, PeerEvaluationSubmit, PmEvaluationSubmit } from '../schemas/evaluation';

import QualitativeEvaluationCard from '../components/QualitativeEvaluationCard';
import PeerEvaluationGrid from '../components/PeerEvaluationGrid';
import PmEvaluationGrid from '../components/PmEvaluationGrid';


const MyEvaluationsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [evaluationTasks, setEvaluationTasks] = useState<MyEvaluationTask[]>([]);
  const [selectedProject, setSelectedProject] = useState<MyEvaluationTask | null>(null);
  
  const [peerEvaluationData, setPeerEvaluationData] = useState<PeerEvaluationData | null>(null);
  const [pmEvaluationData, setPmEvaluationData] = useState<PmEvaluationData | null>(null);
  const [isProjectDataLoading, setIsProjectDataLoading] = useState(false);


  useEffect(() => {
    const fetchInitialData = async () => {
        try {
            setLoading(true);
            const userRes = await api.auth.getCurrentUser();
            setCurrentUser(userRes);

            const tasksRes = await api.evaluations.getMyTasks();
            setEvaluationTasks(tasksRes.data);

        } catch (error) {
            console.error("Failed to fetch initial data", error);
            alert('초기 데이터 로딩에 실패했습니다.');
        } finally {
            setLoading(false);
        }
    };

    fetchInitialData();
  }, []);

  const fetchProjectEvaluationData = async (project: MyEvaluationTask) => {
    setIsProjectDataLoading(true);
    setPeerEvaluationData(null);
    setPmEvaluationData(null);
    try {
        if (project.user_role_in_project === 'MEMBER') {
            const res = await api.evaluations.getPeerEvaluations(project.project_id);
            setPeerEvaluationData(res.data);
        } else if (project.user_role_in_project === 'PM') {
            const res = await api.evaluations.getPmEvaluations(project.project_id);
            setPmEvaluationData(res.data);
        }
    } catch (error) {
        console.error(`Failed to fetch evaluation data for project ${project.project_id}`, error);
        alert(`${project.project_name} 평가 데이터 로딩에 실패했습니다.`);
    } finally {
        setIsProjectDataLoading(false);
    }
  };

  const handleProjectChange = async (event: SelectChangeEvent<number>) => {
    const projectId = event.target.value as number;
    const project = evaluationTasks.find(t => t.project_id === projectId) || null;
    setSelectedProject(project);
    if (project) {
        await fetchProjectEvaluationData(project);
    }
  };

  const handlePeerSubmit = async (formData: PeerEvaluationSubmit) => {
    try {
      await api.evaluations.submitPeerEvaluations(formData);
      alert('동료평가가 성공적으로 제출되었습니다.');
      if (selectedProject) {
        await fetchProjectEvaluationData(selectedProject);
      }
    } catch (error) {
      console.error('Failed to submit peer evaluations', error);
      alert('동료평가 제출에 실패했습니다.');
    }
  };

  const handlePmSubmit = async (formData: PmEvaluationSubmit) => {
    try {
      await api.evaluations.submitPmEvaluations(formData);
      alert('PM 평가가 성공적으로 제출되었습니다.');
       if (selectedProject) {
        await fetchProjectEvaluationData(selectedProject);
      }
    } catch (error) {
      console.error('Failed to submit PM evaluations', error);
      alert('PM 평가 제출에 실패했습니다.');
    }
  };


  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom>내 평가 (2025-H1)</Typography>
      
      {loading ? (
        <CircularProgress />
      ) : (
        <>
            {(currentUser?.role === 'team_lead' || currentUser?.role === 'dept_head') && (
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h5" gutterBottom>정성평가</Typography>
                    <QualitativeEvaluationCard />
                </Box>
            )}

            <Box>
                <Typography variant="h5" gutterBottom>프로젝트 평가</Typography>
                
                <FormControl fullWidth sx={{mb: 3}}>
                    <InputLabel id="project-select-label">프로젝트 선택</InputLabel>
                    <Select
                        labelId="project-select-label"
                        value={selectedProject?.project_id || ''}
                        label="프로젝트 선택"
                        onChange={handleProjectChange}
                        disabled={evaluationTasks.length === 0}
                    >
                        {evaluationTasks.map((task) => (
                            <MenuItem key={task.project_id} value={task.project_id}>
                                {task.project_name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {isProjectDataLoading ? <CircularProgress /> : (
                    <>
                        {peerEvaluationData && <PeerEvaluationGrid data={peerEvaluationData} onSubmit={handlePeerSubmit} />}
                        {pmEvaluationData && <PmEvaluationGrid data={pmEvaluationData} onSubmit={handlePmSubmit} />}
                    </>
                )}
            </Box>
        </>
      )}
    </Box>
  );
};

export default MyEvaluationsPage;

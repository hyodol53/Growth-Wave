
import React, { useState, useEffect } from 'react';
import { Box, Typography, Tabs, Tab, Button, CircularProgress } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import type { GridColDef } from '@mui/x-data-grid';
import * as api from '../../services/api';
import type { EvaluationPeriod, EvaluationPeriodCreate, EvaluationPeriodUpdate, DepartmentGradeRatio, DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate, EvaluationWeight, EvaluationWeightCreate, EvaluationWeightUpdate } from '../../schemas/evaluation';
import EvaluationPeriodDialog from '../../components/Admin/EvaluationPeriodDialog';
import DepartmentGradeRatioDialog from '../../components/Admin/DepartmentGradeRatioDialog';
import EvaluationWeightDialog from '../../components/Admin/EvaluationWeightDialog';

function TabPanel(props: { children?: React.ReactNode; index: number; value: number; }) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const EvaluationSettingsPage: React.FC = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  
  // Evaluation Periods
  const [periods, setPeriods] = useState<EvaluationPeriod[]>([]);
  const [periodDialogOpen, setPeriodDialogOpen] = useState(false);
  const [editingPeriod, setEditingPeriod] = useState<EvaluationPeriod | null>(null);

  // Department Grade Ratios
  const [ratios, setRatios] = useState<DepartmentGradeRatio[]>([]);
  const [ratioDialogOpen, setRatioDialogOpen] = useState(false);
  const [editingRatio, setEditingRatio] = useState<DepartmentGradeRatio | null>(null);

  // Evaluation Weights
  const [weights, setWeights] = useState<EvaluationWeight[]>([]);
  const [weightDialogOpen, setWeightDialogOpen] = useState(false);
  const [editingWeight, setEditingWeight] = useState<EvaluationWeight | null>(null);

  const fetchPeriods = async () => {
    try {
      const response = await api.getEvaluationPeriods();
      setPeriods(response.data);
    } catch (error) {
      console.error("Failed to fetch evaluation periods", error);
    }
  };

  const fetchRatios = async () => {
    try {
      const response = await api.getDepartmentGradeRatios();
      setRatios(response.data);
    } catch (error) {
      console.error("Failed to fetch department grade ratios", error);
    }
  };

  const fetchWeights = async () => {
    try {
      const response = await api.getEvaluationWeights();
      setWeights(response.data);
    } catch (error) {
      console.error("Failed to fetch evaluation weights", error);
    }
  };

  useEffect(() => {
    setLoading(true);
    Promise.all([fetchPeriods(), fetchRatios(), fetchWeights()]).finally(() => setLoading(false));
  }, []);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
  };

  // Period Handlers
  const handleAddNewPeriod = () => { setEditingPeriod(null); setPeriodDialogOpen(true); };
  const handleEditPeriod = (period: EvaluationPeriod) => { setEditingPeriod(period); setPeriodDialogOpen(true); };
  const handleDeletePeriod = async (id: number) => {
    if (window.confirm('이 평가 기간을 정말로 삭제하시겠습니까?')) {
      try {
        await api.deleteEvaluationPeriod(id);
        fetchPeriods();
      } catch (error) { console.error("Failed to delete evaluation period", error); alert('평가 기간 삭제에 실패했습니다.'); }
    }
  };
  const handleSavePeriod = async (data: EvaluationPeriodCreate | EvaluationPeriodUpdate) => {
    try {
      if (editingPeriod) {
        await api.updateEvaluationPeriod(editingPeriod.id, data as EvaluationPeriodUpdate);
      } else {
        await api.createEvaluationPeriod(data as EvaluationPeriodCreate);
      }
      fetchPeriods();
      setPeriodDialogOpen(false);
    } catch (error) { console.error("Failed to save evaluation period", error); alert('평가 기간 저장에 실패했습니다.'); }
  };

  // Ratio Handlers
  const handleAddNewRatio = () => { setEditingRatio(null); setRatioDialogOpen(true); };
  const handleEditRatio = (ratio: DepartmentGradeRatio) => { setEditingRatio(ratio); setRatioDialogOpen(true); };
  const handleDeleteRatio = async (id: number) => {
    if (window.confirm('이 등급 비율을 정말로 삭제하시겠습니까?')) {
      try {
        await api.deleteDepartmentGradeRatio(id);
        fetchRatios();
      } catch (error) { console.error("Failed to delete grade ratio", error); alert('등급 비율 삭제에 실패했습니다.'); }
    }
  };
  const handleSaveRatio = async (data: DepartmentGradeRatioCreate | DepartmentGradeRatioUpdate) => {
    try {
      if (editingRatio) {
        await api.updateDepartmentGradeRatio(editingRatio.id, data as DepartmentGradeRatioUpdate);
      } else {
        await api.createDepartmentGradeRatio(data as DepartmentGradeRatioCreate);
      }
      fetchRatios();
      setRatioDialogOpen(false);
    } catch (error) { console.error("Failed to save grade ratio", error); alert('등급 비율 저장에 실패했습니다.'); }
  };

  // Weight Handlers
  const handleAddNewWeight = () => { setEditingWeight(null); setWeightDialogOpen(true); };
  const handleEditWeight = (weight: EvaluationWeight) => { setEditingWeight(weight); setWeightDialogOpen(true); };
  const handleDeleteWeight = async (id: number) => {
    if (window.confirm('이 평가 가중치를 정말로 삭제하시겠습니까?')) {
      try {
        await api.deleteEvaluationWeight(id);
        fetchWeights();
      } catch (error) { console.error("Failed to delete evaluation weight", error); alert('평가 가중치 삭제에 실패했습니다.'); }
    }
  };
  const handleSaveWeight = async (data: EvaluationWeightCreate | EvaluationWeightUpdate) => {
    try {
      if (editingWeight) {
        await api.updateEvaluationWeight(editingWeight.id, data as EvaluationWeightUpdate);
      } else {
        await api.createEvaluationWeight(data as EvaluationWeightCreate);
      }
      fetchWeights();
      setWeightDialogOpen(false);
    } catch (error) { console.error("Failed to save evaluation weight", error); alert('평가 가중치 저장에 실패했습니다.'); }
  };

  const periodColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'name', headerName: '기간 이름', width: 150 },
    { field: 'start_date', headerName: '시작일', width: 150, type: 'date', valueGetter: (value) => value ? new Date(value) : null },
    { field: 'end_date', headerName: '종료일', width: 150, type: 'date', valueGetter: (value) => value ? new Date(value) : null },
    { field: 'is_active', headerName: '활성', width: 120, type: 'boolean' },
    {
      field: 'actions',
      headerName: '작업',
      width: 150,
      renderCell: (params) => (
        <>
          <Button size="small" onClick={() => handleEditPeriod(params.row)}>수정</Button>
          <Button size="small" color="secondary" onClick={() => handleDeletePeriod(params.id as number)}>삭제</Button>
        </>
      ),
    },
  ];

  const ratioColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'department_grade', headerName: '부서 등급', width: 120 },
    { field: 's_ratio', headerName: 'S-비율 (%)', width: 120, type: 'number' },
    { field: 'a_ratio', headerName: 'A-비율 (%)', width: 120, type: 'number' },
    { field: 'b_ratio', headerName: 'B-비율 (%)', width: 120, type: 'number' },
    {
      field: 'actions',
      headerName: '작업',
      width: 150,
      renderCell: (params) => (
        <>
          <Button size="small" onClick={() => handleEditRatio(params.row)}>수정</Button>
          <Button size="small" color="secondary" onClick={() => handleDeleteRatio(params.id as number)}>삭제</Button>
        </>
      ),
    },
  ];

  const weightColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'user_role', headerName: '사용자 역할', width: 150 },
    { field: 'item', headerName: '평가 항목', width: 200 },
    { field: 'weight', headerName: '가중치 (%)', width: 120, type: 'number' },
    {
      field: 'actions',
      headerName: '작업',
      width: 150,
      renderCell: (params) => (
        <>
          <Button size="small" onClick={() => handleEditWeight(params.row)}>수정</Button>
          <Button size="small" color="secondary" onClick={() => handleDeleteWeight(params.id as number)}>삭제</Button>
        </>
      ),
    },
  ];

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom>평가 설정</Typography>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabIndex} onChange={handleTabChange} aria-label="evaluation settings tabs">
          <Tab label="평가 기간" />
          <Tab label="등급 비율" />
          <Tab label="평가 가중치" />
        </Tabs>
      </Box>

      {loading ? <CircularProgress sx={{mt: 3}}/> : (
        <>
          <TabPanel value={tabIndex} index={0}>
            <Box sx={{ mb: 2 }}>
                <Button variant="contained" onClick={handleAddNewPeriod}>새 기간 추가</Button>
            </Box>
            <Box sx={{ height: 600, width: '100%' }}>
              <DataGrid 
                rows={periods} 
                columns={periodColumns} 
                initialState={{
                  pagination: {
                    paginationModel: { pageSize: 10 },
                  },
                }}
                pageSizeOptions={[10]} 
                checkboxSelection 
                disableRowSelectionOnClick 
              />
            </Box>
          </TabPanel>
          <TabPanel value={tabIndex} index={1}>
            <Box sx={{ mb: 2 }}>
                <Button variant="contained" onClick={handleAddNewRatio}>새 비율 추가</Button>
            </Box>
            <Box sx={{ height: 600, width: '100%' }}>
              <DataGrid 
                rows={ratios} 
                columns={ratioColumns} 
                initialState={{
                  pagination: {
                    paginationModel: { pageSize: 10 },
                  },
                }}
                pageSizeOptions={[10]} 
                checkboxSelection 
                disableRowSelectionOnClick 
              />
            </Box>
          </TabPanel>
          <TabPanel value={tabIndex} index={2}>
            <Box sx={{ mb: 2 }}>
                <Button variant="contained" onClick={handleAddNewWeight}>새 가중치 추가</Button>
            </Box>
            <Box sx={{ height: 600, width: '100%' }}>
              <DataGrid 
                rows={weights} 
                columns={weightColumns} 
                initialState={{
                  pagination: {
                    paginationModel: { pageSize: 10 },
                  },
                }}
                pageSizeOptions={[10]} 
                checkboxSelection 
                disableRowSelectionOnClick 
              />
            </Box>
          </TabPanel>
        </>
      )}
      <EvaluationPeriodDialog 
        open={periodDialogOpen} 
        onClose={() => setPeriodDialogOpen(false)} 
        onSave={handleSavePeriod} 
        period={editingPeriod}
      />
      <DepartmentGradeRatioDialog
        open={ratioDialogOpen}
        onClose={() => setRatioDialogOpen(false)}
        onSave={handleSaveRatio}
        ratio={editingRatio}
      />
      <EvaluationWeightDialog
        open={weightDialogOpen}
        onClose={() => setWeightDialogOpen(false)}
        onSave={handleSaveWeight}
        weight={editingWeight}
      />
    </Box>
  );
};

export default EvaluationSettingsPage;

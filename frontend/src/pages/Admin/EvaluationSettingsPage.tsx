
import React, { useState, useEffect } from 'react';
import { Box, Typography, Tabs, Tab, Button, CircularProgress } from '@mui/material';
import { DataGrid, GridColDef, GridRowsProp } from '@mui/x-data-grid';
import * as api from '../../services/api';
import { EvaluationPeriod, EvaluationPeriodCreate, EvaluationPeriodUpdate, DepartmentGradeRatio, DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate, EvaluationWeight, EvaluationWeightCreate, EvaluationWeightUpdate } from '../../schemas/evaluation';
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
  const [periods, setPeriods] = useState<GridRowsProp>([]);
  const [periodDialogOpen, setPeriodDialogOpen] = useState(false);
  const [editingPeriod, setEditingPeriod] = useState<EvaluationPeriod | null>(null);

  // Department Grade Ratios
  const [ratios, setRatios] = useState<GridRowsProp>([]);
  const [ratioDialogOpen, setRatioDialogOpen] = useState(false);
  const [editingRatio, setEditingRatio] = useState<DepartmentGradeRatio | null>(null);

  // Evaluation Weights
  const [weights, setWeights] = useState<GridRowsProp>([]);
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

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
  };

  // Period Handlers
  const handleAddNewPeriod = () => { setEditingPeriod(null); setPeriodDialogOpen(true); };
  const handleEditPeriod = (period: EvaluationPeriod) => { setEditingPeriod(period); setPeriodDialogOpen(true); };
  const handleDeletePeriod = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this evaluation period?')) {
      try {
        await api.deleteEvaluationPeriod(id);
        fetchPeriods();
      } catch (error) { console.error("Failed to delete evaluation period", error); alert('Failed to delete evaluation period'); }
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
    } catch (error) { console.error("Failed to save evaluation period", error); alert('Failed to save evaluation period'); }
  };

  // Ratio Handlers
  const handleAddNewRatio = () => { setEditingRatio(null); setRatioDialogOpen(true); };
  const handleEditRatio = (ratio: DepartmentGradeRatio) => { setEditingRatio(ratio); setRatioDialogOpen(true); };
  const handleDeleteRatio = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this grade ratio?')) {
      try {
        await api.deleteDepartmentGradeRatio(id);
        fetchRatios();
      } catch (error) { console.error("Failed to delete grade ratio", error); alert('Failed to delete grade ratio'); }
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
    } catch (error) { console.error("Failed to save grade ratio", error); alert('Failed to save grade ratio'); }
  };

  // Weight Handlers
  const handleAddNewWeight = () => { setEditingWeight(null); setWeightDialogOpen(true); };
  const handleEditWeight = (weight: EvaluationWeight) => { setEditingWeight(weight); setWeightDialogOpen(true); };
  const handleDeleteWeight = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this evaluation weight?')) {
      try {
        await api.deleteEvaluationWeight(id);
        fetchWeights();
      } catch (error) { console.error("Failed to delete evaluation weight", error); alert('Failed to delete evaluation weight'); }
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
    } catch (error) { console.error("Failed to save evaluation weight", error); alert('Failed to save evaluation weight'); }
  };

  const periodColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'name', headerName: 'Period Name', width: 150 },
    { field: 'start_date', headerName: 'Start Date', width: 150, type: 'date', valueGetter: (params) => new Date(params.value) },
    { field: 'end_date', headerName: 'End Date', width: 150, type: 'date', valueGetter: (params) => new Date(params.value) },
    { field: 'is_active', headerName: 'Active', width: 120, type: 'boolean' },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <>
          <Button size="small" onClick={() => handleEditPeriod(params.row)}>Edit</Button>
          <Button size="small" color="secondary" onClick={() => handleDeletePeriod(params.id as number)}>Delete</Button>
        </>
      ),
    },
  ];

  const ratioColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'department_grade', headerName: 'Dept. Grade', width: 120 },
    { field: 's_ratio', headerName: 'S-Ratio (%)', width: 120, type: 'number' },
    { field: 'a_ratio', headerName: 'A-Ratio (%)', width: 120, type: 'number' },
    { field: 'b_ratio', headerName: 'B-Ratio (%)', width: 120, type: 'number' },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <>
          <Button size="small" onClick={() => handleEditRatio(params.row)}>Edit</Button>
          <Button size="small" color="secondary" onClick={() => handleDeleteRatio(params.id as number)}>Delete</Button>
        </>
      ),
    },
  ];

  const weightColumns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'user_role', headerName: 'User Role', width: 150 },
    { field: 'item', headerName: 'Evaluation Item', width: 200 },
    { field: 'weight', headerName: 'Weight (%)', width: 120, type: 'number' },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <>
          <Button size="small" onClick={() => handleEditWeight(params.row)}>Edit</Button>
          <Button size="small" color="secondary" onClick={() => handleDeleteWeight(params.id as number)}>Delete</Button>
        </>
      ),
    },
  ];

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom>Evaluation Settings</Typography>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabIndex} onChange={handleTabChange} aria-label="evaluation settings tabs">
          <Tab label="Evaluation Periods" />
          <Tab label="Grade Ratios" />
          <Tab label="Evaluation Weights" />
        </Tabs>
      </Box>

      {loading ? <CircularProgress sx={{mt: 3}}/> : (
        <>
          <TabPanel value={tabIndex} index={0}>
            <Box sx={{ mb: 2 }}>
                <Button variant="contained" onClick={handleAddNewPeriod}>Add New Period</Button>
            </Box>
            <Box sx={{ height: 600, width: '100%' }}>
              <DataGrid rows={periods} columns={periodColumns} pageSize={10} rowsPerPageOptions={[10]} checkboxSelection disableSelectionOnClick />
            </Box>
          </TabPanel>
          <TabPanel value={tabIndex} index={1}>
            <Box sx={{ mb: 2 }}>
                <Button variant="contained" onClick={handleAddNewRatio}>Add New Ratio</Button>
            </Box>
            <Box sx={{ height: 600, width: '100%' }}>
              <DataGrid rows={ratios} columns={ratioColumns} pageSize={10} rowsPerPageOptions={[10]} checkboxSelection disableSelectionOnClick />
            </Box>
          </TabPanel>
          <TabPanel value={tabIndex} index={2}>
            <Box sx={{ mb: 2 }}>
                <Button variant="contained" onClick={handleAddNewWeight}>Add New Weight</Button>
            </Box>
            <Box sx={{ height: 600, width: '100%' }}>
              <DataGrid rows={weights} columns={weightColumns} pageSize={10} rowsPerPageOptions={[10]} checkboxSelection disableSelectionOnClick />
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

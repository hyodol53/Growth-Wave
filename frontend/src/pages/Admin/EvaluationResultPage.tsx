import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
} from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import type { GridColDef } from '@mui/x-data-grid';
import VisibilityIcon from '@mui/icons-material/Visibility';
import api from '../../services/api';
import type { EvaluationPeriod, EvaluatedUser, DetailedEvaluationResult } from '../../schemas/evaluation';
import EvaluationDetailDialog from '../../components/Admin/EvaluationDetailDialog';

const EvaluationResultPage: React.FC = () => {
  const [periods, setPeriods] = useState<EvaluationPeriod[]>([]);
  const [selectedPeriodId, setSelectedPeriodId] = useState<string>('');
  const [evaluatedUsers, setEvaluatedUsers] = useState<EvaluatedUser[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [isDetailOpen, setIsDetailOpen] = useState<boolean>(false);
  const [detailData, setDetailData] = useState<DetailedEvaluationResult | null>(null);
  const [detailLoading, setDetailLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchPeriods = async () => {
      try {
        setLoading(true);
        const { data } = await api.evaluations.getEvaluationPeriods();
        setPeriods(data);
        if (data.length > 0) {
          setSelectedPeriodId(data[0].id.toString());
        }
      } catch (err) {
        setError('Failed to load evaluation periods.');
      } finally {
        setLoading(false);
      }
    };
    fetchPeriods();
  }, []);

  useEffect(() => {
    if (!selectedPeriodId) return;

    const fetchEvaluatedUsers = async () => {
      try {
        setLoading(true);
        setError(null);
        const { data } = await api.evaluations.getEvaluatedUsersByPeriod(Number(selectedPeriodId));
        setEvaluatedUsers(data);
      } catch (err) {
        setError('Failed to load evaluated users for the selected period.');
        setEvaluatedUsers([]);
      }
      finally {
        setLoading(false);
      }
    };

    fetchEvaluatedUsers();
  }, [selectedPeriodId]);

  const handlePeriodChange = (event: SelectChangeEvent<string>) => {
    setSelectedPeriodId(event.target.value as string);
  };

  const handleViewDetails = async (userId: number) => {
    try {
      setDetailLoading(true);
      setIsDetailOpen(true);
      const { data } = await api.evaluations.getDetailedEvaluationResult(Number(selectedPeriodId), userId);
      setDetailData(data);
    } catch (err) {
      setError('Failed to load evaluation details.');
    } finally {
      setDetailLoading(false);
    }
  };

  const handleCloseDetail = () => {
    setIsDetailOpen(false);
    setDetailData(null);
  };

  const columns: GridColDef[] = [
    { field: 'full_name', headerName: 'Name', flex: 1 },
    { field: 'title', headerName: 'Title', flex: 1 },
    { field: 'organization_name', headerName: 'Organization', flex: 1 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Details',
      width: 100,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<VisibilityIcon />}
          label="View Details"
          onClick={() => handleViewDetails(params.row.user_id)}
        />,
      ],
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Evaluation Results
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box sx={{ mb: 2 }}>
        <FormControl fullWidth disabled={loading}>
          <InputLabel id="period-select-label">Evaluation Period</InputLabel>
          <Select
            labelId="period-select-label"
            value={selectedPeriodId}
            label="Evaluation Period"
            onChange={handlePeriodChange}
          >
            {periods.map((p) => (
              <MenuItem key={p.id} value={p.id.toString()}>
                {p.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      <Box sx={{ height: 600, width: '100%' }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <CircularProgress />
          </Box>
        ) : (
          <DataGrid
            rows={evaluatedUsers}
            columns={columns}
            getRowId={(row) => row.user_id}
            pageSizeOptions={[10, 25, 50]}
          />
        )}
      </Box>
      {detailData && (
        <EvaluationDetailDialog
          open={isDetailOpen}
          onClose={handleCloseDetail}
          data={detailData}
          loading={detailLoading}
        />
      )}
    </Container>
  );
};

export default EvaluationResultPage;
import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Divider
} from '@mui/material';
import type { DetailedEvaluationResult } from '../../schemas/evaluation';

interface EvaluationDetailDialogProps {
  open: boolean;
  onClose: () => void;
  data: DetailedEvaluationResult | null;
  loading: boolean;
}

const EvaluationDetailDialog: React.FC<EvaluationDetailDialogProps> = ({ open, onClose, data, loading }) => {
  const renderContent = () => {
    if (loading) {
      return <CircularProgress />;
    }

    if (!data) {
      return <Typography>데이터가 없습니다.</Typography>;
    }

    if (data.status === 'IN_PROGRESS') {
      return <Typography variant="h6" color="text.secondary">아직 평가가 완료되지 않았습니다.</Typography>;
    }

    return (
      <Box>
        <Typography variant="h6" gutterBottom>최종 결과</Typography>
        <TableContainer component={Paper} variant="outlined" sx={{ mb: 2 }}>
          <Table size="small">
            <TableBody>
              <TableRow>
                <TableCell component="th" scope="row" sx={{ width: '30%' }}><strong>최종 등급</strong></TableCell>
                <TableCell>{data.final_evaluation?.grade || 'N/A'}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell component="th" scope="row"><strong>최종 점수</strong></TableCell>
                <TableCell>{data.final_evaluation?.final_score?.toFixed(2) || 'N/A'}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
        
        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" gutterBottom>프로젝트 평가</Typography>
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>프로젝트</TableCell>
                <TableCell align="right">참여 비중</TableCell>
                <TableCell align="right">동료 평가 점수</TableCell>
                <TableCell align="right">PM 평가 점수</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.project_evaluations.map((p) => (
                <React.Fragment key={p.project_id}>
                  <TableRow>
                    <TableCell component="th" scope="row">{p.project_name}</TableCell>
                    <TableCell align="right">{p.participation_weight}%</TableCell>
                    <TableCell align="right">{p.peer_evaluation_score?.toFixed(2) || '-'}</TableCell>
                    <TableCell align="right">{p.pm_evaluation_score?.toFixed(2) || '-'}</TableCell>
                  </TableRow>
                  {p.peer_feedback && p.peer_feedback.length > 0 && (
                    <TableRow>
                      <TableCell colSpan={4} style={{ paddingBottom: 0, paddingTop: 0, border: 0 }}>
                        <Box sx={{ margin: 1, padding: 1.5, bgcolor: 'grey.50', borderRadius: 1 }}>
                          <Typography variant="subtitle2" gutterBottom component="div">
                            <strong>동료 피드백</strong>
                          </Typography>
                          <TableContainer component={Paper} variant="outlined">
                            <Table size="small" aria-label="peer feedback">
                              <TableBody>
                                {p.peer_feedback.map((feedback, index) => (
                                  <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell component="th" scope="row">
                                      {feedback}
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </Box>
                      </TableCell>
                    </TableRow>
                  )}
                </React.Fragment>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" gutterBottom>정성 평가</Typography>
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>항목</TableCell>
                <TableCell align="right">점수</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell component="th" scope="row">정성 점수</TableCell>
                <TableCell align="right">{data.qualitative_evaluation?.qualitative_score?.toFixed(2) || 'N/A'} / 20</TableCell>
              </TableRow>
              <TableRow>
                <TableCell component="th" scope="row">부서 기여도 점수</TableCell>
                <TableCell align="right">{data.qualitative_evaluation?.department_contribution_score?.toFixed(2) || 'N/A'} / 10</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
        <Box sx={{ mt: 1, p: 2, border: '1px solid rgba(224, 224, 224, 1)', borderRadius: '4px' }}>
            <Typography variant="body2"><strong>차상위자 피드백:</strong> {data.qualitative_evaluation?.feedback || '-'}</Typography>
        </Box>
      </Box>
    );
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle>
        {data?.user_info.full_name}님의 상세 평가 결과
      </DialogTitle>
      <DialogContent sx={{ minHeight: '300px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        {renderContent()}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>닫기</Button>
      </DialogActions>
    </Dialog>
  );
};

export default EvaluationDetailDialog;

import React from 'react';
import { Card, CardContent, Typography, Button, CardActions } from '@mui/material';

const QualitativeEvaluationCard: React.FC = () => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">정성평가</Typography>
        <Typography color="text.secondary" sx={{ mt: 1 }}>
          팀/부서 구성원에 대한 정성평가를 진행합니다.
        </Typography>
        {/* TODO: Add evaluation form elements */}
      </CardContent>
      <CardActions>
        <Button size="small" variant="contained">제출하기</Button>
      </CardActions>
    </Card>
  );
};

export default QualitativeEvaluationCard;

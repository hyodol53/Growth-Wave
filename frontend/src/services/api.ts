// frontend/src/services/api.ts
import axios, { type AxiosResponse } from 'axios';
import type * as schemas from '../schemas/index';

// 1. apiClient.ts의 내용을 api.ts에 통합
const apiClient = axios.create({
  baseURL: '/api/v1', // 4. 상대 경로로 복원
});

// 2. 인터셉터 설정 통합
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


// 3. 기존 api.ts의 내용 (apiClient를 직접 사용하도록 수정)
export const auth = {
  login: (username: string, password: string): Promise<AxiosResponse<schemas.Token>> => {
    const credentials = new URLSearchParams();
    credentials.append('username', username);
    credentials.append('password', password);

    return apiClient.post('/auth/token', credentials, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  getCurrentUser: (): Promise<AxiosResponse<schemas.User>> =>
    apiClient.get('/users/me'),
};

export const users = {
  getUsers: (): Promise<AxiosResponse<schemas.User[]>> => apiClient.get('/users/'),
  updateUser: (
    id: number,
    data: schemas.UserUpdate
  ): Promise<AxiosResponse<schemas.User>> => apiClient.put(`/users/${id}`, data),
  createUser: (data: schemas.UserCreate): Promise<AxiosResponse<schemas.User>> =>
    apiClient.post('/users/', data),
  deleteUser: (id: number): Promise<AxiosResponse<void>> =>
    apiClient.delete(`/users/${id}`),
  getMySubordinates: (): Promise<AxiosResponse<schemas.User[]>> =>
    apiClient.get('/users/me/subordinates'),
  getUserHistory: (userId?: number): Promise<AxiosResponse<schemas.UserHistoryResponse>> =>
    apiClient.get(userId ? `/users/${userId}/history` : '/users/me/history'),
  getUserProjectWeights: (userId: number): Promise<AxiosResponse<schemas.UserProjectWeight[]>> =>
    apiClient.get(`/users/${userId}/project-weights`),
  updateUserProjectWeights: (userId: number, data: schemas.UserProjectWeightsUpdate): Promise<AxiosResponse<schemas.UserProjectWeight[]>> =>
    apiClient.put(`/users/${userId}/project-weights`, data),
};

export const organizations = {
    getOrganizations: (): Promise<AxiosResponse<schemas.Organization[]>> => apiClient.get('/organizations/'),
    createOrganization: (data: schemas.OrganizationCreate): Promise<AxiosResponse<schemas.Organization>> => apiClient.post('/organizations/', data),
    updateOrganization: (id: number, data: schemas.OrganizationUpdate): Promise<AxiosResponse<schemas.Organization>> => apiClient.put(`/organizations/${id}`, data),
    deleteOrganization: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/organizations/${id}`),
    syncChart: (file: File): Promise<AxiosResponse<any>> => {
        const formData = new FormData();
        formData.append('file', file);
        return apiClient.post('/organizations/sync-chart', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    }
};

export const projects = {
    getProjects: (): Promise<AxiosResponse<schemas.Project[]>> => apiClient.get('/projects/'),
    createProject: (data: schemas.ProjectCreate): Promise<AxiosResponse<schemas.Project>> => apiClient.post('/projects/', data),
    updateProject: (id: number, data: schemas.ProjectUpdate): Promise<AxiosResponse<schemas.Project>> => apiClient.put(`/projects/${id}`, data),
    deleteProject: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/projects/${id}`),
    getProjectMembers: (projectId: number): Promise<AxiosResponse<schemas.ProjectMemberDetails[]>> => apiClient.get(`/projects/${projectId}/members`),
};

export const evaluations = {
    getMyTasks: (): Promise<AxiosResponse<schemas.MyEvaluationTask[]>> => apiClient.get('/evaluations/my-tasks'),
    getPeerEvaluations: (projectId: number): Promise<AxiosResponse<schemas.PeerEvaluationData>> => apiClient.get(`/evaluations/peer-evaluations/${projectId}`),
    submitPeerEvaluations: (data: schemas.PeerEvaluationSubmit): Promise<AxiosResponse<any>> => apiClient.post('/evaluations/peer-evaluations/', data),
    getPmEvaluations: (projectId: number): Promise<AxiosResponse<schemas.PmEvaluationData>> => apiClient.get(`/evaluations/pm-evaluations/${projectId}`),
    submitPmEvaluations: (data: schemas.PmEvaluationSubmit): Promise<AxiosResponse<any>> => apiClient.post('/evaluations/pm-evaluations/', data),
    getEvaluationResultForUser: (userId: number): Promise<AxiosResponse<schemas.ManagerEvaluationView>> => apiClient.get(`/evaluations/${userId}/result`),
    getMyEvaluationResult: (): Promise<AxiosResponse<schemas.MyEvaluationResult>> => apiClient.get('/evaluations/me'),
    adjustGrades: (adjustments: schemas.GradeAdjustment[]): Promise<AxiosResponse<any>> => apiClient.post('/evaluations/adjust-grades', { adjustments }),

    // Settings
    getEvaluationPeriods: (): Promise<AxiosResponse<schemas.EvaluationPeriod[]>> => apiClient.get('/evaluations/evaluation-periods/'),
    createEvaluationPeriod: (data: schemas.EvaluationPeriodCreate): Promise<AxiosResponse<schemas.EvaluationPeriod>> => apiClient.post('/evaluations/evaluation-periods/', data),
    updateEvaluationPeriod: (id: number, data: schemas.EvaluationPeriodUpdate): Promise<AxiosResponse<schemas.EvaluationPeriod>> => apiClient.put(`/evaluations/evaluation-periods/${id}`, data),
    deleteEvaluationPeriod: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/evaluations/evaluation-periods/${id}`),

    getDepartmentGradeRatios: (): Promise<AxiosResponse<schemas.DepartmentGradeRatio[]>> => apiClient.get('/evaluations/department-grade-ratios/'),
    createDepartmentGradeRatio: (data: schemas.DepartmentGradeRatioCreate): Promise<AxiosResponse<schemas.DepartmentGradeRatio>> => apiClient.post('/evaluations/department-grade-ratios/', data),
    updateDepartmentGradeRatio: (id: number, data: schemas.DepartmentGradeRatioUpdate): Promise<AxiosResponse<schemas.DepartmentGradeRatio>> => apiClient.put(`/evaluations/department-grade-ratios/${id}`, data),
    deleteDepartmentGradeRatio: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/evaluations/department-grade-ratios/${id}`),

    getEvaluationWeights: (): Promise<AxiosResponse<schemas.EvaluationWeight[]>> => apiClient.get('/evaluations/'),
    createEvaluationWeight: (data: schemas.EvaluationWeightCreate): Promise<AxiosResponse<schemas.EvaluationWeight>> => apiClient.post('/evaluations/', data),
    updateEvaluationWeight: (id: number, data: schemas.EvaluationWeightUpdate): Promise<AxiosResponse<schemas.EvaluationWeight>> => apiClient.put(`/evaluations/${id}`, data),
    deleteEvaluationWeight: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/evaluations/${id}`),

    // New UX APIs
    getEvaluatedUsersByPeriod: (periodId: number): Promise<AxiosResponse<schemas.EvaluatedUser[]>> => apiClient.get(`/evaluations/periods/${periodId}/evaluated-users`),
    getDetailedEvaluationResult: (periodId: number, userId: number): Promise<AxiosResponse<schemas.DetailedEvaluationResult>> => apiClient.get(`/evaluations/periods/${periodId}/users/${userId}/details`),
};

const api = {
  auth,
  users,
  organizations,
  projects,
  evaluations,
};

export default api;

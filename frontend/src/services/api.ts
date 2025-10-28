import axios from 'axios';

import { User, UserCreate, UserUpdate, UserHistoryItem } from '../schemas/user';
import { ProjectMemberDetails } from '../schemas/project';
import { EvaluationPeriod, EvaluationPeriodCreate, EvaluationPeriodUpdate, DepartmentGradeRatio, DepartmentGradeRatioCreate, DepartmentGradeRatioUpdate, EvaluationWeight, EvaluationWeightCreate, EvaluationWeightUpdate, PeerEvaluationCreate, PmEvaluationCreate, QualitativeEvaluationCreate, ManagerEvaluationView, GradeAdjustmentRequest } from '../schemas/evaluation';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const auth = {
  login: async (username: string, password: string) => {
    const response = await api.post('/auth/token', new URLSearchParams({
      username,
      password,
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    localStorage.setItem('access_token', response.data.access_token);
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('access_token');
  },
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
  },
  getOrganizations: async () => {
    const response = await api.get('/organizations/');
    return response.data;
  },
  getUsers: async () => {
    const response = await api.get('/users/');
    return response.data;
  },

  // Organization CRUD
  createOrganization: async (data: any) => {
    const response = await api.post('/organizations/', data);
    return response.data;
  },
  updateOrganization: async (id: number, data: any) => {
    const response = await api.put(`/organizations/${id}`, data);
    return response.data;
  },
  deleteOrganization: async (id: number) => {
    const response = await api.delete(`/organizations/${id}`);
    return response.data;
  },

  // User CRUD
  createUser: async (data: any) => {
    const response = await api.post('/users/', data);
    return response.data;
  },
  updateUser: async (id: number, data: any) => {
    const response = await api.put(`/users/${id}`, data);
    return response.data;
  },
  deleteUser: async (id: number) => {
    const response = await api.delete(`/users/${id}`);
    return response.data;
  },

  // Project CRUD
  getProjects: async () => {
    const response = await api.get('/projects/');
    return response.data;
  },
  createProject: async (data: any) => {
    const response = await api.post('/projects/', data);
    return response.data;
  },
  updateProject: async (id: number, data: any) => {
    const response = await api.put(`/projects/${id}`, data);
    return response.data;
  },
  deleteProject: async (id: number) => {
    const response = await api.delete(`/projects/${id}`);
    return response.data;
  },

  // Project Members
  setProjectMemberWeights: async (data: any) => {
    const response = await api.post('/projects/members/weights', data);
    return response.data;
  },
};

export const deleteProject = (projectId: number) => api.delete(`/projects/${projectId}`);

// =============================================================================
// Evaluation APIs
// =============================================================================

// Data fetching for evaluation page
export const getUserHistory = () => api.get<UserHistoryItem[]>('/users/me/history');
export const getProjectMembers = (projectId: number) => api.get<ProjectMemberDetails[]>(`/projects/${projectId}/members`);
export const getMySubordinates = () => api.get<User[]>('/users/me/subordinates');

// Submitting evaluations
export const createPeerEvaluations = (data: PeerEvaluationCreate) => api.post('/evaluations/peer-evaluations/', data);
export const createPmEvaluations = (data: PmEvaluationCreate) => api.post('/evaluations/pm-evaluations/', data);
export const createQualitativeEvaluations = (data: QualitativeEvaluationCreate) => api.post('/evaluations/qualitative-evaluations/', data);

// Evaluation Settings
// Evaluation Periods
export const getEvaluationPeriods = () => api.get<EvaluationPeriod[]>('/evaluations/evaluation-periods/');
export const createEvaluationPeriod = (data: EvaluationPeriodCreate) => api.post<EvaluationPeriod>('/evaluations/evaluation-periods/', data);
export const updateEvaluationPeriod = (id: number, data: EvaluationPeriodUpdate) => api.put<EvaluationPeriod>(`/evaluations/evaluation-periods/${id}`, data);
export const deleteEvaluationPeriod = (id: number) => api.delete(`/evaluations/evaluation-periods/${id}`);

// Department Grade Ratios
export const getDepartmentGradeRatios = () => api.get<DepartmentGradeRatio[]>('/evaluations/department-grade-ratios/');
export const createDepartmentGradeRatio = (data: DepartmentGradeRatioCreate) => api.post<DepartmentGradeRatio>('/evaluations/department-grade-ratios/', data);
export const updateDepartmentGradeRatio = (id: number, data: DepartmentGradeRatioUpdate) => api.put<DepartmentGradeRatio>(`/evaluations/department-grade-ratios/${id}`, data);
export const deleteDepartmentGradeRatio = (id: number) => api.delete(`/evaluations/department-grade-ratios/${id}`);

// Evaluation Weights
export const getEvaluationWeights = () => api.get<EvaluationWeight[]>('/evaluations/');
export const createEvaluationWeight = (data: EvaluationWeightCreate) => api.post<EvaluationWeight>('/evaluations/', data);
export const updateEvaluationWeight = (id: number, data: EvaluationWeightUpdate) => api.put<EvaluationWeight>(`/evaluations/${id}`, data);
export const deleteEvaluationWeight = (id: number) => api.delete(`/evaluations/${id}`);

// Grade Adjustment
export const getEvaluationResultForUser = (userId: number) => api.get<ManagerEvaluationView>(`/evaluations/${userId}/result`);
export const adjustGrades = (data: GradeAdjustmentRequest) => api.post('/evaluations/adjust-grades', data);


export default api;

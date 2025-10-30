// frontend/src/services/api.ts
import axios, { type AxiosResponse } from 'axios';
import type {
    Token,
    User,
    UserUpdate,
    UserCreate,
    UserHistoryResponse,
    UserProjectWeight,
    UserProjectWeightsUpdate,
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
    Project,
    ProjectCreate,
    ProjectUpdate,
    ProjectMemberDetails,
    MyEvaluationTask,
    PeerEvaluationData,
    PeerEvaluationSubmit,
    PmEvaluationData,
    PmEvaluationSubmit,
    QualitativeEvaluationData,
    QualitativeEvaluationCreate,
    ManagerEvaluationView,
    GradeAdjustment,
    EvaluatedUser,
    DetailedEvaluationResult,
    DepartmentEvaluation,
    ExternalAccount,
    ExternalAccountCreate,
    Retrospective,
    RetrospectiveCreate,
    RetrospectiveUpdate,
    GeneratedRetrospective,
    GenerateRetrospectivePayload,
} from '../schemas';
import { DepartmentGrade } from "../schemas/evaluation";

import type {
    MyEvaluationResult,
    EvaluationPeriod,
    EvaluationPeriodCreate,
    EvaluationPeriodUpdate,
    DepartmentGradeRatio,
    DepartmentGradeRatioCreate,
    DepartmentGradeRatioUpdate,
    EvaluationWeight,
    EvaluationWeightCreate,
    EvaluationWeightUpdate,
} from '../schemas/evaluation';

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
  login: (username: string, password: string): Promise<AxiosResponse<Token>> => {
    const credentials = new URLSearchParams();
    credentials.append('username', username);
    credentials.append('password', password);

    return apiClient.post('/auth/token', credentials, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  getCurrentUser: (): Promise<AxiosResponse<User>> =>
    apiClient.get('/users/me'),
};

export const users = {
  getUsers: (): Promise<AxiosResponse<User[]>> => apiClient.get('/users/'),
  updateUser: (
    id: number,
    data: UserUpdate
  ): Promise<AxiosResponse<User>> => apiClient.put(`/users/${id}`, data),
  createUser: (data: UserCreate): Promise<AxiosResponse<User>> =>
    apiClient.post('/users/', data),
  deleteUser: (id: number): Promise<AxiosResponse<void>> =>
    apiClient.delete(`/users/${id}`),
  getMySubordinates: (): Promise<AxiosResponse<User[]>> =>
    apiClient.get('/users/me/subordinates'),
  getUserHistory: (userId?: number): Promise<AxiosResponse<UserHistoryResponse>> =>
    apiClient.get(userId ? `/users/${userId}/history` : '/users/me/history'),
  getUserProjectWeights: (userId: number): Promise<AxiosResponse<UserProjectWeight[]>> =>
    apiClient.get(`/users/${userId}/project-weights`),
  updateUserProjectWeights: (userId: number, data: UserProjectWeightsUpdate): Promise<AxiosResponse<UserProjectWeight[]>> =>
    apiClient.put(`/users/${userId}/project-weights`, data),
};

export const organizations = {
    getOrganizations: (): Promise<AxiosResponse<Organization[]>> => apiClient.get('/organizations/'),
    createOrganization: (data: OrganizationCreate): Promise<AxiosResponse<Organization>> => apiClient.post('/organizations/', data),
    updateOrganization: (id: number, data: OrganizationUpdate): Promise<AxiosResponse<Organization>> => apiClient.put(`/organizations/${id}`, data),
    setDepartmentGrade: async (orgId: number, grade: DepartmentGrade): Promise<Organization> => {
        const response = await apiClient.put(`/organizations/${orgId}/grade`, { department_grade: grade });
        return response.data;
    },

    deleteOrganization: async (orgId: number): Promise<void> => {
      await apiClient.delete(`/organizations/${orgId}`);
    },
    syncChart: (file: File): Promise<AxiosResponse<any>> => {
        const formData = new FormData();
        formData.append('file', file);
        return apiClient.post('/organizations/sync-chart', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    }
};

export const projects = {
    getProjects: (params?: { evaluation_period_id: number }): Promise<AxiosResponse<Project[]>> => apiClient.get('/projects/', { params }),
    createProject: (data: ProjectCreate): Promise<AxiosResponse<Project>> => apiClient.post('/projects/', data),
    updateProject: (id: number, data: ProjectUpdate): Promise<AxiosResponse<Project>> => apiClient.put(`/projects/${id}`, data),
    deleteProject: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/projects/${id}`),
    getProjectMembers: (projectId: number): Promise<AxiosResponse<ProjectMemberDetails[]>> => apiClient.get(`/projects/${projectId}/members`),
    addProjectMember: (projectId: number, userId: number): Promise<AxiosResponse<any>> => apiClient.post(`/projects/${projectId}/members`, { user_id: userId }),
    removeProjectMember: (projectId: number, userId: number): Promise<AxiosResponse<void>> => apiClient.delete(`/projects/${projectId}/members/${userId}`),
};

export const evaluationPeriods = {
    getEvaluationPeriods: (): Promise<AxiosResponse<EvaluationPeriod[]>> => apiClient.get('/evaluations/evaluation-periods/'),
};

export const evaluations = {
    getMyTasks: (): Promise<AxiosResponse<MyEvaluationTask[]>> => apiClient.get('/evaluations/my-tasks'),
    getPeerEvaluations: (projectId: number): Promise<AxiosResponse<PeerEvaluationData>> => apiClient.get(`/evaluations/peer-evaluations/${projectId}`),
    submitPeerEvaluations: (data: PeerEvaluationSubmit): Promise<AxiosResponse<any>> => apiClient.post('/evaluations/peer-evaluations/', data),
    getPmEvaluations: (projectId: number): Promise<AxiosResponse<PmEvaluationData>> => apiClient.get(`/evaluations/pm-evaluations/${projectId}`),
    submitPmEvaluations: (data: PmEvaluationSubmit): Promise<AxiosResponse<any>> => apiClient.post('/evaluations/pm-evaluations/', data),
    getQualitativeEvaluations: (): Promise<AxiosResponse<QualitativeEvaluationData>> => apiClient.get('/evaluations/qualitative-evaluations/'),
    submitQualitativeEvaluations: (data: QualitativeEvaluationCreate): Promise<AxiosResponse<any>> => apiClient.post('/evaluations/qualitative-evaluations/', data),
    getEvaluationResultForUser: (userId: number, evaluation_period?: string): Promise<AxiosResponse<ManagerEvaluationView>> => apiClient.get(`/evaluations/${userId}/result`, { params: { evaluation_period } }),
    getMyEvaluationResult: (): Promise<AxiosResponse<MyEvaluationResult>> => apiClient.get('/evaluations/me'),
    adjustGrades: (evaluation_period: string, adjustments: GradeAdjustment[]): Promise<AxiosResponse<any>> => apiClient.post('/evaluations/adjust-grades', { evaluation_period, adjustments }),

    // Settings
    getEvaluationPeriods: (): Promise<AxiosResponse<EvaluationPeriod[]>> => apiClient.get('/evaluations/evaluation-periods/'),
    createEvaluationPeriod: (data: EvaluationPeriodCreate): Promise<AxiosResponse<EvaluationPeriod>> => apiClient.post('/evaluations/evaluation-periods/', data),
    updateEvaluationPeriod: (id: number, data: EvaluationPeriodUpdate): Promise<AxiosResponse<EvaluationPeriod>> => apiClient.put(`/evaluations/evaluation-periods/${id}`, data),
    deleteEvaluationPeriod: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/evaluations/evaluation-periods/${id}`),

    getDepartmentGradeRatios: (): Promise<AxiosResponse<DepartmentGradeRatio[]>> => apiClient.get('/evaluations/department-grade-ratios/'),
    getDepartmentEvaluations: (evaluation_period_id: number): Promise<AxiosResponse<DepartmentEvaluation[]>> => 
      apiClient.get('/evaluations/department-evaluations/', { params: { evaluation_period_id } }),
    createDepartmentGradeRatio: (data: DepartmentGradeRatioCreate): Promise<AxiosResponse<DepartmentGradeRatio>> => apiClient.post('/evaluations/department-grade-ratios/', data),
    updateDepartmentGradeRatio: (id: number, data: DepartmentGradeRatioUpdate): Promise<AxiosResponse<DepartmentGradeRatio>> => apiClient.put(`/evaluations/department-grade-ratios/${id}`, data),
    deleteDepartmentGradeRatio: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/evaluations/department-grade-ratios/${id}`),

    getEvaluationWeights: (): Promise<AxiosResponse<EvaluationWeight[]>> => apiClient.get('/evaluations/'),
    createEvaluationWeight: (data: EvaluationWeightCreate): Promise<AxiosResponse<EvaluationWeight>> => apiClient.post('/evaluations/', data),
    updateEvaluationWeight: (id: number, data: EvaluationWeightUpdate): Promise<AxiosResponse<EvaluationWeight>> => apiClient.put(`/evaluations/${id}`, data),
    deleteEvaluationWeight: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/evaluations/${id}`),

    // New UX APIs
    getEvaluatedUsersByPeriod: (periodId: number): Promise<AxiosResponse<EvaluatedUser[]>> => apiClient.get(`/evaluations/periods/${periodId}/evaluated-users`),
    getDetailedEvaluationResult: (periodId: number, userId: number): Promise<AxiosResponse<DetailedEvaluationResult>> => apiClient.get(`/evaluations/periods/${periodId}/users/${userId}/details`),
    calculateFinalScores: (evaluationPeriodId: number): Promise<AxiosResponse<{ message: string }>> => apiClient.post(`/evaluations/evaluation-periods/${evaluationPeriodId}/calculate`),

    // Department Evaluations
    upsertDepartmentEvaluation: (data: { department_id: number; grade: string; evaluation_period_id: number }): Promise<AxiosResponse<any>> => 
        apiClient.post('/evaluations/department-evaluations/', data),
};

export const externalAccounts = {
    getAccounts: (): Promise<AxiosResponse<ExternalAccount[]>> => apiClient.get('/external-accounts'),
    createAccount: (data: ExternalAccountCreate): Promise<AxiosResponse<ExternalAccount>> => apiClient.post('/external-accounts', data),
    deleteAccount: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/external-accounts/${id}`),
};

export const retrospectives = {
    getList: (): Promise<AxiosResponse<Retrospective[]>> => apiClient.get('/retrospectives'),
    getById: (id: number): Promise<AxiosResponse<Retrospective>> => apiClient.get(`/retrospectives/${id}`),
    create: (data: RetrospectiveCreate): Promise<AxiosResponse<Retrospective>> => apiClient.post('/retrospectives', data),
    update: (id: number, data: RetrospectiveUpdate): Promise<AxiosResponse<Retrospective>> => apiClient.put(`/retrospectives/${id}`, data),
    delete: (id: number): Promise<AxiosResponse<void>> => apiClient.delete(`/retrospectives/${id}`),
    generate: (payload: GenerateRetrospectivePayload): Promise<AxiosResponse<GeneratedRetrospective>> => apiClient.post('/retrospectives/generate', payload),
};

const api = {
  auth,
  users,
  organizations,
  projects,
  evaluations,
  externalAccounts,
  retrospectives,
};

export default api;

import axios from 'axios';

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
  getCurrentUser: async () => {
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
  getProjectMembers: async (id: number) => {
    const response = await api.get(`/projects/${id}/members`);
    return response.data;
  },
};

export default api;

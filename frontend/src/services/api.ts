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
};

export default api;

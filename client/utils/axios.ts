import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401) {
      // Try to refresh token
      try {
        const refresh = localStorage.getItem('refresh');
        if (refresh) {
          const response = await axios.post('/auth/jwt/refresh/', {
            refresh
          });
          localStorage.setItem('token', response.data.access);
          error.config.headers.Authorization = `Bearer ${response.data.access}`;
          return api.request(error.config);
        }
      } catch (refreshError) {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
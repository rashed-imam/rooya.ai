import { createContext, useContext, useState, useEffect } from 'react';
import api from '../utils/api';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      fetchUserData();
    }
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await api.get('/api/auth/user/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      const response = await api.post('/auth/jwt/create/', {
        username,
        password
      });
      
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
      setIsAuthenticated(true);
      await fetchUserData();
    } catch (error) {
      console.error('Login error:', error);
      throw new Error('Invalid credentials');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
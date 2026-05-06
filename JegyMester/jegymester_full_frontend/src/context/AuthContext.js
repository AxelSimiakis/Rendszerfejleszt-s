import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { api } from '../api/endpoints';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const normalizeUser = (data) => ({
    ...data,
    roles: data?.roles || []
  });

  const loadUser = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const res = await api.me();
      setUser(normalizeUser(res.data));
    } catch {
      localStorage.removeItem('token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  const login = async (email, password) => {
    const res = await api.login({ email, password });
    if (!res.data?.token) throw new Error('A backend nem adott vissza tokent.');
    localStorage.setItem('token', res.data.token);
    setUser(normalizeUser(res.data));
    await loadUser();
  };

  const register = async (formData) => {
    await api.register(formData);
    await login(formData.email, formData.password);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = useMemo(() => ({ user, login, register, logout, loading }), [user, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);

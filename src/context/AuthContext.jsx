// src/context/AuthContext.jsx

import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  // Dev auto-login is OFF by default. To enable for local testing set Vite env var `VITE_DEV_ADMIN=true`.
  const DEV_ADMIN_OVERRIDE = import.meta.env.VITE_DEV_ADMIN === 'true'
    ? { is_admin: true, isAdmin: true, role: 'admin', nome: 'Dev Admin', email: 'dev@local' }
    : null;

  const getInitial = () => {
    try {
      const rawUser = localStorage.getItem('user');
      const token = localStorage.getItem('token');
      if (rawUser) return { user: JSON.parse(rawUser), token };
    } catch (e) {
      // ignore
    }
    // If DEV override is enabled explicitly via VITE_DEV_ADMIN, use it; otherwise start logged out
    return { user: DEV_ADMIN_OVERRIDE, token: null };
  };

  const initial = getInitial();

  const [user, setUser] = useState(initial.user);
  const [token, setToken] = useState(initial.token);

  const isLoggedIn = !!user;

  // login agora espera (userData, jwt)
  const login = (userData, jwt) => {
    setUser(userData);
    setToken(jwt || null);
    try {
      localStorage.setItem('user', JSON.stringify(userData));
      if (jwt) localStorage.setItem('token', jwt);
    } catch (e) {
      // ignore
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    try {
      localStorage.removeItem('user');
      localStorage.removeItem('token');
    } catch (e) {
      // ignore
    }
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
// src/context/AuthContext.jsx

import React, { createContext, useContext, useState } from 'react';

// 1. Cria o Contexto
const AuthContext = createContext();

// 2. Componente Provedor (É OBRIGATÓRIO envolver o App com ele!)
export const AuthProvider = ({ children }) => {
  // Em desenvolvimento, expõe um usuário admin de teste para facilitar QA
  const DEV_ADMIN_OVERRIDE = process.env.NODE_ENV !== 'production'
    ? { isAdmin: true, role: 'admin', nome: 'Dev Admin', email: 'dev@local' }
    : null;

  // Tenta recuperar um usuário salvo no localStorage; senão usa o override de dev
  const getInitialUser = () => {
    try {
      const raw = localStorage.getItem('user');
      if (raw) return JSON.parse(raw);
    } catch (e) {
      // ignore
    }
    return DEV_ADMIN_OVERRIDE;
  };

  const initialUser = getInitialUser();

  // Estado: reflete se há um usuário inicial
  const [isLoggedIn, setIsLoggedIn] = useState(!!initialUser);
  const [user, setUser] = useState(initialUser); // Dados do usuário

  // Função para simular o login (será chamada pelo Login.jsx ou Cadastro.jsx)
  const login = (userData) => {
    setIsLoggedIn(true);
    setUser(userData);
    try {
      localStorage.setItem('user', JSON.stringify(userData));
    } catch (e) {
      // ignore storage errors in environments without localStorage
    }
    // Futuramente: aqui você salvará um token JWT no localStorage
  };

  // Função para simular o logout (será chamada pelo Navbar.jsx)
  const logout = () => {
    setIsLoggedIn(false);
    setUser(null);
    try {
      localStorage.removeItem('user');
    } catch (e) {
      // ignore
    }
    // Futuramente: aqui você removerá o token JWT do localStorage
  };

  return (
    // O 'value' é o que estará disponível para qualquer componente que usar 'useAuth()'
    <AuthContext.Provider value={{ isLoggedIn, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// 3. Hook customizado: é o que o Cadastro.jsx importa (useAuth)
export const useAuth = () => useContext(AuthContext);
// src/context/AuthContext.jsx

import React, { createContext, useContext, useState } from 'react';

// 1. Cria o Contexto
const AuthContext = createContext();

// 2. Componente Provedor (É OBRIGATÓRIO envolver o App com ele!)
export const AuthProvider = ({ children }) => {
  // Simulação de estado: isLoggedIn dirá se o usuário está logado
  const [isLoggedIn, setIsLoggedIn] = useState(false); 
  const [user, setUser] = useState(null); // Dados do usuário

  // Função para simular o login (será chamada pelo Login.jsx ou Cadastro.jsx)
  const login = (userData) => {
    setIsLoggedIn(true);
    setUser(userData); 
    // Futuramente: aqui você salvará um token JWT no localStorage
  };

  // Função para simular o logout (será chamada pelo Navbar.jsx)
  const logout = () => {
    setIsLoggedIn(false);
    setUser(null);
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
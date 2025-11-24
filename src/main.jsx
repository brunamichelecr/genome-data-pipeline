// src/main.jsx

import React from 'react';
import ReactDOM from 'react-dom/client';
// Importa o componente para habilitar o roteamento (rotas)
import { BrowserRouter } from 'react-router-dom'; 
import App from './App.jsx';

// Importa o Contexto de Autenticação
import { AuthProvider } from './context/AuthContext'; 

// Importa o arquivo SCSS principal que contém o Bootstrap e seus estilos.
// 💡 Certifique-se de que o caminho './styles/custom.scss' está correto.
import './styles/custom.scss'; 

// Ponto de entrada do React: 
// 1. <BrowserRouter> envolve tudo para que as rotas funcionem.
// 2. <AuthContextProvider> envolve <App /> para que todos os componentes acessem 
//    o estado de login e as funções (login, logout, user).
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
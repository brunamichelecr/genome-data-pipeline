// src/App.jsx

import React from 'react';
// IMPORTANTE: Remova a importação de 'BrowserRouter as Router' e 'AuthProvider'.
// Mantenha apenas o que é usado DENTRO do componente App.
import { Routes, Route } from 'react-router-dom'; 

// Importações dos Componentes de Layout
import Navbar from './components/Navbar'; 
import Footer from './components/Footer'; 

// Componentes de Contexto (NÃO precisam ser importados aqui se já estão no main.jsx)
// REMOVA: import { AuthProvider } from './context/AuthContext'; 

// Importações dos Componentes de Página
import Cadastro from './pages/Cadastro'; 
import Login from './pages/Login';
import Resultados from './pages/Resultados';
import Home from './pages/Home'; 
import Sobre from './pages/Sobre'; 
import Contato from './pages/Contato'; 
import CarregarDados from './pages/CarregarDados'; 
import CadastroDoenca from './pages/CadastroDoenca';


function App() {
  return (
    // ATENÇÃO: Removemos <AuthProvider> e <Router> daqui!
    // Usamos apenas o div de layout.
    <div className="d-flex flex-column min-vh-100">
      
      <Navbar /> 
      
      <main className="flex-grow-1">
        <Routes>
          {/* Rota principal (index.html) */}
          <Route path="/" element={<Home />} />
          
          {/* Rotas de Autenticação */}
          <Route path="/cadastro" element={<Cadastro />} /> 
          <Route path="/login" element={<Login />} />
          
          {/* Rota de Funcionalidade */}
          <Route path="/carregar-dados" element={<CarregarDados />} />
          <Route path="/resultados" element={<Resultados />} />
          
          {/* Rotas Estáticas */}
          <Route path="/sobre" element={<Sobre />} />
          <Route path="/contato" element={<Contato />} />

          {/* Rota para cadastro de doenças (apenas admins) */}
          <Route path="/cadastro-doenca" element={<CadastroDoenca />} />

          {/* Rota 404/Página não encontrada (Opcional) */}
          {/* <Route path="*" element={<h1>404 - Página Não Encontrada</h1>} /> */}
        </Routes>
      </main>
      
      <Footer /> 
    </div>
    // ATENÇÃO: Removemos o fechamento dos wrappers AuthProvider e Router!
  );
}

export default App;
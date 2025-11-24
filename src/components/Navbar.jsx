// src/components/Navbar.jsx

import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Importação essencial

function AppNavbar() {
  // 💡 Hooks de Contexto e Navegação
  const { isLoggedIn, user, logout } = useAuth(); // Pega o estado e a função logout
  const navigate = useNavigate();

  // Verifica se o usuário é administrador
  const isAdmin = user && (user.isAdmin === true || user.role === 'admin');

  // Função para lidar com a saída do sistema
  const handleLogout = () => {
    logout(); // Chama a função logout do AuthContext (limpa a sessão)
    navigate('/'); // Redireciona o usuário para a página inicial
  };

  return (
    <Navbar expand="lg" className="bg-white shadow-sm py-3" sticky="top">
      <Container>
        {/* Logo/Título - Sempre usa Link para a rota inicial */}
        <Navbar.Brand as={Link} to="/" className="fw-bold d-flex align-items-center">
          {/* 💡 Se você tiver uma imagem de favicon/logo, use aqui. 
          Ex: <img src="/favicon.png" alt="DemoMind Logo" height="30" className="me-2" /> */}
          <span className="h4 mb-0" style={{ color: '#3e8e7e' }}>DemoMind</span>
        </Navbar.Brand>
        
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        
        <Navbar.Collapse id="basic-navbar-nav">
          {/* Links Principais (Esquerda) */}
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Início</Nav.Link>
            <Nav.Link as={Link} to="/carregar-dados">Análise</Nav.Link>
            <Nav.Link as={Link} to="/resultados">Resultados</Nav.Link>
            <Nav.Link as={Link} to="/sobre">Sobre</Nav.Link>
            <Nav.Link as={Link} to="/contato">Contato</Nav.Link>
            {isAdmin && (
              <Nav.Link as={Link} to="/cadastro-doenca">Cadastro Doença</Nav.Link>
            )}
          </Nav>
          
          {/* Links de Autenticação (Direita) */}
          <Nav>
            {isLoggedIn ? (
              // 💡 SE ESTIVER LOGADO
                <>
                <Navbar.Text className="me-3 fw-bold text-primary">
                  Olá, {user?.nome || 'Usuário'}!
                </Navbar.Text>
                {isAdmin && (
                  <Button as={Link} to="/cadastro-doenca" variant="outline-primary" className="me-2">
                    Cadastro Doença
                  </Button>
                )}
                <Button className="btn-logout" onClick={handleLogout}>
                  Sair
                </Button>
              </>
            ) : (
              // 💡 SE NÃO ESTIVER LOGADO
              <>
                <Nav.Link as={Link} to="/login" className="me-2">
                  Login
                </Nav.Link>
                <Button as={Link} to="/cadastro" variant="primary" className="btn-navbar-create">
                  Cadastrar
                </Button>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default AppNavbar;
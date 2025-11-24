// src/pages/Login.jsx

import React, { useState } from 'react';
import { Form, Button, Card, Container, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; 
import CookieBanner from '../components/CookieBanner';

const initialFormData = {
  email: '',
  senha: '',
};

function Login() {
  const [formData, setFormData] = useState(initialFormData);
  const [feedback, setFeedback] = useState({ message: '', type: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const navigate = useNavigate(); // Hook para redirecionar
  const { login } = useAuth(); // Hook para mudar o estado de login global

  // Manipulador de Mudança (Conecta os campos ao estado)
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value,
    }));
    setFeedback({ message: '', type: '' }); // Limpa a mensagem ao digitar
  };
  
  // Lógica de Submissão (Simula a API de Login)
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.senha) {
      setFeedback({ message: 'E-mail e senha são obrigatórios.', type: 'danger' });
      return;
    }

    setIsSubmitting(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 1000)); 
      
      // Validação simulada para teste:
      if (formData.email === 'test@demomind.com' && formData.senha === 'senha123') {
        setFeedback({ message: 'Login realizado com sucesso!', type: 'success' });
        
        login({ email: formData.email, nome: 'Usuário de Teste' }); 
        
        // Redireciona para onde o usuário logado deve ir (ex: página de resultados)
        navigate('/resultados'); 
        
      } else {
        setFeedback({ message: 'E-mail ou senha inválidos.', type: 'danger' });
      }

    } catch (error) {
      setFeedback({ message: 'Erro ao tentar conectar. Tente novamente.', type: 'danger' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="flex-grow-1 d-flex justify-content-center align-items-center py-5">
      <Card className="p-4 shadow-sm" style={{ maxWidth: '400px', width: '100%' }}>
        <h2 className="text-center mb-4">Entrar</h2>

        {feedback.message && (
          <Alert variant={feedback.type} className="mb-3">
            {feedback.message}
          </Alert>
        )}

        <Form onSubmit={handleSubmit} noValidate>
          {/* Campo E-mail - Conectado ao estado */}
          <Form.Group className="mb-3" controlId="email">
            <Form.Label>E-mail</Form.Label>
            <Form.Control
              type="email"
              name="email"
              placeholder="seu@email.com"
              required
              value={formData.email}
              onChange={handleChange}
            />
          </Form.Group>

          {/* Campo Senha - Conectado ao estado */}
          <Form.Group className="mb-3" controlId="senha">
            <Form.Label>Senha</Form.Label>
            <Form.Control
              type="password"
              name="senha"
              placeholder="********"
              required
              value={formData.senha}
              onChange={handleChange}
            />
          </Form.Group>

          <Button type="submit" className="w-100" disabled={isSubmitting}>
            {isSubmitting ? 'Verificando...' : 'Login'}
          </Button>

          <div className="text-center mt-3">
            <a href="#">Esqueceu a senha? (Simulação)</a>
          </div>

          <div className="text-center mt-2">
            <Link to="/cadastro" className="btn btn-outline-primary w-100 btn-create">
              Criar conta
            </Link>
          </div>
        </Form>
      </Card>
      <CookieBanner />
    </main>
  );
}

export default Login;
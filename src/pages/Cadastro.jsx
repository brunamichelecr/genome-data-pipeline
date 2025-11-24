// src/pages/Cadastro.jsx

import React, { useState } from 'react';
// Importamos o React-Bootstrap para usar os componentes visuais
import { Form, Button, Card, Container, Alert } from 'react-bootstrap';
// Importamos o Link para navegação e o useAuth para o estado global
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; 
import CookieBanner from '../components/CookieBanner'; 

// Estado inicial para o formulário
const initialFormData = {
  nome: '',
  genero: '',
  email: '',
  senha: '',
  confirmar: '',
  termos: false,
};

function Cadastro() {
  // 💡 Hooks de Estado Local
  const [formData, setFormData] = useState(initialFormData);
  const [feedback, setFeedback] = useState({ message: '', type: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 💡 Hook de Contexto Global: Pega a função 'login' do AuthProvider
  const { login } = useAuth(); 

  // Manipulador de Mudança Genérico
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value, // Lida com checkbox e input normal
    }));
    setFeedback({ message: '', type: '' });
  };
  
  // Lógica de Validação (Replicando o cadastro.js)
  const validateForm = () => {
    const { nome, genero, email, senha, confirmar, termos } = formData;
    const senhaValidaRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

    if (!nome || !genero || !email || !senha || !confirmar) {
      setFeedback({ message: 'Todos os campos são obrigatórios.', type: 'danger' });
      return false;
    }

    if (!termos) {
      setFeedback({ message: 'Você precisa concordar com os termos de uso e política de privacidade.', type: 'danger' });
      return false;
    }

    if (!senhaValidaRegex.test(senha)) {
      setFeedback({ message: 'A senha deve conter pelo menos 8 caracteres, incluindo letras e números.', type: 'danger' });
      return false;
    }

    if (senha !== confirmar) {
      setFeedback({ message: 'As senhas não conferem.', type: 'danger' });
      return false;
    }

    return true; 
  };


  // Lógica de Submissão (Simulação de API)
  const handleSubmit = async (e) => {
    e.preventDefault(); 

    if (!validateForm()) {
      return; 
    }

    setIsSubmitting(true); 

    try {
      // --- SIMULAÇÃO DA CHAMADA À API ---
      if (formData.email === 'simular@erro.com') {
        setFeedback({ message: 'E-mail já cadastrado. Tente outro.', type: 'danger' });
      } 
      else {
        await new Promise(resolve => setTimeout(resolve, 1500)); 
        
        setFeedback({ message: 'Cadastro realizado com sucesso! Redirecionando...', type: 'success' });
        
        // Chama a função de login do Contexto para atualizar o estado global
        login({ email: formData.email, nome: formData.nome }); 
      }

    } catch (error) {
      setFeedback({ message: 'Erro ao conectar com o servidor. Tente novamente mais tarde.', type: 'danger' });
      console.error(error);
    } finally {
      setIsSubmitting(false); 
    }
  };

  return (
    <section className="py-5">
      <Container className="pt-5 mt-5 d-flex justify-content-center align-items-center">
        <Card className="p-4 shadow-sm" style={{ maxWidth: '500px', width: '100%' }}>
          <h2 className="text-center mb-4">Criar Conta</h2>

          {feedback.message && (
            <Alert variant={feedback.type} className="mb-3">
              {feedback.message}
            </Alert>
          )}

          <Form onSubmit={handleSubmit} noValidate>
            {/* Campo Nome */}
            <Form.Group className="mb-3" controlId="nome">
              <Form.Label>Nome Completo</Form.Label>
              <Form.Control
                type="text"
                name="nome"
                placeholder="Seu nome completo"
                required
                value={formData.nome}
                onChange={handleChange}
              />
            </Form.Group>

            {/* Campo Gênero */}
            <Form.Group className="mb-3" controlId="genero">
              <Form.Label>Gênero</Form.Label>
              <Form.Select name="genero" required value={formData.genero} onChange={handleChange}>
                <option value="">Selecione...</option>
                <option value="Feminino">Feminino</option>
                <option value="Masculino">Masculino</option>
                <option value="Outro">Outro</option>
                <option value="NaoInformar">Não Informar</option>
              </Form.Select>
            </Form.Group>

            {/* Campo E-mail */}
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

            {/* Campo Senha */}
            <Form.Group className="mb-3" controlId="senha">
              <Form.Label>Senha (mín. 8 caracteres, letra e número)</Form.Label>
              <Form.Control
                type="password"
                name="senha"
                placeholder="********"
                required
                minlength="8"
                value={formData.senha}
                onChange={handleChange}
              />
            </Form.Group>

            {/* Campo Confirmar Senha */}
            <Form.Group className="mb-3" controlId="confirmar-senha">
              <Form.Label>Confirmar senha</Form.Label>
              <Form.Control
                type="password"
                name="confirmar"
                placeholder="********"
                required
                minlength="8"
                value={formData.confirmar}
                onChange={handleChange}
              />
            </Form.Group>

            {/* Checkbox Termos */}
            <Form.Group className="form-check mb-3">
              <Form.Check
                type="checkbox"
                id="termos"
                name="termos"
                required
                checked={formData.termos}
                onChange={handleChange}
                label={
                  <>
                    Concordo com os <Link to="/termos-de-uso">termos de uso</Link> e{' '}
                    <Link to="/politica-de-privacidade">política de privacidade</Link>.
                  </>
                }
              />
            </Form.Group>

            {/* Botão de Submissão */}
            <Button type="submit" className="w-100" disabled={isSubmitting}>
              {isSubmitting ? 'Cadastrando...' : 'Cadastrar'}
            </Button>

            {/* Link para Login */}
            <div className="text-center mt-3">
              <Link to="/login">Já tem uma conta? Faça login</Link>
            </div>
          </Form>
        </Card>
      </Container>
      <CookieBanner /> 
    </section>
  );
}

export default Cadastro;
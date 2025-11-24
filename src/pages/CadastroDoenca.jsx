// src/pages/CadastroDoenca.jsx
import React, { useState } from 'react';
import { Container, Card, Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import CookieBanner from '../components/CookieBanner';

function CadastroDoenca() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [formData, setFormData] = useState({
    disease_name: '',
    disease_name_pt: '',
    medgen_uid: '',
    disease_desc_pt: '',
    breve_desc: '',
  });

  const [feedback, setFeedback] = useState({ message: '', type: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setFeedback({ message: '', type: '' });
  };

  const validate = () => {
    if (!formData.disease_name || !formData.disease_name_pt) {
      setFeedback({ message: 'Os campos nome (EN) e nome (PT) são obrigatórios.', type: 'danger' });
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setIsSubmitting(true);

    try {
      // Simulação de chamada à API: aguarda 1s e retorna sucesso
      await new Promise(res => setTimeout(res, 1000));
      setFeedback({ message: 'Doença cadastrada com sucesso.', type: 'success' });
      // Após cadastro, opcionalmente limpar ou redirecionar
      setFormData({ disease_name: '', disease_name_pt: '', medgen_uid: '', disease_desc_pt: '', breve_desc: '' });
      // navigate('/resultados'); // se desejar redirecionar
    } catch (err) {
      console.error(err);
      setFeedback({ message: 'Erro ao cadastrar. Tente novamente.', type: 'danger' });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Verificação simples de admin: espera-se que `user` tenha `isAdmin` ou `role === 'admin'`
  const isAdmin = user && (user.isAdmin === true || user.role === 'admin');

  if (!isAdmin) {
    return (
      <section className="py-5">
        <Container className="pt-5 mt-5 d-flex justify-content-center align-items-center">
          <Card className="p-4 shadow-sm" style={{ maxWidth: '700px', width: '100%' }}>
            <h3 className="mb-3">Acesso restrito</h3>
            <p>Esta página está disponível apenas para administradores do site.</p>
          </Card>
        </Container>
        <CookieBanner />
      </section>
    );
  }

  return (
    <section className="py-5">
      <Container className="pt-5 mt-5 d-flex justify-content-center align-items-center">
        <Card className="p-4 shadow-sm" style={{ maxWidth: '800px', width: '100%' }}>
          <h2 className="text-center mb-4">Cadastrar Doença</h2>

          {feedback.message && (
            <Alert variant={feedback.type} className="mb-3">{feedback.message}</Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="disease_name">
              <Form.Label>Nome (EN)</Form.Label>
              <Form.Control
                type="text"
                name="disease_name"
                placeholder="Disease name (EN)"
                value={formData.disease_name}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="disease_name_pt">
              <Form.Label>Nome (PT)</Form.Label>
              <Form.Control
                type="text"
                name="disease_name_pt"
                placeholder="Nome da doença (PT)"
                value={formData.disease_name_pt}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="medgen_uid">
              <Form.Label>MedGen UID</Form.Label>
              <Form.Control
                type="text"
                name="medgen_uid"
                placeholder="Ex: D012345"
                value={formData.medgen_uid}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="breve_desc">
              <Form.Label>Breve descrição</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                name="breve_desc"
                placeholder="Resumo curto da doença"
                value={formData.breve_desc}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="disease_desc_pt">
              <Form.Label>Descrição (PT)</Form.Label>
              <Form.Control
                as="textarea"
                rows={6}
                name="disease_desc_pt"
                placeholder="Descrição detalhada da doença em português"
                value={formData.disease_desc_pt}
                onChange={handleChange}
              />
            </Form.Group>

            <div className="d-grid">
              <Button type="submit" disabled={isSubmitting} variant="primary">
                {isSubmitting ? 'Cadastrando...' : 'Cadastrar Doença'}
              </Button>
            </div>
          </Form>
        </Card>
      </Container>
      <CookieBanner />
    </section>
  );
}

export default CadastroDoenca;

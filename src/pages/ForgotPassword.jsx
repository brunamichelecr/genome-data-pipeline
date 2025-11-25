import React, { useState } from 'react';
import { Form, Button, Card, Container, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [feedback, setFeedback] = useState({ message: '', type: '' });
  const [code, setCode] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFeedback({ message: '', type: '' });
    setCode(null);
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const data = await resp.json();
      if (!resp.ok) {
        setFeedback({ message: data.detail || 'Erro ao solicitar reset.', type: 'danger' });
      } else {
        setFeedback({ message: data.detail || 'Se o e-mail existe, um código foi enviado.', type: 'success' });
        if (data.reset_code) setCode(data.reset_code);
      }
    } catch (err) {
      setFeedback({ message: 'Erro ao conectar com o servidor.', type: 'danger' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="py-5">
      <Container className="pt-5 mt-5 d-flex justify-content-center align-items-center">
        <Card className="p-4 shadow-sm" style={{ maxWidth: '500px', width: '100%' }}>
          <h2 className="text-center mb-4">Esqueceu a senha</h2>

          {feedback.message && (
            <Alert variant={feedback.type} className="mb-3">{feedback.message}</Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="email">
              <Form.Label>E-mail</Form.Label>
              <Form.Control type="email" name="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
            </Form.Group>

            <Button type="submit" className="w-100" disabled={isSubmitting}>{isSubmitting ? 'Enviando...' : 'Enviar código de redefinição'}</Button>

            {code && (
                  <div className="mt-3">
                    <p className="small text-muted">Código (apenas desenvolvimento):</p>
                    <pre style={{ wordBreak: 'break-all' }}>{code}</pre>
                    <p className="small">Copie esse código ou use o botão abaixo para abrir a página de redefinição.</p>
                    <div className="d-flex gap-2">
                      <Link to={`/reset-password?token=${code}`} className="btn btn-primary">Ir para Redefinição</Link>
                      <Link to="/reset-password" className="btn btn-outline-secondary">Abrir página de redefinição</Link>
                    </div>
                  </div>
                )}
            {!code && feedback.type === 'success' && (
                  <div className="mt-3">
                    <p className="small">Se você não recebeu o código, verifique o e-mail ou tente novamente. Você também pode abrir a página de redefinição manualmente:</p>
                    <Link to="/reset-password" className="btn btn-outline-primary">Abrir página de redefinição</Link>
                  </div>
                )}
          </Form>
        </Card>
      </Container>
    </section>
  );
}

export default ForgotPassword;

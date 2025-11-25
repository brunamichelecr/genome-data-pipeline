import React, { useState } from 'react';
import { Form, Button, Card, Container, Alert } from 'react-bootstrap';

function ForgotPassword2() {
  const [email, setEmail] = useState('');
  const [feedback, setFeedback] = useState({ message: '', type: '' });
  const [token, setToken] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFeedback({ message: '', type: '' });
    setToken(null);
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
        // backend returns `reset_code` for development flow
        if (data.reset_code) setToken(data.reset_code);
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

            <Button type="submit" className="w-100" disabled={isSubmitting}>{isSubmitting ? 'Enviando...' : 'Enviar token de redefinição'}</Button>

            {token && (
              <div className="mt-3">
                <p className="small text-muted">Código (apenas desenvolvimento):</p>
                <pre style={{ wordBreak: 'break-all' }}>{token}</pre>
                <p className="small">Copie esse código e cole na página de redefinição de senha.</p>
              </div>
            )}
          </Form>
        </Card>
      </Container>
    </section>
  );
}

export default ForgotPassword2;

import React, { useState } from 'react';
import { Form, Button, Card, Container, Alert } from 'react-bootstrap';
import { useSearchParams, useNavigate } from 'react-router-dom';

function ResetPassword() {
  const [searchParams] = useSearchParams();
  const preToken = searchParams.get('token') || '';
  const [code, setCode] = useState(preToken);
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmar, setConfirmar] = useState('');
  const [feedback, setFeedback] = useState({ message: '', type: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const codeTrim = (code || '').toString().trim();
    const codeValid = /^[A-Za-z0-9]{6}$/.test(codeTrim);

    if (!senha || senha.length < 8) {
      setFeedback({ message: 'Senha deve ter ao menos 8 caracteres.', type: 'danger' });
      return;
    }
    if (senha !== confirmar) {
      setFeedback({ message: 'As senhas não conferem.', type: 'danger' });
      return;
    }
    if (!codeValid) {
      setFeedback({ message: 'Código inválido. Deve ter 6 caracteres alfanuméricos.', type: 'danger' });
      return;
    }
    setIsSubmitting(true);
    setFeedback({ message: '', type: '' });
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, code, senha })
      });
      const data = await resp.json();
      if (!resp.ok) {
        setFeedback({ message: data.detail || 'Erro ao redefinir senha.', type: 'danger' });
      } else {
        setFeedback({ message: data.detail || 'Senha alterada com sucesso. Redirecionando para login...', type: 'success' });
        // redirect to login after a short delay so the user sees the message
        setTimeout(() => navigate('/login'), 900);
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
          <h2 className="text-center mb-4">Redefinir senha</h2>

          {feedback.message && (
            <Alert variant={feedback.type} className="mb-3">{feedback.message}</Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="email">
              <Form.Label>E-mail</Form.Label>
              <Form.Control type="email" name="email" required value={email} onChange={(e)=>setEmail(e.target.value)} />
            </Form.Group>

            <Form.Group className="mb-3" controlId="code">
              <Form.Label>Código de redefinição (6 caracteres)</Form.Label>
              <Form.Control type="text" name="code" required value={code} onChange={(e)=>setCode(e.target.value)} />
            </Form.Group>

            <Form.Group className="mb-3" controlId="senha">
              <Form.Label>Nova senha</Form.Label>
              <Form.Control type="password" name="senha" required value={senha} onChange={(e)=>setSenha(e.target.value)} />
            </Form.Group>

            <Form.Group className="mb-3" controlId="confirmar">
              <Form.Label>Confirmar senha</Form.Label>
              <Form.Control type="password" name="confirmar" required value={confirmar} onChange={(e)=>setConfirmar(e.target.value)} />
            </Form.Group>

            <Button type="submit" className="w-100" disabled={isSubmitting}>{isSubmitting ? 'Enviando...' : 'Redefinir senha'}</Button>
          </Form>
        </Card>
      </Container>
    </section>
  );
}

export default ResetPassword;

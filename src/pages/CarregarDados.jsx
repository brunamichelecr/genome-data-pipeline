// src/pages/CarregarDados.jsx

import React, { useState, useEffect } from 'react';
import { Container, Card, Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import CookieBanner from '../components/CookieBanner';

function CarregarDados() {
  const navigate = useNavigate();
  // 💡 Hook Global: Verifica se o usuário está logado
  const { isLoggedIn } = useAuth(); 
  
  // Hook 1: Armazena o arquivo selecionado
  const [selectedFile, setSelectedFile] = useState(null);
  // Hook 2: Gerencia o feedback da operação
  const [feedback, setFeedback] = useState({ message: '', type: '' });
  // Hook 3: Controla o estado do formulário (enviando/pronto)
  const [isUploading, setIsUploading] = useState(false);
  // Hook 4: Simula se o usuário já enviou um arquivo (para replicar o 'already' do Jinja)
  const [hasAlreadyUploaded, setHasAlreadyUploaded] = useState(false); 

  // 💡 Efeito: Redireciona se não estiver logado
  useEffect(() => {
    if (!isLoggedIn) {
      // Se não estiver logado, redireciona para a página de login
      navigate('/login');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoggedIn]); 

  // Manipula a seleção do arquivo
  const handleFileChange = (e) => {
    setFeedback({ message: '', type: '' });
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      
      // Validação de tipo de arquivo (replica o accept=".csv" do HTML)
      if (file.type && file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
         setFeedback({ message: 'Por favor, envie apenas arquivos no formato CSV.', type: 'danger' });
         setSelectedFile(null);
      } else {
         setSelectedFile(file);
      }
    } else {
      setSelectedFile(null);
    }
  };

  // Manipula o envio do formulário (Simulação de POST multipart/form-data)
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setFeedback({ message: 'Selecione um arquivo CSV para continuar.', type: 'warning' });
      return;
    }
    
    if (isUploading) return;
    
    setIsUploading(true); // Inicia o estado de upload
    setFeedback({ message: 'Processando arquivo...', type: 'info' });

    // --- SIMULAÇÃO DA CHAMADA À API (Substituirá o POST real do Flask) ---
    try {
      // 1. Cria o objeto FormData (Necessário para enviar arquivos)
      const formData = new FormData();
      formData.append('file', selectedFile);

      // 2. Simula o tempo de processamento do Back-end
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // 3. Simula o sucesso e o redirecionamento
      setFeedback({ 
        message: 'Arquivo enviado e análise iniciada! Redirecionando para resultados...', 
        type: 'success' 
      });
      setHasAlreadyUploaded(true); // Simula que o arquivo já foi enviado
      
      // 4. Redireciona para a página de resultados após o sucesso
      setTimeout(() => {
        navigate('/resultados');
      }, 1500);

    } catch (error) {
      setFeedback({ message: 'Erro ao enviar o arquivo. Tente novamente.', type: 'danger' });
    } finally {
      setIsUploading(false); // Finaliza o estado de upload
    }
  };

  // Se o usuário não está logado, ele será redirecionado pelo useEffect, 
  // então só precisamos renderizar se 'isLoggedIn' for true.
  if (!isLoggedIn) {
    return null; 
  }

  // Define o conteúdo principal com base no estado 'hasAlreadyUploaded' (simulando o 'elif not already' do Jinja)
  const mainContent = hasAlreadyUploaded ? (
    <Card className="p-4 shadow-sm">
      <h3 className="mb-3 text-success">Análise em Andamento!</h3>
      <p className="lead">Seu arquivo já foi enviado e está sendo processado.</p>
      <p>Você pode conferir os <Button variant="link" onClick={() => navigate('/resultados')}>resultados aqui</Button>.</p>
    </Card>
  ) : (
    <Card className="p-4 shadow-sm" style={{ maxWidth: '600px', width: '100%' }}>
      <h3 className="mb-4">Selecione seu arquivo CSV</h3>
      <p className="text-muted">Formatos aceitos: `.csv` (dados genéticos brutos).</p>
      
      <Form onSubmit={handleSubmit} className="upload-form">
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Control
            type="file"
            name="file"
            accept=".csv"
            onChange={handleFileChange}
            required
            disabled={isUploading}
          />
        </Form.Group>
        
        <Button 
          type="submit" 
          variant="primary" 
          className="w-100 mt-3"
          disabled={isUploading || !selectedFile}
        >
          {isUploading ? 'Analisando DNA...' : 'Analisar meu DNA agora'}
        </Button>
      </Form>
    </Card>
  );

  return (
    <main className="upload-section py-5 text-center flex-grow-1 d-flex align-items-center">
      <Container>
        <h2 className="mb-4">Envie seu arquivo genético</h2>
        <p className="mb-4 text-muted fs-5">
          Faça o upload do seu arquivo CSV para iniciar a análise personalizada.
        </p>
        
        {/* Exibe feedback (sucesso, erro, carregando) */}
        {feedback.message && (
          <Alert variant={feedback.type} className="mb-4 mx-auto" style={{ maxWidth: '600px' }}>
            {feedback.message}
          </Alert>
        )}

        <div className="d-flex justify-content-center">
          {mainContent}
        </div>
        
      </Container>
      <CookieBanner />
    </main>
  );
}

export default CarregarDados;
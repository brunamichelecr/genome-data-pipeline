// src/components/CardDoenca.jsx

import React, { useState } from 'react';
import { Card, Button, Modal, ProgressBar, Col } from 'react-bootstrap';

// Este componente recebe os dados de uma ÚNICA doença via "props"
function CardDoenca({ doenca, delay }) {
  // Hook para controlar a visibilidade do Modal (Janela pop-up)
  const [showModal, setShowModal] = useState(false);

  const handleClose = () => setShowModal(false);
  const handleShow = () => setShowModal(true);

  // Determina a classe da barra de progresso com base na porcentagem
  const getProgressBarVariant = (percent) => {
    if (percent > 80) return 'danger';
    if (percent > 50) return 'warning';
    return 'success';
  };

  // 💡 A coluna (Col) é renderizada AQUI, facilitando o layout
  return (
    <Col md={6} className="mb-4">
      {/* O estilo em linha 'animation-delay' é o que estava no resultados.html */}
      <div className="card-doenca h-100" style={{ animationDelay: `${delay}s` }}> 
        <h4 className="card-title fw-bold">{doenca.name}</h4>
        <p className="card-text text-muted">{doenca.brief}</p>

        {/* Botão para abrir o modal, substituindo data-bs-toggle/target do Bootstrap */}
        <Button variant="info" className="btn-card" onClick={handleShow}>
          Leia mais
        </Button>

        {/* Barra de progresso */}
        <ProgressBar className="mt-3">
          <ProgressBar
            variant={getProgressBarVariant(doenca.percent)}
            now={doenca.percent}
            label={`${doenca.percent}%`}
            key={1}
          />
        </ProgressBar>
      </div>

      {/* Modal - Conectado ao estado 'showModal' */}
      <Modal show={showModal} onHide={handleClose} scrollable>
        <Modal.Header closeButton>
          <Modal.Title className="fw-bold">{doenca.name}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="text-muted">{doenca.desc}</p>
          {/* Adicione outros detalhes da doença aqui, se houver */}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Fechar
          </Button>
        </Modal.Footer>
      </Modal>
    </Col>
  );
}

export default CardDoenca;
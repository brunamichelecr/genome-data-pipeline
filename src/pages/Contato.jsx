// src/pages/Contato.jsx

import React from 'react';
import { Container, Row, Col, ListGroup, Button } from 'react-bootstrap';
// Usamos Link ou a tag <a> normal se o destino for externo ou e-mail
import CookieBanner from '../components/CookieBanner';

function Contato() {
  return (
    <>
      <main className="flex-grow-1 container py-5">
        <div className="text-center mb-5">
          <h1 className="mb-3">Entre em contato</h1>
          <p className="lead">Fique à vontade para me encontrar nas redes ou enviar um e-mail direto:</p>
        </div>

        <Row className="justify-content-center">
          <Col md={6}>
            <ListGroup variant="flush">
              {/* Item: LinkedIn */}
              <ListGroup.Item className="d-flex justify-content-between align-items-center">
                <span>LinkedIn</span>
                <Button 
                  as="a" // Usa Button com estilo, mas como tag <a>
                  href="https://www.linkedin.com/in/brunamcr" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn-navbar-create"
                >
                  Visitar
                </Button>
              </ListGroup.Item>
              
              {/* Item: GitHub */}
              <ListGroup.Item className="d-flex justify-content-between align-items-center">
                <span>GitHub</span>
                <Button 
                  as="a"
                  href="https://github.com/brunamichelecr" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn-navbar-create"
                >
                  Ver projetos
                </Button>
              </ListGroup.Item>
              
              {/* Item: E-mail */}
              <ListGroup.Item className="d-flex justify-content-between align-items-center">
                <span>E-mail</span>
                <Button 
                  as="a"
                  href="mailto:brunamichelecr@gmail.com" 
                  className="btn-navbar-create"
                >
                  Enviar mensagem
                </Button>
              </ListGroup.Item>
              
            </ListGroup>
          </Col>
        </Row>
      </main>
      <CookieBanner />
    </>
  );
}

export default Contato;
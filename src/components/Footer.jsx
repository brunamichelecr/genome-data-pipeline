// src/components/Footer.jsx

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom'; // Usamos o Link para navegação interna

function Footer() {
  return (
    <footer className="footer-custom py-5 mt-auto">
      <Container>
        <Row>
          {/* Mapa do site (Links internos) */}
          <Col md={4} className="mb-4">
            <h5 className="footer-title">Mapa do site</h5>
            <ul className="list-unstyled">
              <li><Link to="/">Início</Link></li>
              <li><Link to="/sobre">Sobre</Link></li>
              <li><Link to="/contato">Contato</Link></li>
              <li><Link to="/carregar-dados">Análise</Link></li>
            </ul>
          </Col>
          {/* Sobre o projeto (Links externos) */}
          <Col md={4} className="mb-4">
            <h5 className="footer-title">Sobre o projeto</h5>
            <ul className="list-unstyled">
              <li>Desenvolvido por Bruna</li>
              <li><a href="https://github.com/brunamichelecr/genome-data-pipeline" target="_blank" rel="noopener noreferrer">Este projeto</a></li>
              <li><a href="https://www.linkedin.com/in/brunamcr" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
              <li><Link to="/creditos">Créditos e tecnologias</Link></li>
            </ul>
          </Col>
          {/* Legal (Links internos) */}
          <Col md={4} className="mb-4">
            <h5 className="footer-title">Legal</h5>
            <ul className="list-unstyled">
              <li><Link to="/aviso-privacidade">Aviso de privacidade</Link></li>
              <li><Link to="/termos-de-uso">Termos de uso</Link></li>
              <li><Link to="/cookies">Cookies</Link></li>
            </ul>
          </Col>
        </Row>
        <hr className="my-4" />
        <div className="text-center small text-muted">
          © 2025 DemoMind. Todos os direitos reservados.
        </div>
      </Container>
    </footer>
  );
}

export default Footer;
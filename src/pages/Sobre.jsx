// src/pages/Sobre.jsx

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
// Link é usado para navegação interna sem recarregar a página
import { Link } from 'react-router-dom';
import CookieBanner from '../components/CookieBanner';

function Sobre() {
  return (
    <>
      <main className="flex-grow-1 container py-5">
        <Row className="justify-content-center">
          <Col lg={8}>
            <h1 className="mb-4 text-center">Quem somos nós</h1>
            <p className="lead">
              O **DemoMind** é criado por **Bruna Michele**,
              engenheira de dados, com foco em saúde personalizada e análise genética.
            </p>
            <p className="lead">
              O projeto transforma arquivos de SNPs em análises claras sobre doenças,
              genes impactados e riscos genéticos.
            </p>
            <p className="lead">
              Integra fontes confiáveis (NCBI, ClinVar, dbSNP) e tecnologias modernas
              (Python, Flask, PostgreSQL, Bootstrap). Código aberto no
              <a href="https://github.com/brunamichelecr/genome-data-pipeline" target="_blank" rel="noopener noreferrer">
                GitHub
              </a>.
            </p>
            <p className="lead">
              Serve como vitrine técnica e convida à reflexão sobre uso ético e seguro
              de dados genéticos.
            </p>
            <h2 className="mt-5">Contato e redes da autora</h2>
            <ul className="list-unstyled mt-3">
              {/* LinkedIn */}
              <li className="mb-2 d-flex align-items-center">
                {/* 💡 Nota: Em React, use tags <img> ou ícones de bibliotecas. 
                Aqui, estamos usando ícones simples para manter a fidelidade. */}
                <img width="24" height="24" src="https://img.icons8.com/color/48/linkedin.png" alt="LinkedIn" className="me-2" />
                <a href="https://www.linkedin.com/in/brunamcr" target="_blank" rel="noopener noreferrer">
                  LinkedIn
                </a>
              </li>
              {/* GitHub */}
              <li className="mb-2 d-flex align-items-center">
                <img width="24" height="24" src="https://img.icons8.com/ios-filled/50/github.png" alt="GitHub" className="me-2" />
                <a href="https://github.com/brunamichelecr" target="_blank" rel="noopener noreferrer">
                  GitHub
                </a>
              </li>
              {/* E-mail */}
              <li className="mb-2 d-flex align-items-center">
                <img width="24" height="24" src="https://img.icons8.com/color/48/gmail-new.png" alt="E-mail" className="me-2" />
                <a href="mailto:brunamichelecr@gmail.com">
                  brunamichelecr@gmail.com
                </a>
              </li>
            </ul>
          </Col>
        </Row>
      </main>
      <CookieBanner />
    </>
  );
}

export default Sobre;
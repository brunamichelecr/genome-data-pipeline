// src/pages/Home.jsx
import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import CookieBanner from '../components/CookieBanner';

function Home() {
  return (
    <>
      {/* 1. Hero Section */}
      <section className="hero-section d-flex align-items-center justify-content-center text-center">
        <div className="hero-overlay">
          <h1 className="hero-title">O que seu DNA revela sobre sua saúde?</h1>
          <p className="hero-subtitle">
            Com base no seu DNA, revelamos predisposições genéticas e
            te ajudamos a entender melhor sua saúde.
          </p>
          <Link to="/carregar-dados" className="btn btn-primary">
            Analisar meu DNA
          </Link>
        </div>
      </section>

      {/* 2. How it Works Section */}
      <section className="how-it-works py-5">
        <Container className="text-center">
          <h2 className="section-title mb-4">Como funciona</h2>
          <p className="section-subtitle mb-5">Três passos simples para a sua análise.</p>
          <Row>
            <Col md={4} className="mb-4">
              <Card className="h-100 p-4">
                <img src="/img/icon1.png" alt="Enviar arquivo" className="how-icon mb-3" />
                <h5 className="fw-bold">1. Envie seu arquivo</h5>
                <p>Faça o upload do seu arquivo de dados genéticos brutos (CSV).</p>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="h-100 p-4">
                <img src="/img/icon5.png" alt="Análise" className="how-icon mb-3" />
                <h5 className="fw-bold">2. Análise</h5>
                <p>Nosso pipeline processa seus SNPs com base em bases de dados confiáveis.</p>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="h-100 p-4">
                <img src="/img/icon4.png" alt="Resultados" className="how-icon mb-3" />
                <h5 className="fw-bold">3. Receba os resultados</h5>
                <p>Visualize predisposições, riscos e recomendações personalizadas.</p>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* 3. Testimonials Section (simplificada) */}
      <section className="testimonials-section py-5 bg-light">
        <Container className="text-center">
          <h2 className="mb-5">Histórias reais, descobertas genéticas</h2>
          <Row className="justify-content-center">
              <Col md={5} lg={4} className="mb-4">
              <Card className="testimonial-card p-4 h-100">
                <img src="/img/homem.jpg" alt="João" className="testimonial-avatar mb-3" />
                <p className="testimonial-text">
                  “João descobriu predisposição genética para intolerância à lactose.”
                </p>
                <span className="testimonial-name">- João, São Paulo</span>
              </Card>
            </Col>
            <Col md={5} lg={4} className="mb-4">
              <Card className="testimonial-card p-4 h-100">
                <img src="/img/mulher.jpg" alt="Maria" className="testimonial-avatar mb-3" />
                <p className="testimonial-text">
                  “Maria identificou SNPs ligados à resposta a medicamentos.”
                </p>
                <span className="testimonial-name">- Maria, Belo Horizonte</span>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>
      <CookieBanner />
    </>
  );
}

export default Home;
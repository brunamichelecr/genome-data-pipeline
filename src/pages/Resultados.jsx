// src/pages/Resultados.jsx

import React, { useState, useEffect } from 'react';
import { Container, Row } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; 
import CardDoenca from '../components/CardDoenca';
import CookieBanner from '../components/CookieBanner';
import { simulatedDiseases } from '../data/SimulatedData'; 

function Resultados() {
  // Estado para armazenar os dados (a lista de doenças)
  const [doencas, setDoencas] = useState([]);
  // Estado para controlar a tela de carregamento
  const [isLoading, setIsLoading] = useState(true);
  
  // Verifica se o usuário está logado
  const { isLoggedIn } = useAuth(); 
  const navigate = useNavigate();

  // 💡 Hook useEffect: Responsável por buscar dados e gerenciar efeitos colaterais
  useEffect(() => {
    // 1. Checagem de Autenticação (Substitui o {% if not session.get('user_id') %} do Jinja)
    if (!isLoggedIn) {
      navigate('/login');
      return; 
    }

    // 2. Simulação de Fetching de API (Substitui a lógica de carregamento do Flask)
    const fetchResults = async () => {
      setIsLoading(true);
      try {
        // Simula o tempo de latência da API (2 segundos)
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // No futuro, aqui você fará o 'fetch' real para a API Flask:
        // const response = await fetch('/api/resultados', { headers: { Authorization: `Bearer ${token}` } });
        
        // Carrega os dados simulados
        setDoencas(simulatedDiseases);
      } catch (error) {
        // Lógica de erro da API
        console.error("Erro ao buscar resultados:", error);
      } finally {
        setIsLoading(false); // Remove o estado de carregamento
      }
    };

    fetchResults();
  }, [isLoggedIn, navigate]); // Dependências: Garante que roda ao logar/deslogar

  // Se a navegação já ocorreu, não renderiza nada
  if (!isLoggedIn) {
    return null; 
  }
  
  return (
    <main className="container resultados-main mt-5 pt-4 flex-grow-1">
      <div className="text-center mb-5">
        <h1 className="mb-3">Resultados da Análise Genética</h1>
        <p className="lead">Achados relacionados ao seu perfil genético.</p>
      </div>
      
      {/* Renderização Condicional: Carregando vs. Dados Prontos */}
      {isLoading ? (
        <div className="text-center py-5">
          <p className="lead">Analisando seus dados genéticos...</p>
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Carregando...</span>
          </div>
        </div>
      ) : doencas.length > 0 ? (
        // 💡 Substitui o {% for d in doencas %} do Jinja pelo .map() do JavaScript
        <Row>
          {doencas.map((doenca, index) => (
            // CardDoenca é o componente reutilizável que criamos antes
            <CardDoenca 
              key={doenca.id} // Chave única é OBRIGATÓRIA ao mapear listas no React
              doenca={doenca} 
              delay={0.2 * (index + 1)} // Replicando o delay incremental do seu CSS
            />
          ))}
        </Row>
      ) : (
        // Caso a lista de doencas esteja vazia
        <div className="text-center py-5">
          <p className="lead text-muted">Nenhum achado significativo encontrado para o seu perfil.</p>
        </div>
      )}

      <CookieBanner />
    </main>
  );
}

export default Resultados;
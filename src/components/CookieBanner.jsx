// src/components/CookieBanner.jsx

import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';

function CookieBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // 💡 Efeito Colateral: Roda apenas uma vez (ao montar o componente)
    // Verifica se o usuário já aceitou
    const accepted = sessionStorage.getItem('cookies_accepted');
    if (!accepted) {
      setIsVisible(true);
    }
  }, []);

  const handleAccept = () => {
    // 💡 Lógica de Estado: Muda o estado e salva no navegador
    setIsVisible(false);
    sessionStorage.setItem('cookies_accepted', 'true');
  };

  // Renderização Condicional: Se não for visível, retorna null (não renderiza nada)
  if (!isVisible) {
    return null;
  }

  return (
    <div className="cookie-banner fixed-bottom p-3 d-flex justify-content-center align-items-center">
      Este site utiliza cookies para melhorar sua experiência. <a href="/cookies">Saiba mais</a>
      <Button variant="primary" size="sm" onClick={handleAccept} className="ms-2">
        Aceitar
      </Button>
    </div>
  );
}

export default CookieBanner;
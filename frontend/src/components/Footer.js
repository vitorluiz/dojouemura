// src/components/Footer.js

import React from 'react';
import { Link } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import empresaService from '../services/empresaService';
import LoadingSpinner from './LoadingSpinner';
import './Footer.css';

function Footer() {
  const { data: dojoInfo, loading, error } = useApi(
    () => empresaService.obterInformacoes(),
    [],
    true
  );

  const currentYear = new Date().getFullYear();

  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-section about">
          <h2 className="footer-logo-text">Dojô Uemura</h2>
          <p>
            Ensinando a arte suave com disciplina, respeito e dedicação.
          </p>
          <div className="contact">
            {loading && <LoadingSpinner size="small" message="Carregando contatos..." />}
            {error && (
              <span style={{ color: '#ff6b6b', fontSize: '12px' }}>
                Erro ao carregar informações de contato
              </span>
            )}
            {dojoInfo && !loading && (
              <>
                <span><i className="fas fa-phone"></i> &nbsp; {dojoInfo.telefone}</span>
                <span><i className="fas fa-envelope"></i> &nbsp; {dojoInfo.email}</span>
              </>
            )}
          </div>
        </div>

        <div className="footer-section links">
          <h2>Links Rápidos</h2>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/inscricao">Inscrição</Link></li>
            <li><Link to="/contato">Contato</Link></li>
          </ul>
        </div>

        <div className="footer-section social">
          <h2>Siga-nos</h2>
          <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
          <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer">Instagram</a>
        </div>
      </div>

      <div className="footer-bottom">
        <span>&copy; {currentYear} Dojô Uemura | Todos os direitos reservados.</span>
        <span className="credits">
          Feito com ❤️ por <a href="https://www.vnetworks.com.br" target="_blank" rel="noopener noreferrer">VNetWorks</a>
        </span>
      </div>
    </footer>
  );
}

export default Footer;
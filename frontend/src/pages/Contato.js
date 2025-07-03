// src/pages/Contato.js

import React from 'react';
import { useApi } from '../hooks/useApi';
import empresaService from '../services/empresaService';
import LoadingSpinner from '../components/LoadingSpinner';
import './Contato.css';

function Contato() {
  const { data: dojoInfo, loading, error } = useApi(
    () => empresaService.obterInformacoes(),
    [],
    true
  );

  // Mapa do Google Maps. Pode ser atualizado no futuro para usar dados da API também.
  const mapUrl = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3703.111818120658!2d-55.74850588562144!3d-15.452669489182392!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9378c77399628383%3A0x3c55c82a5633e94!2sDoj%C3%B4%20Uemura!5e1!3m2!1spt-BR!2sbr!4v1688173491228!5m2!1spt-BR!2sbr";

  if (loading) {
    return (
      <div className="contato-container">
        <LoadingSpinner size="large" message="Carregando informações de contato..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="contato-container">
        <h2>Entre em Contato</h2>
        <div className="error-message" style={{
          padding: '20px',
          backgroundColor: '#f8d7da',
          color: '#721c24',
          border: '1px solid #f5c6cb',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          <p>Erro ao carregar informações de contato. Por favor, tente novamente mais tarde.</p>
          <p>Em caso de urgência, entre em contato pelo telefone: (65) 98111-1125</p>
        </div>
      </div>
    );
  }

  if (!dojoInfo) {
    return (
      <div className="contato-container">
        <h2>Entre em Contato</h2>
        <p>Informações não disponíveis no momento.</p>
      </div>
    );
  }

  // Constrói o endereço completo a partir dos dados da API
  const enderecoCompleto = `${dojoInfo.logradouro}, Nº ${dojoInfo.numero}, ${dojoInfo.complemento}`;
  const cidadeEstadoCEP = `${dojoInfo.bairro} - ${dojoInfo.municipio}/${dojoInfo.uf} - CEP: ${dojoInfo.cep}`;

  return (
    <div className="contato-container">
      <h2>Entre em Contato</h2>
      <div className="contato-content">
        <div className="contato-info">
          <h3>{dojoInfo.nome_fantasia}</h3>
          <p>{enderecoCompleto}</p>
          <p>{cidadeEstadoCEP}</p>
          <br/>
          <h3>Telefone</h3>
          <p>
            <a href={`tel:${dojoInfo.telefone.replace(/\D/g, '')}`} style={{ color: '#8B0000', textDecoration: 'none' }}>
              {dojoInfo.telefone}
            </a>
          </p>
          <br/>
          <h3>Email</h3>
          <p>
            <a href={`mailto:${dojoInfo.email}`} style={{ color: '#8B0000', textDecoration: 'none' }}>
              {dojoInfo.email}
            </a>
          </p>
        </div>
        <div className="contato-mapa">
          <iframe
            src={mapUrl}
            width="100%"
            height="450"
            style={{ border: 0 }}
            allowFullScreen=""
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
            title={`Localização do ${dojoInfo.nome_fantasia}`}
          ></iframe>
        </div>
      </div>
    </div>
  );
}

export default Contato;
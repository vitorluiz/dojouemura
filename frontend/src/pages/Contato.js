// src/pages/Contato.js

import React, { useState, useEffect } from 'react';
import { fetchDojoInfo } from '../api/dojoApi'; // Importamos nossa função da API
import './Contato.css';

function Contato() {
  const [dojoInfo, setDojoInfo] = useState(null); // Estado para guardar os dados
  
  // Efeito que busca os dados quando a página carrega
  useEffect(() => {
    fetchDojoInfo().then(data => {
      setDojoInfo(data);
    });
  }, []); // O array vazio [] garante que isso rode apenas uma vez

  // Mapa do Google Maps. Pode ser atualizado no futuro para usar dados da API também.
  const mapUrl = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3703.111818120658!2d-55.74850588562144!3d-15.452669489182392!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9378c77399628383%3A0x3c55c82a5633e94!2sDoj%C3%B4%20Uemura!5e1!3m2!1spt-BR!2sbr!4v1688173491228!5m2!1spt-BR!2sbr";

  // Mostra uma mensagem de "carregando" enquanto os dados não chegam
  if (!dojoInfo) {
    return <div className="contato-container"><h2>Carregando informações...</h2></div>;
  }

  // Constrói o endereço completo a partir dos dados da API
  const enderecoCompleto = `${dojoInfo.logradouro}, Nº ${dojoInfo.numero}, ${dojoInfo.complemento}`;
  const cidadeEstadoCEP = `${dojoInfo.bairro} - ${dojoInfo.municipio}/${dojoInfo.uf} - CEP: ${dojoInfo.cep}`;

  return (
    <div className="contato-container">
      <h2>Entre em Contato</h2>
      <div className="contato-content">
        <div className="contato-info">
          <h3>{dojoInfo.nomeFantasia}</h3>
          <p>{enderecoCompleto}</p>
          <p>{cidadeEstadoCEP}</p>
          <br/>
          <h3>Telefone</h3>
          <p>{dojoInfo.telefone}</p>
          <br/>
          <h3>Email</h3>
          <p>{dojoInfo.email}</p>
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
            title={`Localização do ${dojoInfo.nomeFantasia}`}
          ></iframe>
        </div>
      </div>
    </div>
  );
}

export default Contato;
// src/pages/Home.js

import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

// 1. Importamos a imagem diretamente. 
//    Certifique-se de que o caminho e o nome do arquivo estão corretos.
import dojoHeroImage from '../assets/images/banner-hero.webp';

function Home() {
  // 2. Criamos um objeto de estilo para aplicar a imagem como fundo.
  const heroStyles = {
    backgroundImage: `url(${dojoHeroImage})`
  };

  return (
    // 3. Aplicamos o estilo diretamente no container do banner.
    //    A tag <img> foi REMOVIDA daqui.
    <div className="home-hero" style={heroStyles}>
      <div className="hero-text">
        <h1>Dojô Eumura</h1>
        <p>Jiu-Jitsu Arte Suave</p>
        <Link to="/inscricao" className="cta-button">
          Faça sua Inscrição
        </Link>
      </div>
    </div>
  );
}

export default Home;
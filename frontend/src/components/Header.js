// src/components/Header.js

import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import './Header.css'; // Importa o nosso novo arquivo de CSS
import brandLogo from '../assets/images/brand.png'; // Importa a sua logo

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLinkClick = () => {
    setMenuOpen(false);
  };

  return (
    <header className="app-header">
      <div className="header-content">
        <Link to="/" className="brand-link" onClick={handleLinkClick}>
          <img src={brandLogo} alt="Logo Dojô Eumura" className="brand-logo" />
          <span className="brand-name">Dojô Eumura</span>
        </Link>

        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? '✕' : '☰'}
        </button>

        <nav className={`main-nav ${menuOpen ? 'open' : ''}`}>
          <ul>
            <li>
              <NavLink to="/" onClick={handleLinkClick}>Home</NavLink>
            </li>
            <li>
              <NavLink to="/inscricao" onClick={handleLinkClick}>Inscrição</NavLink>
            </li>
            <li>
              <NavLink to="/contato" onClick={handleLinkClick}>Contato</NavLink>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
// src/components/LoadingSpinner.js

import React from 'react';
import './LoadingSpinner.css';

/**
 * Componente de loading spinner reutilizável
 */
const LoadingSpinner = ({ size = 'medium', message = 'Carregando...' }) => {
  return (
    <div className={`loading-spinner-container ${size}`}>
      <div className="loading-spinner"></div>
      {message && <p className="loading-message">{message}</p>}
    </div>
  );
};

export default LoadingSpinner;


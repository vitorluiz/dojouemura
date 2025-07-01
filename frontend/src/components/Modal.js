// src/components/Modal.js
import React from 'react';
import ReactMarkdown from 'react-markdown';
import './Modal.css';

function Modal({ isOpen, onClose, onAccept, title, children }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h4 className="modal-title">{title}</h4>
          <button onClick={onClose} className="modal-close-btn">&times;</button>
        </div>
        <div className="modal-body">
          <div className="modal-text">
            <ReactMarkdown>{children}</ReactMarkdown>
          </div>
        </div>
        <div className="modal-footer">
          <button onClick={onAccept} className="modal-accept-btn">Li e Aceito</button>
        </div>
      </div>
    </div>
  );
}

export default Modal;
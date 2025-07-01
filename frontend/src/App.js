// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header'; // Importamos o cabeçalho
import Footer from './components/Footer'; // Importamos nosso novo rodapé
import Home from './pages/Home';
import Inscricao from './pages/Inscricao';
import Contato from './pages/Contato';
import './App.css'; 

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />

        <main className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/inscricao" element={<Inscricao />} />
            <Route path="/contato" element={<Contato />} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
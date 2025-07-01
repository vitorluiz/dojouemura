// src/pages/Inscricao.js

import React, { useState, useEffect } from 'react';
import Modal from '../components/Modal';
import { IMaskInput } from 'react-imask';
import './Inscricao.css';

const FORM_DRAFT_KEY = 'dojo-inscricao-draft';

const getInitialState = (key, defaultValue) => {
  try {
    const savedData = localStorage.getItem(FORM_DRAFT_KEY);
    if (savedData) {
      const parsedData = JSON.parse(savedData);
      return parsedData[key] || defaultValue;
    }
  } catch (error) {
    console.error("Falha ao ler o rascunho do formulário.", error);
    return defaultValue;
  }
  return defaultValue;
};

const initialDependenteState = {
  nomeCompleto: '', cpf: '', dataNascimento: '', parentesco: '', foto: null,
  escolaNome: '', escolaSerie: '', escolaPeriodo: 'Manhã',
  planoSaudeQual: '', alergiasQuais: '', medicamentosQuais: '', condicoesMedicas: '',
  emergenciaNome: '', emergenciaTelefone: '',
  historicoEsportivo: [],
  termos: { responsabilidade: false, imagem: false, medica: false }
};

const initialResponsavelState = {
  cpf: '', rg: '', nomeCompleto: '', telefone: '', email: '',
};

const initialEnderecoState = {
  logradouro: '', numero: '', complemento: '', bairro: '', localidade: '', uf: '',
};

const fetchTermoTextFromAPI = (termoId) => {
  return fetch(`/api/v1/termos/${termoId}/`)
    .then(response => {
      if (!response.ok) { throw new Error(`Termo '${termoId}' não encontrado na API.`); }
      return response.json();
    })
    .then(data => data)
    .catch(error => {
      console.error('Erro ao buscar o texto do termo da API:', error);
      return {
        titulo: "Erro ao Carregar",
        conteudo: `Ocorreu um erro ao carregar o texto do termo. Por favor, tente novamente.`
      };
    });
};

function Inscricao() {
  const [responsavel, setResponsavel] = useState(() => getInitialState('responsavel', initialResponsavelState));
  const [endereco, setEndereco] = useState(() => getInitialState('endereco', initialEnderecoState));
  const [cep, setCep] = useState(() => getInitialState('cep', ''));
  const [dependentes, setDependentes] = useState(() => getInitialState('dependentes', []));
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalContent, setModalContent] = useState({ title: '', text: '' });
  const [activeTermoInfo, setActiveTermoInfo] = useState({ dependentIndex: null, termoId: null });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState({ message: '', type: '' });

  useEffect(() => {
    if (!isSubmitting) {
      const draftData = { responsavel, endereco, cep, dependentes };
      localStorage.setItem(FORM_DRAFT_KEY, JSON.stringify(draftData));
    }
  }, [responsavel, endereco, cep, dependentes, isSubmitting]);

  const isSubmitDisabled =
    dependentes.length === 0 || isSubmitting || !dependentes.every(dep => dep.termos.responsabilidade && dep.termos.imagem && dep.termos.medica);

  const handleOpenModal = async (dependentIndex, termoId) => {
    setActiveTermoInfo({ dependentIndex, termoId });
    setModalContent({ title: "Carregando...", text: 'Buscando termo...' });
    setIsModalOpen(true);
    const { titulo, conteudo } = await fetchTermoTextFromAPI(termoId);
    setModalContent({ title: titulo, text: conteudo });
  };

  const handleCloseModal = () => setIsModalOpen(false);

  const handleAcceptTermo = () => {
    const { dependentIndex, termoId } = activeTermoInfo;
    if (dependentIndex !== null && termoId) {
      const novosDependentes = dependentes.map((dep, index) => {
        if (index === dependentIndex) {
          return { ...dep, termos: { ...dep.termos, [termoId]: true } };
        }
        return dep;
      });
      setDependentes(novosDependentes);
    }
    handleCloseModal();
  };
  
  const handleResponsavelChange = (e) => setResponsavel({ ...responsavel, [e.target.name]: e.target.value });
  const handleEnderecoChange = (e) => setEndereco({ ...endereco, [e.target.name]: e.target.value });
  const handleDependenteChange = (index, e) => {
    const { name, value } = e.target;
    const novosDependentes = dependentes.map((dependente, i) => {
      if (i === index) { return { ...dependente, [name]: value }; }
      return dependente;
    });
    setDependentes(novosDependentes);
  };
  const handleAddDependente = () => setDependentes([...dependentes, { ...initialDependenteState, historicoEsportivo: [] }]);
  const handleRemoveDependente = (index) => setDependentes(dependentes.filter((_, i) => i !== index));
  
  const resetForm = () => {
      setResponsavel(initialResponsavelState);
      setEndereco(initialEnderecoState);
      setCep('');
      setDependentes([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFeedback({ message: '', type: '' });

    const formData = {
      responsavel: {
        cpf: responsavel.cpf,
        rg: responsavel.rg,
        nome_completo: responsavel.nomeCompleto,
        telefone: responsavel.telefone,
        email: responsavel.email,
      },
      endereco: {
        logradouro: endereco.logradouro,
        numero: endereco.numero,
        complemento: endereco.complemento,
        bairro: endereco.bairro,
        localidade: endereco.localidade,
        uf: endereco.uf,
      },
      cep: cep,
      dependentes: dependentes.map(dep => ({
        nome_completo: dep.nomeCompleto,
        cpf: dep.cpf,
        data_nascimento: dep.dataNascimento,
        parentesco: dep.parentesco,
        escola_nome: dep.escolaNome,
        escola_serie: dep.escolaSerie,
        escola_periodo: dep.escolaPeriodo,
        plano_saude_qual: dep.planoSaudeQual,
        alergias_quais: dep.alergiasQuais,
        medicamentos_quais: dep.medicamentosQuais,
        condicoes_medicas: dep.condicoesMedicas,
        contato_emergencia_nome: dep.emergenciaNome,
        contato_emergencia_telefone: dep.emergenciaTelefone,
        historico_esportivo: dep.historicoEsportivo,
      }))
    };
    
    try {
      const response = await fetch('/api/v1/inscricoes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || 'Ocorreu um erro ao enviar a inscrição.');
      }

      setFeedback({ message: 'Inscrição enviada com sucesso! O responsável receberá um e-mail de confirmação em breve.', type: 'success' });
      localStorage.removeItem(FORM_DRAFT_KEY);
      resetForm();

    } catch (error) {
      console.error('Falha ao enviar inscrição:', error);
      setFeedback({ message: `Erro: ${error.message}`, type: 'error' });
    
    } finally {
      setIsSubmitting(false);
    }
  };

  useEffect(() => {
    const cepNumerico = cep.replace(/\D/g, '');
    if (cepNumerico.length === 8) {
      fetch(`https://viacep.com.br/ws/${cepNumerico}/json/`)
        .then((res) => res.json())
        .then((data) => {
          if (!data.erro) {
            setEndereco(prev => ({
              ...prev,
              logradouro: data.logradouro || prev.logradouro,
              bairro: data.bairro || prev.bairro,
              localidade: data.localidade,
              uf: data.uf
            }));
          }
        });
    }
  }, [cep]);
  
  const calculateAge = (dataNascimento) => {
    if (!dataNascimento) return '';
    const today = new Date();
    const birthDate = new Date(dataNascimento);
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) { age--; }
    return age >= 0 ? age : '';
  };

  return (
    <div className="inscricao-container">
      <h2>Formulário de Inscrição</h2>
      
      {feedback.message && (
        <div className={`feedback-message ${feedback.type}`}>
          {feedback.message}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Seção do Responsável */}
        <div className="form-section">
          <h3>Responsável</h3>
          <div className="form-grid">
            <input type="text" name="nomeCompleto" placeholder="Nome Completo" value={responsavel.nomeCompleto} onChange={handleResponsavelChange} required />
            <IMaskInput mask="000.000.000-00" value={responsavel.cpf} name="cpf" placeholder="CPF" required className="form-control" onAccept={(value) => handleResponsavelChange({ target: { name: 'cpf', value } })} />
            <input type="text" name="rg" placeholder="RG" value={responsavel.rg} onChange={handleResponsavelChange} required />
            <IMaskInput mask="(00) 00000-0000" value={responsavel.telefone} name="telefone" placeholder="Telefone" required className="form-control" onAccept={(value) => handleResponsavelChange({ target: { name: 'telefone', value } })} />
            <input type="email" name="email" placeholder="Email" value={responsavel.email} onChange={handleResponsavelChange} required />
          </div>
        </div>

        {/* Seção de Endereço */}
        <div className="form-section">
          <h3>Endereço</h3>
          <div className="form-grid-address">
            <IMaskInput mask="00000-000" value={cep} name="cep" placeholder="CEP" required className="form-control cep" onAccept={(value) => setCep(value)} />
            <input className="logradouro" type="text" name="logradouro" placeholder="Logradouro (Rua, Av.)" value={endereco.logradouro} onChange={handleEnderecoChange} required />
            <input className="numero" type="text" name="numero" placeholder="Nº" value={endereco.numero} onChange={handleEnderecoChange} required />
            <input className="bairro" type="text" name="bairro" placeholder="Bairro" value={endereco.bairro} onChange={handleEnderecoChange} required />
            <input className="complemento" type="text" name="complemento" placeholder="Complemento (Apto, Bloco)" value={endereco.complemento} onChange={handleEnderecoChange} />
            <input className="cidade" type="text" name="localidade" placeholder="Cidade" value={endereco.localidade} readOnly />
            <input className="uf" type="text" name="uf" placeholder="UF" value={endereco.uf} readOnly />
          </div>
        </div>
        
        {/* Seção de Dependentes */}
        <div className="form-section">
          <h3>Dependentes</h3>
          {dependentes.map((dependente, index) => (
            <div key={index} className="dependente-card">
              <h4>Dependente {index + 1}</h4>
              <button type="button" className="remove-btn" onClick={() => handleRemoveDependente(index)}>Remover</button>
              
              {/* Dados Pessoais do Dependente */}
              <div className="form-grid">
                <input type="text" name="nomeCompleto" placeholder="Nome Completo do Dependente" value={dependente.nomeCompleto} onChange={(e) => handleDependenteChange(index, e)} required />
                <IMaskInput mask="000.000.000-00" value={dependente.cpf} name="cpf" placeholder="CPF do Dependente" className="form-control" onAccept={(value) => handleDependenteChange(index, { target: { name: 'cpf', value } })} />
                <input type="text" name="parentesco" placeholder="Parentesco" value={dependente.parentesco} onChange={(e) => handleDependenteChange(index, e)} required />
                <div><label>Data de Nascimento</label><input type="date" name="dataNascimento" value={dependente.dataNascimento} onChange={(e) => handleDependenteChange(index, e)} required /></div>
                <div><label>Idade</label><input type="number" value={calculateAge(dependente.dataNascimento)} readOnly /></div>
              </div>

              <h5>Dados Escolares</h5>
              <div className="form-grid">
                <input type="text" name="escolaNome" placeholder="Nome da Escola" value={dependente.escolaNome} onChange={(e) => handleDependenteChange(index, e)} />
                <select name="escolaSerie" value={dependente.escolaSerie} onChange={(e) => handleDependenteChange(index, e)} required>
                    <option value="" disabled>Selecione a série</option>
                    <optgroup label="Ensino Básico: 1º Ciclo">
                        <option value="1º ano">1º ano</option><option value="2º ano">2º ano</option><option value="3º ano">3º ano</option><option value="4º ano">4º ano</option>
                    </optgroup>
                    <optgroup label="Ensino Básico: 2º Ciclo">
                        <option value="5º ano">5º ano</option><option value="6º ano">6º ano</option>
                    </optgroup>
                    <optgroup label="Ensino Básico: 3º Ciclo">
                        <option value="7º ano">7º ano</option><option value="8º ano">8º ano</option><option value="9º ano">9º ano</option>
                    </optgroup>
                    <optgroup label="Ensino Secundário">
                        <option value="10º ano">10º ano</option><option value="11º ano">11º ano</option><option value="12º ano">12º ano</option>
                    </optgroup>
                </select>
                <select name="escolaPeriodo" value={dependente.escolaPeriodo} onChange={(e) => handleDependenteChange(index, e)}>
                    <option value="Manhã">Manhã</option><option value="Tarde">Tarde</option><option value="Noite">Noite</option><option value="Integral">Integral</option>
                </select>
              </div>
              
              <h5>Dados Médicos</h5>
              <div className="form-grid">
                <input type="text" name="planoSaudeQual" placeholder="Plano de Saúde (se houver)" value={dependente.planoSaudeQual} onChange={(e) => handleDependenteChange(index, e)} />
                <input type="text" name="alergiasQuais" placeholder="Alergias (se houver)" value={dependente.alergiasQuais} onChange={(e) => handleDependenteChange(index, e)} />
                <input type="text" name="medicamentosQuais" placeholder="Medicamentos (se houver)" value={dependente.medicamentosQuais} onChange={(e) => handleDependenteChange(index, e)} />
                <textarea name="condicoesMedicas" placeholder="Outras condições médicas" value={dependente.condicoesMedicas} onChange={(e) => handleDependenteChange(index, e)} />
              </div>
              
              {/* Termos */}
              <div className="termos-section-dependente">
                <h5>Termos e Condições</h5>
                <div className="form-group-checkbox"><input type="checkbox" checked={dependente.termos.responsabilidade} readOnly /><span className="term-link" onClick={() => handleOpenModal(index, 'responsabilidade')}>Eu li e aceito o Termo de Responsabilidade.</span></div>
                <div className="form-group-checkbox"><input type="checkbox" checked={dependente.termos.imagem} readOnly /><span className="term-link" onClick={() => handleOpenModal(index, 'imagem')}>Eu li e aceito o Termo de Direito de Imagem.</span></div>
                <div className="form-group-checkbox"><input type="checkbox" checked={dependente.termos.medica} readOnly /><span className="term-link" onClick={() => handleOpenModal(index, 'medica')}>Eu li e aceito o Termo de Condição Médica.</span></div>
              </div>
            </div>
          ))}
          <button type="button" className="add-btn" onClick={handleAddDependente}>+ Adicionar Dependente</button>
        </div>

        <button type="submit" className="submit-btn" disabled={isSubmitDisabled}>
          {isSubmitting ? 'Enviando...' : 'Enviar Inscrição'}
        </button>
      </form>

      {/* CORREÇÃO FINAL: Passamos o texto diretamente para o Modal. O Modal.js é responsável pelo ReactMarkdown. */}
      <Modal isOpen={isModalOpen} onClose={handleCloseModal} onAccept={handleAcceptTermo} title={modalContent.title}>
        {modalContent.text}
      </Modal>
    </div>
  );
}

export default Inscricao;

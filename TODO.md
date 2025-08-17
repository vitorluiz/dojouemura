# 📋 TODO - SISTEMA DOJÔ UEMURA

## 🎯 **OBJETIVO PRINCIPAL**
Implementar sistema completo de matrículas para projeto social e modalidades pagas do Dojô Uemura.

---

## ✅ **CONCLUÍDO**

### **1. Estrutura Base**
- [x] Modelo Usuario com tipos de conta (RESPONSAVEL, PROFESSOR, GESTOR, FUNCIONARIO)
- [x] Modelo Dependente com campos de matrícula
- [x] Modelos para choices (Modalidade, TipoMatricula, StatusMatricula)
- [x] Campo email_verificado no Usuario
- [x] Admin Django configurado para todos os modelos
- [x] Migrações criadas e aplicadas
- [x] Dados iniciais criados (modalidades, tipos, status)

### **2. Formulários e Templates**
- [x] DependenteForm atualizado com campos de matrícula
- [x] Template cadastrar_dependente.html atualizado
- [x] Dashboard atualizado para mostrar informações de matrícula
- [x] Template matricula_projeto_social.html criado
- [x] URLs organizadas para diferentes tipos de matrícula

---

## 🚧 **EM ANDAMENTO**

### **3. Views e Lógica de Negócio**
- [ ] Implementar view `matricula_projeto_social`
- [ ] Implementar view `matricula_modalidade_paga`
- [ ] Atualizar view `cadastrar_dependente` para usar novos campos
- [ ] Validações específicas por tipo de matrícula

---

## 📋 **PRÓXIMOS PASSOS**

### **4. Views Específicas (PRIORIDADE ALTA)**
- [ ] **View: matricula_projeto_social**
  - Formulário específico para projeto social
  - Validações de idade (6-18 anos)
  - Validações de escola obrigatória
  - Taxa de inscrição R$ 50,00
  
- [ ] **View: matricula_modalidade_paga**
  - Formulário para modalidades pagas
  - Escolha de modalidade obrigatória
  - Validações de idade (a partir de 6 anos)
  - Sistema de mensalidades

- [ ] **View: cadastrar_dependente atualizada**
  - Integrar com novos campos de matrícula
  - Validações condicionais por tipo
  - Processamento automático de dados

### **5. Sistema de Validações (PRIORIDADE ALTA)**
- [ ] **Validações de Projeto Social**
  - Idade entre 6-18 anos
  - Escola regular obrigatória
  - Termos obrigatórios
  
- [ ] **Validações de Modalidade Paga**
  - Idade a partir de 6 anos
  - Modalidade obrigatória
  - Termos opcionais

### **6. Sistema de Pagamentos (PRIORIDADE MÉDIA)**
- [ ] **Integração com PIX**
  - Geração de QR Code PIX
  - Validação de pagamento
  - Webhook de confirmação
  
- [ ] **Sistema de Boletos**
  - Geração de boletos bancários
  - Controle de vencimento
  - Status de pagamento

### **7. Notificações e Comunicação (PRIORIDADE MÉDIA)**
- [ ] **Email automático**
  - Confirmação de matrícula
  - Instruções de pagamento
  - Status de aprovação
  
- [ ] **SMS (futuro)**
  - Lembretes de pagamento
  - Confirmações importantes

### **8. Controle de Frequência (PRIORIDADE BAIXA)**
- [ ] **Sistema de QR Code**
  - Geração de QR para cada dependente
  - Leitor na portaria
  - Registro de entrada/saída
  
- [ ] **Notificações em tempo real**
  - Para responsáveis
  - Para professores

### **9. Relatórios e Analytics (PRIORIDADE BAIXA)**
- [ ] **Dashboard do Gestor**
  - Total de matrículas por tipo
  - Receita mensal
  - Frequência dos alunos
  
- [ ] **Relatórios financeiros**
  - Inadimplência
  - Projeções de receita
  - Histórico de pagamentos

---

## 🛠️ **TECNOLOGIAS E FERRAMENTAS**

### **Backend**
- [x] Django 5.2.4
- [x] SQLite (desenvolvimento)
- [ ] Django REST Framework (futuro)
- [ ] Celery (para tarefas assíncronas)

### **Frontend**
- [x] Bootstrap 5
- [x] JavaScript vanilla
- [ ] QR Code Scanner (futuro)
- [ ] PWA capabilities (futuro)

### **Integrações**
- [ ] API PIX (Banco Central)
- [ ] Serviços de email (SendGrid, etc.)
- [ ] Serviços de SMS (Twilio, etc.)

---

## 📅 **CRONOGRAMA ESTIMADO**

### **Semana 1-2: Views e Validações**
- [ ] Implementar views de matrícula
- [ ] Sistema de validações
- [ ] Testes básicos

### **Semana 3-4: Sistema de Pagamentos**
- [ ] Integração PIX
- [ ] Sistema de boletos
- [ ] Controle financeiro

### **Semana 5-6: Notificações e UX**
- [ ] Emails automáticos
- [ ] Melhorias na interface
- [ ] Testes de usuário

### **Semana 7-8: Funcionalidades Avançadas**
- [ ] Controle de frequência
- [ ] Relatórios
- [ ] Documentação

---

## 🚨 **PROBLEMAS IDENTIFICADOS**

### **Urgente**
- [x] ~~Views faltando para novas URLs~~
- [x] ~~Campos de matrícula não implementados~~

### **Para Resolver**
- [ ] Validações específicas por tipo de matrícula
- [ ] Sistema de pagamentos
- [ ] Notificações automáticas

---

## 📝 **NOTAS IMPORTANTES**

- **Arquitetura**: Manter app `usuarios` único (decisão tomada)
- **Banco**: Usar ForeignKey para choices (flexibilidade via admin)
- **Frontend**: Manter simplicidade, focar na experiência do usuário
- **Segurança**: Implementar validações robustas no backend

---

**Status**: 🚧 Em Desenvolvimento  
**Última Atualização**: {{ date.today().strftime('%d/%m/%Y') }}  
**Próxima Reunião**: Implementar views de matrícula


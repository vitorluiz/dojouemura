
O SISTEMA DE GESTÃO DO DOJÔ UEMURA, PERMITE AO GESTOR TER A VISÃO MACRO DO SEU NEGOCIO.
O DOJÔ UEMURA CONTA COM OFERTAS DE AULAS GRATUIRAS DE JIU-JITSU PARA CRIANÇAS E ADOLECENETES DE 6 A 18 ANOS. OFERECE OUTRA MODALIDADES DE ESPORTES COMO JUDÔ, MUAY THAI, PARA CRIANÇAS E ADULTOS COM MENSALIDADES QUE CABEM NO BOLSO. 
TEMOS AGENDAS NOS 3 PERIODOS PARA ATENDER A TODOS A TODA SOCIEDADE CHAPADENSE.
O CADASTRO PARA TURMAS DE JIU-JITSU SÃO REALIZADAS VIA WEB, PELO SITE DO DOJÔ EM PERIODOS DE INSCRIÇÃO ABERTOS. NOSSAS TURMAS TEM X ALUNOS, NOSSOS PROFESSORES SÃO GRADUADOS.
PARA OS PAIS E RESPONSÁVEL TEMOS O CONTROLE DE FREQUENCIA DO SEU FILHO, QUE ENVIA A NOTIFICAÇÃO QUANDO SEU FILHO ENTRA E SAI DO DOJO. 
O RESPONSÁVEL PODERÁ ACOMPANHAR O SEU DEPENDENTE AO VIVO, NA HORA SUA AULA. ATRAVES DO NOSSO PORTAL DO ALUNO. 
PARA ALUNOS QUE DESEJAM SER ALUNOS MENSALISTA PODEM SOLICITAR SUA AULA NO SITE, ASSIM PODERÁ MARCAR SUA AULA.
O PROCESSO É SIMPLES NO NOSSO SITE EM AGENDAMENTO INFORME SEU EMAIL VOCE RECEBERÁ UMA SENHA QUE EXPIRA EM 24 HORAS, FAÇA O SEU AGENDAMENTO E RECEBER O CÓDIGO PARA SUA AULA EXPERIMENTAL.
QUER SER ALUNO FALE COM NOSSOS COLABORADORES QUE TEREMOS O MAIRO PRAZER EM TER VOCE COMO NOSSO ALUNO.
ATENÇÃO O PROJETO SOCIAL SÓ PODEM PARTICIPAR CRIANÇAS E ADOLECENTES DE 06 A 18 ANOS, MATRICULADOS NA ESCOLA RELUGAR E OBRIGATORIAMENTE SER MATRICULADO POR SEU RESPONSÁVEL LEGAL. 
TEREMOS UMA CARTEIRA DO ATLETA QUE IDENTICARA O ALUNO COM UM CÓDIGO ALFANUMERICO DE 10 DIGITOS QUE SERÁ GERADO UM QRCODE PARA FACILITAR A SUA LEITURA, IREMOS DISPONIBILIZAR UMA LEITOR NA PORTARIA QUE FARA A SUA LEITURA E PERMISSÃO PARA REALIZAR AS AULAS, AO ALUNOS MENSALISTA SERÁ REALIZADO O CONTROLE DA FREQUENCIA E MENSALIDADES POR ESTE QR. TODOS OS ALUNOS DEVEM TER SUA FOTO NO CARTÃO DO ATLETA. DADOS MÉDICOS COMO TIPO SANGUINEO E ALERGIAS, CONDIÇÕES MÉDICAS, QUE OS PROFESSORES DEVEM SABER. SEU CONTATO DE EMERGENCIA.  SE É INICIANTE OU JÁ PRATICANTE DE ESPORTES. 
NOSSOS PROFESSORES TERAM ACESSO AS AULAS PODENDO GERENCIA ALUNOS MATRICULADOS EM SUA AULA, MANDAR NOTIFICAÇÕES PARA OS RESPONSÁVEIS E ALUNOS MENSALISTA MATRICULADOS NA TURMA. 
TEMOS UMA GALERIA DE FOTOS DOS EVENTOS E CAMPEONATOS DO DOJÔ. 


# INSCRIÇÃO DO PROJETO SOCIAL

- realizar sua inscrição no periodo de inscrição
- ser menor de idade, (06 - 18 anos);
- ter uma responsável legal;
- estar matriculado e frequentando escola regular;
- não ter restrições médicas que proibem a prática do esporte;
- aceitar os termos de responsabilidade, uso de imagem, condições médicas.
- pagar a taxa de inscrição R$ 50,00.

# INSCRIÇÃO POR MODALIDADE

- realizar sua inscrição no site;
- apartir de 06 anos;
- ser ou ter responsável financeiro;
- não ter restrições médicas que proibem a prática do esporte;
- aceitar os termos de responsabilidade, condições médicas, uso de imagem (opcional);
- realizar o pagamento da mensalidade da modalidade que escolheu e confeção do cartão do atleta.

### Municipais
- Escola Municipal Água Branca
- Escola Municipal Casca III
- Escola Municipal Córrego do Campo
- Escola Municipal Cristo Rei
- Escola Municipal JJ
- Escola Municipal Monteiro Lobato
- Escola Municipal Professor Jacondino Bezerra
- Escola Municipal Professora Abinel Freitas Pereira
- Escola Municipal Professora Elba Xavier Ferreira
- Escola Municipal Professora Irene Ferreira da Silva
- Escola Municipal Professora Maria Luiza de Araújo Gomes
- Escola Municipal Santa Helena
- Escola Municipal Thermozina de Siqueira

### Estaduais
- Escola Estadual Cel Rafael de Siqueira
- Escola Estadual Professor Ana Tereza Albernaz
- Escola Estadual Reunidas de Cachoeira Rica
- Escola Estadual São José

## Privadas
- Colégio Tales de Mileto
- Centro Educacional Sebastião Albernaz

# 📋 PLANO DE EXECUÇÃO - SISTEMA DE FREQUÊNCIA DOJÔ UEMURA

## 🎯 **OBJETIVO PRINCIPAL**
Implementar um sistema completo de controle de frequência que permita aos responsáveis acompanhar em tempo real quando seus atletas entram e saem do Dojô, incluindo notificações automáticas e controle de acesso via QR Code.

## 🚀 **FASE 1: SISTEMA DE FREQUÊNCIA (PRIORIDADE MÁXIMA)**

### **1.1 Estrutura de Dados para Frequência**

#### **Modelo: Frequencia**
```python
class Frequencia(models.Model):
    atleta = models.ForeignKey(Dependente, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField()
    data_saida = models.DateTimeField(null=True, blank=True)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE)
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default='presente')
    observacoes = models.TextField(blank=True)
    qr_code_utilizado = models.CharField(max_length=10)
```

#### **Modelo: Turma**
```python
class Turma(models.Model):
    nome = models.CharField(max_length=100)
    modalidade = models.CharField(choices=MODALIDADE_CHOICES)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)
    alunos = models.ManyToManyField(Dependente, through='Matricula')
    capacidade_maxima = models.IntegerField()
    ativa = models.BooleanField(default=True)
```

#### **Modelo: Professor**
```python
class Professor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    graduacao = models.CharField(max_length=50)
    modalidades = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)
```

#### **Modelo: Matricula**
```python
class Matricula(models.Model):
    atleta = models.ForeignKey(Dependente, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_matricula = models.DateField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    tipo_matricula = models.CharField(choices=TIPO_MATRICULA_CHOICES)
```

### **1.2 Sistema de QR Code**

#### **Geração de QR Code**
- **Código Alfanumérico**: 10 dígitos únicos por atleta
- **QR Code**: Gerado automaticamente e atualizado na carteira do atleta
- **Validação**: Verificação de validade e permissões

#### **Leitor de QR Code na Portaria**
- **Interface Web**: Para funcionários da portaria
- **Validação Instantânea**: Verificação de matrícula ativa
- **Registro Automático**: Entrada/saída automática
- **Alertas**: Para alunos não autorizados

### **1.3 Controle de Entrada/Saída**

#### **Registro de Entrada**
- **Leitura QR Code**: Na portaria
- **Validação**: Verificar se aluno está matriculado na turma do dia
- **Horário**: Registro automático do timestamp
- **Notificação**: Envio imediato para responsável

#### **Registro de Saída**
- **Leitura QR Code**: Na saída
- **Horário**: Registro automático
- **Duração da Aula**: Cálculo automático
- **Notificação**: Confirmação para responsável

## 📱 **FASE 2: SISTEMA DE NOTIFICAÇÕES**

### **2.1 Notificações em Tempo Real**

#### **Para Responsáveis**
- **Entrada**: "Seu atleta [NOME] entrou no Dojô às [HORA]"
- **Saída**: "Seu atleta [NOME] saiu do Dojô às [HORA]"
- **Atraso**: "Seu atleta [NOME] não compareceu à aula de hoje"
- **Frequência**: Relatório semanal de presenças

#### **Para Professores**
- **Alunos Presentes**: Lista atualizada em tempo real
- **Alunos Ausentes**: Alertas para alunos não presentes
- **Estatísticas**: Contagem de presenças por aula

### **2.2 Canais de Notificação**
- **Email**: Notificações automáticas
- **SMS**: Para casos urgentes
- **Push Notifications**: Via aplicativo web
- **WhatsApp**: Integração futura

## 🖥️ **FASE 3: INTERFACES DE USUÁRIO**

### **3.1 Portal da Portaria**
- **Interface Simples**: Para funcionários
- **Leitura QR Code**: Scanner integrado
- **Validação Visual**: Status do aluno em tempo real
- **Registro Manual**: Para casos especiais

### **3.2 Portal do Responsável**
- **Dashboard**: Visão geral da frequência
- **Histórico**: Entradas e saídas detalhadas
- **Relatórios**: Frequência semanal/mensal
- **Alertas**: Notificações de eventos importantes

### **3.3 Portal do Professor**
- **Lista de Presença**: Alunos da turma
- **Controle de Aula**: Início/fim da sessão
- **Relatórios**: Estatísticas de frequência
- **Comunicação**: Envio de mensagens para responsáveis

## 🔧 **FASE 4: IMPLEMENTAÇÃO TÉCNICA**

### **4.1 Backend (Django)**
- **Novos Apps**: `frequencia`, `turmas`, `professores`
- **APIs REST**: Para comunicação em tempo real
- **WebSockets**: Para notificações instantâneas
- **Celery**: Para tarefas assíncronas (notificações)

### **4.2 Frontend**
- **Bootstrap 5**: Interface responsiva
- **JavaScript**: Validações e interações
- **QR Code Scanner**: Biblioteca para leitura
- **PWA**: Aplicativo web progressivo

### **4.3 Banco de Dados**
- **Migrations**: Estrutura de novas tabelas
- **Índices**: Para consultas de frequência
- **Backup**: Sistema de backup automático

## 📅 **CRONOGRAMA DE IMPLEMENTAÇÃO**

### **Semana 1-2: Estrutura Base**
- [ ] Criar modelos de dados (Frequencia, Turma, Professor, Matricula)
- [ ] Implementar migrações do banco
- [ ] Criar admin do Django para gestão

### **Semana 3-4: Sistema de QR Code**
- [ ] Implementar geração de QR Code
- [ ] Criar sistema de validação
- [ ] Desenvolver leitor na portaria

### **Semana 5-6: Controle de Frequência**
- [ ] Implementar registro de entrada/saída
- [ ] Criar validações de permissão
- [ ] Desenvolver sistema de horários

### **Semana 7-8: Notificações**
- [ ] Implementar sistema de notificações
- [ ] Criar templates de email
- [ ] Desenvolver notificações em tempo real

### **Semana 9-10: Interfaces**
- [ ] Portal da portaria
- [ ] Portal do responsável
- [ ] Portal do professor

### **Semana 11-12: Testes e Ajustes**
- [ ] Testes de integração
- [ ] Testes de usuário
- [ ] Ajustes finais
- [ ] Documentação

## 🛠️ **TECNOLOGIAS NECESSÁRIAS**

### **Backend**
- Django 5.2.4 (já existente)
- Django REST Framework (novo)
- Celery (novo)
- Redis (novo - para cache e filas)

### **Frontend**
- Bootstrap 5 (já existente)
- QR Code Scanner (novo)
- WebSockets (novo)
- PWA capabilities (novo)

### **Infraestrutura**
- SQLite (desenvolvimento - já existente)
- Redis (novo)
- Celery Worker (novo)

## 📊 **MÉTRICAS DE SUCESSO**

### **Funcionais**
- [ ] 100% dos alunos com QR Code funcional
- [ ] Notificações enviadas em menos de 30 segundos
- [ ] Sistema disponível 99.9% do tempo
- [ ] Interface responsiva em todos os dispositivos

### **Usuário**
- [ ] Redução de 80% nas dúvidas sobre frequência
- [ ] Aumento de 90% na satisfação dos responsáveis
- [ ] Tempo de registro de entrada/saída < 5 segundos

## 🚨 **RISCOS E MITIGAÇÕES**

### **Riscos Técnicos**
- **QR Code não lido**: Implementar registro manual como fallback
- **Sistema offline**: Cache local para operações críticas
- **Performance**: Otimização de consultas e índices

### **Riscos de Usuário**
- **Resistência à mudança**: Treinamento e documentação clara
- **Erro humano**: Validações automáticas e confirmações
- **Falta de internet**: Sistema funcionando offline

## 📝 **PRÓXIMOS PASSOS IMEDIATOS**

1. **Criar estrutura de novos apps Django**
2. **Implementar modelos de dados básicos**
3. **Desenvolver sistema de QR Code**
4. **Criar interface da portaria**
5. **Implementar registro de frequência**

---

**Status**: 📋 Planejado  
**Prioridade**: 🔴 Alta  
**Responsável**: Equipe de Desenvolvimento  
**Data de Início**: [DATA]  
**Data de Conclusão**: [DATA + 12 semanas]



# 📋 **TODO - Dojô Uemura**

## 🎯 **OBJETIVO DO PROJETO**
Sistema completo de gestão para Dojô Uemura, incluindo matrículas, frequência, financeiro e eventos.

---

## ✅ **TAREFAS CONCLUÍDAS**

### **🏗️ Estrutura Base**
- [ ] Configuração inicial do projeto Django
- [ ] App `usuarios` como central de autenticação
- [ ] Modelo `Usuario` customizado com `AbstractUser`
- [ ] Modelo `Atleta` para atletas
- [ ] Sistema de tipos de conta (RESPONSAVEL, PROFESSOR, GESTOR, FUNCIONARIO)

### **🔐 Sistema de Autenticação**
- [ ] Views de registro e login
- [ ] Verificação de email
- [ ] Templates de autenticação
- [ ] Sistema de mensagens

### **📊 Modelos de Dados**
- [ ] Modelos `Modalidade`, `TipoMatricula`, `StatusMatricula`
- [ ] Campos de matrícula no modelo `Atleta`
- [ ] Relacionamentos entre modelos
- [ ] Migrações do banco de dados

### **🎨 Interface e Navegação**
- [ ] Template home com fluxo claro de navegação
- [ ] Botões "Registre-se" e "Portal do Aluno" na home
- [ ] Seção Portal do Aluno com explicações claras
- [ ] Dashboard com informações do usuário

### **📝 Sistema de Matrículas**
- [ ] Views para projeto social e modalidade paga
- [ ] Template específico para projeto social
- [ ] Template específico para modalidade paga
- [ ] Validações específicas por tipo de matrícula
- [ ] Dashboard com opções de matrícula

---

## 🔄 **TAREFAS EM ANDAMENTO**

### **⚡ Views e Lógica de Negócio**
- [ ] ~~Implementar view `matricula_projeto_social`~~ ✅ **CONCLUÍDO**
- [ ] ~~Implementar view `matricula_modalidade_paga`~~ ✅ **CONCLUÍDO**
- [ ] ~~Atualizar view `cadastrar_atleta` para usar novos campos~~ ✅ **CONCLUÍDO**
- [ ] ~~Validações específicas por tipo de matrícula~~ ✅ **CONCLUÍDO**

---

## 📋 **PRÓXIMAS TAREFAS (PRIORIDADE ALTA)**

### **📱 Controle de Frequência**
- [ ] **Sistema de QR Code** - Check-in/check-out dos alunos
- [ ] **Notificações em tempo real** - Avisos para responsáveis
- [ ] **Relatórios de presença** - Estatísticas de frequência

### **🔧 Melhorias no Sistema de Matrículas**
- [ ] **Validações de CPF** - Implementar validação real de CPF
- [ ] **Upload de fotos** - Configurar media files para fotos dos atletas
- [ ] **Validações de CEP** - Integrar com API de CEP para autocompletar endereço
- [ ] **Termos legais** - Criar templates para termos de responsabilidade e uso de imagem


### **💰 Sistema de Pagamentos (PRIORIDADE MÉDIA)**
- [ ] **Integração com PIX** - Configurar gateway de pagamento
- [ ] **Sistema de Boletos** - Geração automática de boletos
- [ ] **Controle de mensalidades** - Sistema de cobrança recorrente
- [ ] **Relatórios financeiros** - Dashboard para gestores

### **📧 Notificações e Comunicação (PRIORIDADE MÉDIA)**
- [ ] **Email automático** - Confirmação de matrícula e status
- [ ] **SMS (futuro)** - Notificações importantes
- [ ] **WhatsApp Business** - Comunicação direta com responsáveis

## 📋 **TAREFAS FUTURAS (PRIORIDADE BAIXA)**

### **📊 Relatórios e Analytics**
- [ ] **Dashboard do Gestor** - Visão geral do Dojô
- [ ] **Relatórios financeiros** - Análise de receita e despesas
- [ ] **Estatísticas de alunos** - Crescimento e retenção

### **🎉 Sistema de Eventos**
- [ ] **Gestão de competições** - Inscrições e resultados
- [ ] **Graduações** - Controle de faixas e progressão
- [ ] **Eventos especiais** - Workshops e seminários

---

## 🚀 **PRÓXIMOS PASSOS RECOMENDADOS**

### **1. Validações e Melhorias (SEMANA ATUAL)**
- [ ] Implementar validação real de CPF
- [ ] Configurar upload de fotos
- [ ] Integrar validação de CEP
- [ ] Testar fluxo completo de matrículas

### **2. Sistema de Pagamentos (PRÓXIMA SEMANA)**
- [ ] Configurar gateway PIX
- [ ] Implementar sistema de boletos
- [ ] Criar controle de mensalidades
- [ ] Testar fluxo de pagamento

### **3. Notificações (TERCEIRA SEMANA)**
- [ ] Configurar emails automáticos
- [ ] Implementar sistema de mensagens
- [ ] Testar notificações

---

## 📅 **CRONOGRAMA ESTIMADO**

- **Semana 1**: Validações e melhorias ✅ **EM ANDAMENTO**
- **Semana 2**: Sistema de pagamentos
- **Semana 3**: Notificações e comunicação
- **Semana 4**: Controle de frequência
- **Semana 5**: Relatórios e analytics
- **Semana 6**: Sistema de eventos

---

## 🎯 **MÉTRICAS DE SUCESSO**

- [ ] **Usabilidade**: Fluxo de matrícula em menos de 5 minutos
- [ ] **Performance**: Página carrega em menos de 3 segundos
- [ ] **Segurança**: 100% das validações funcionando
- [ ] **Satisfação**: Teste com usuários reais

---

**Última atualização**: 17/08/2025 - Implementação das validações específicas por tipo de matrícula concluída ✅


# 📋 PLANO DE EXECUÇÃO - SISTEMA DE FREQUÊNCIA DOJÔ UEMURA

## 🎯 **OBJETIVO PRINCIPAL**
Implementar um sistema completo de controle de frequência que permita aos responsáveis acompanhar em tempo real quando seus dependentes entram e saem do Dojô, incluindo notificações automáticas e controle de acesso via QR Code.

## 🚀 **FASE 1: SISTEMA DE FREQUÊNCIA (PRIORIDADE MÁXIMA)**

### **1.1 Estrutura de Dados para Frequência**

#### **Modelo: Frequencia**
```python
class Frequencia(models.Model):
    dependente = models.ForeignKey(Dependente, on_delete=models.CASCADE)
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
    dependente = models.ForeignKey(Dependente, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_matricula = models.DateField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    tipo_matricula = models.CharField(choices=TIPO_MATRICULA_CHOICES)
```

### **1.2 Sistema de QR Code**

#### **Geração de QR Code**
- **Código Alfanumérico**: 10 dígitos únicos por dependente
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
- **Entrada**: "Seu dependente [NOME] entrou no Dojô às [HORA]"
- **Saída**: "Seu dependente [NOME] saiu do Dojô às [HORA]"
- **Atraso**: "Seu dependente [NOME] não compareceu à aula de hoje"
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

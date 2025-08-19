# 🚀 Scripts de Inicialização - Dojô Uemura

Esta pasta contém todos os scripts necessários para configurar e inicializar o sistema Dojô Uemura.

## 📋 Scripts Disponíveis

### **🏢 Configuração da Empresa**
- **`setup_empresa.py`** - Configuração inicial da empresa (primeira execução)
- **`atualizar_empresa.py`** - Atualiza dados de empresa existente
- **`testar_empresa.py`** - Testa e verifica configuração da empresa

### **🏋️ Configuração das Modalidades**
- **`setup_modalidades.py`** - Cria modalidades padrão do sistema

### **📜 Configuração dos Termos**
- **`setup_termos_condicoes.py`** - Configura termos e condições legais do sistema

### **🖼️ Configuração da Galeria**
- **`setup_galeria.py`** - Configura galeria de imagens do sistema

### **📧 Testes e Utilitários**
- **`teste_email.py`** - Testa configuração de email
- **`testar_recuperacao_senha.py`** - Testa funcionalidades de recuperação de senha
- **`setup_dados_iniciais.py`** - Configura dados iniciais do sistema

## 🎯 Ordem de Execução Recomendada

### **1ª Execução (Sistema Novo)**
```bash
# 1. Configurar empresa
python scripts_inicializacao/setup_empresa.py

# 2. Configurar modalidades
python scripts_inicializacao/setup_modalidades.py

# 3. Configurar termos e condições
python scripts_inicializacao/setup_termos_condicoes.py

# 4. Configurar galeria
python scripts_inicializacao/setup_galeria.py

# 4. Configurar dados iniciais
python scripts_inicializacao/setup_dados_iniciais.py

# 5. Verificar configuração
python scripts_inicializacao/testar_empresa.py

# 6. Testar email
python scripts_inicializacao/teste_email.py
```

### **Atualizações (Sistema Existente)**
```bash
# Atualizar dados da empresa
python scripts_inicializacao/atualizar_empresa.py

# Verificar configuração
python scripts_inicializacao/testar_empresa.py
```

## ⚠️ Importante

- **Execute apenas uma vez** os scripts de setup inicial
- **Use `atualizar_empresa.py`** para modificar dados existentes
- **Sempre teste** com `testar_empresa.py` após mudanças
- **Ative o ambiente virtual** antes de executar: `venv\Scripts\activate`

## 🔧 Pré-requisitos

- Ambiente virtual ativado (`venv\Scripts\activate`)
- Django configurado e funcionando
- Banco de dados criado e migrações aplicadas
- Arquivo `.env` configurado com dados da empresa

## 📝 Logs

Todos os scripts exibem informações detalhadas sobre:
- ✅ Operações realizadas com sucesso
- ⚠️ Avisos e informações
- ❌ Erros encontrados
- 📊 Resumo das operações

---

**Desenvolvido para Dojô Uemura** 🥋
*Sistema de Gestão de Atletas e Modalidades*

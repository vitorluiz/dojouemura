# TODO

- Backend/Accounts
  - Criar tipos de contas/roles: Atleta, Professor, Admin
  - Ajustar permissões e grupos para cada papel
  - Página de login: layout e mensagens
  - Middleware para forçar troca de senha quando `must_change_password=True`
  - Testes: rate-limit de OTP, reenviar OTP, redirects de login

- Domínio
  - Modalidades: CRUD e ativação/inativação
  - Horários: janelas por dia/semana
  - Turmas: vínculo com Modalidade, Professor(es), capacidade e horário
  - Frequência (presenças): registrar, consultar e exportar por turma/período

- Fluxos
  - Matrícula de Atletas em Turmas (capacidade e conflitos de horário)
  - Relatórios: presença por atleta/turma/período

- Infra/Config
  - Internacionalização (pt-BR) em mensagens e templates
  - Docker: Dockerfile + docker-compose para backend

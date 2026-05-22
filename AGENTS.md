# AGENTS.md

Instruções para Codex ou outros agentes trabalhando neste repositório.

## Objetivo do Projeto

Este é um MVP de Gerenciador de Assinaturas Pessoais. O foco é manter uma aplicação simples, local, fácil de evoluir e com boa experiência visual.

## Como Trabalhar Neste Projeto

- Leia primeiro `context.md`, `roadmap.md` e `docs/architecture.md`.
- Preserve a arquitetura atual: rotas finas, regras no serviço, acesso ao banco no repositório.
- Não remova funcionalidades já implementadas sem pedido explícito.
- Antes de alterar regras financeiras, confira `app/models/subscription.py` e `app/services/subscription_service.py`.
- Antes de alterar o banco, confira `app/database/connection.py`.
- Antes de finalizar qualquer alteração, rode os testes.

## Comandos Úteis

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall app tests
python run.py
```

## Cuidados de Código

- Use queries parametrizadas com `?` no SQLite.
- Mantenha CSRF em todas as rotas POST.
- Mantenha autenticação por sessão nas telas privadas.
- Mantenha a regra de senha forte: mínimo 6, maiúscula, minúscula e caractere especial.
- Alteração de senha deve exigir senha atual correta, confirmação e gerar novo hash.
- Valide e-mail no backend em cadastro e login; sugestões no frontend não substituem validação.
- Toda query de assinatura deve ser filtrada por `user_id`.
- CSRF deve rejeitar token ausente e sessão sem token esperado.
- Em produção, não permita `SECRET_KEY` local/padrão.
- Em produção, mantenha `SESSION_COOKIE_SECURE=True` e use HTTPS.
- Mantenha CSP e cabeçalhos de segurança em `app/__init__.py`.
- Não reative `debug=True` como padrão de execução.
- Mantenha validação backend para valores finitos, nome até 120, valor até R$ 1.000.000,00 e divisão até 1000.
- Mantenha `notificar_dias_antes` entre 0 e 31 e calcule notificações apenas para assinaturas ativas do usuário logado.
- Não coloque segredo real em código.
- Valide entradas no backend mesmo que o HTML já tenha `required`, `min` ou `max`.
- Preserve escape automático do Jinja; evite `|safe` sem necessidade.
- Evite refatorações grandes quando a tarefa for pequena.

## Design

- Bootstrap 5 continua sendo a base.
- O visual atual segue uma estética de painel administrativo, com sidebar fixa no desktop.
- Tokens globais e dark mode ficam em `app/templates/base.html`.
- A página de dashboard usa escopo `.reports-page` por compatibilidade de CSS.
- A tela de assinaturas usa escopo `.subscriptions-page`.
- O dark mode deve ficar preto/cinza, com bom contraste:
  - fundo: `#101010`
  - superfície: `#18181b`
  - ativo: `#2a2a2e`
  - texto principal: claro

## Arquivos Mais Importantes

- `app/routes/subscription_routes.py`: rotas Flask e CSRF.
- `app/routes/auth_routes.py`: cadastro, login, logout e carregamento do usuário da sessão.
- A rota `/perfil` fica em `auth_routes.py` e deve continuar protegida por login e CSRF no POST.
- `app/services/subscription_service.py`: validação, dashboard, relatórios internos e regras de negócio.
- Notificações internas também ficam no serviço, não nos templates.
- `app/services/auth_service.py`: validação de credenciais e hash de senha.
- `AuthService.change_password`: regra de troca de senha.
- `app/repositories/subscription_repository.py`: queries SQLite.
- `app/repositories/user_repository.py`: persistência de usuários.
- `app/models/subscription.py`: entidade e propriedades calculadas.
- `app/templates/base.html`: layout global, sidebar, tema claro/escuro e CSS.
- `app/templates/index.html`: tela de assinaturas.
- `app/templates/reports.html`: tela de dashboard.
- `app/templates/form.html`: formulário de cadastro/edição.
- `app/templates/auth/profile.html`: Minha Conta e alteração de senha.
- `tests/test_app.py`: testes de fluxo principal.
- `.codex/skills/`: cópia versionada das skills customizadas usadas neste projeto.
- `scripts/install-codex-skills.ps1`: instala as skills do projeto no Codex global do notebook atual.

## Checklist Antes de Finalizar

- Testes passam.
- Rotas principais renderizam.
- POST sem CSRF retorna erro.
- Cadastro/login/logout sem CSRF retornam erro.
- Alteração de senha sem CSRF retorna erro e com senha atual incorreta não altera credenciais.
- Headers de segurança, CSP e cookie seguro em produção continuam cobertos por testes.
- Valores mensais/anuais continuam corretos.
- Valores `NaN`/`Infinity` não passam na validação.
- Notificações de vencimento respeitam `notificar_dias_antes`.
- Dark mode continua legível.
- Não há texto quebrado ou acentuação errada em templates.

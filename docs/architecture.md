# Arquitetura

## Visão Geral

A aplicação usa Flask com uma arquitetura simples em camadas:

```text
app/
    |-- __init__.py
    |-- security.py
|-- database/
|   `-- connection.py
|-- models/
|   |-- subscription.py
|   `-- user.py
|-- repositories/
|   |-- subscription_repository.py
|   `-- user_repository.py
|-- routes/
|   |-- auth_routes.py
|   `-- subscription_routes.py
|-- services/
|   |-- auth_service.py
|   `-- subscription_service.py
`-- templates/
    |-- base.html
    |-- form.html
    |-- index.html
    |-- auth/
    |   `-- profile.html
    `-- reports.html
tests/
`-- test_app.py
```

## Fluxo de Requisição

1. O usuário acessa uma rota em `subscription_routes.py`.
2. A rota chama `SubscriptionService`.
3. O serviço usa `SubscriptionRepository` para buscar ou salvar dados.
4. O repositório acessa SQLite usando `get_db()`.
5. O serviço monta dados de tela e cálculos.
6. A rota renderiza um template Jinja.

## Camadas

### Rotas

Arquivo: `app/routes/subscription_routes.py`

Responsabilidades:

- Registrar rotas Flask.
- Renderizar templates.
- Validar CSRF em POST.
- Redirecionar após operações.
- Mostrar mensagens com `flash`.
- Proteger rotas privadas com sessão.

Rotas GET privadas:

- `/`
- `/dashboard`
- `/relatorios` redireciona para `/dashboard`
- `/nova`
- `/editar/<id>`
- `/perfil`

Rotas POST protegidas por CSRF:

- `/nova`
- `/editar/<id>`
- `/excluir/<id>`
- `/duplicar/<id>`
- `/reativar/<id>`
- `/perfil`
- `/logout`

### Serviço

Arquivo: `app/services/subscription_service.py`

Responsabilidades:

- Validar dados do formulário.
- Centralizar regras de negócio.
- Montar dashboard.
- Montar dados do dashboard financeiro.
- Calcular vencimentos próximos.
- Validar cadastro/login e gerar/verificar hash de senha.

Funções importantes:

- `parse_subscription_form`
- `is_due_soon`
- `SubscriptionService.dashboard`
- `SubscriptionService.reports`
- `AuthService.register`
- `AuthService.authenticate`
- `AuthService.change_password`

### Repositório

Arquivo: `app/repositories/subscription_repository.py`

Responsabilidades:

- Ler e escrever no SQLite.
- Converter linhas do banco em `Subscription`.
- Manter queries parametrizadas.
- Filtrar assinaturas por `user_id`.
- Persistir e buscar usuários.

Métodos:

- `list_active`
- `list_inactive`
- `get_by_id`
- `create`
- `update`
- `deactivate`
- `activate`
- `UserRepository.get_by_id`
- `UserRepository.get_by_email`
- `UserRepository.create`
- `UserRepository.update_password`

### Modelo

Arquivo: `app/models/subscription.py`

Responsabilidades:

- Representar assinatura como dataclass.
- Expor propriedades calculadas.

Propriedades:

- `valor_mensal`
- `custo_real_mensal`
- `valor_anual`
- `custo_real_anual`

## Banco de Dados

Arquivo: `app/database/connection.py`

Tabela criada automaticamente:

```sql
CREATE TABLE IF NOT EXISTS assinatura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor REAL NOT NULL CHECK (valor >= 0),
    frequencia TEXT NOT NULL CHECK (frequencia IN ('mensal', 'anual')),
    vencimento INTEGER NOT NULL CHECK (vencimento BETWEEN 1 AND 31),
    categoria TEXT NOT NULL CHECK (categoria IN ('streaming', 'saúde', 'educação', 'outros')),
    divisao INTEGER NOT NULL DEFAULT 1 CHECK (divisao >= 1),
        ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
        notificar_dias_antes INTEGER NOT NULL DEFAULT 7 CHECK (notificar_dias_antes BETWEEN 0 AND 31),
        user_id INTEGER
)
```

```sql
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
```

## Templates

### `base.html`

Contém:

- HTML base.
- Sidebar.
- Topbar.
- Ícone interno de notificações no topo para assinaturas dentro do prazo configurado.
- Menu de conta no topo com iniciais, Minha Conta e Sair.
- Flash messages.
- Bootstrap CDN.
- CSS global.
- Tema claro/escuro.
- Script de dark mode.

### `index.html`

Tela principal com:

- Filtros.
- Resumo de quantidade e total real mensal.
- Assinaturas ativas.
- Assinaturas inativas.
- Dropdown de ações por linha.
- Script de filtro sem recarregar.

### `reports.html`

Tela de dashboard com:

- Cards financeiros.
- Vencimentos próximos.
- Distribuição por categoria.
- Frequência.
- Status da carteira.
- Maiores custos reais.

### `form.html`

Formulário compartilhado para:

- Nova assinatura.
- Editar assinatura.

### `auth/profile.html`

Tela privada de Minha Conta com:

- Nome e e-mail do usuário autenticado.
- Formulário de alteração de senha.
- Validação por senha atual, senha forte e confirmação da nova senha.

## Segurança

Medidas atuais:

- Queries SQLite parametrizadas.
- CSRF manual com token em sessão.
- CSRF rejeita token ausente e sessão sem token esperado.
- Validação backend de campos.
- Constraints no SQLite.
- Escape automático do Jinja.
- Senhas armazenadas apenas como hash do Werkzeug.
- Cadastro exige senha com mínimo de 6 caracteres, letra maiúscula, letra minúscula e caractere especial.
- Alteração de senha exige senha atual correta, nova senha forte, confirmação e salva apenas novo hash.
- Cadastro e login validam formato de e-mail no serviço de autenticação.
- A sugestão de domínio no cadastro é apenas UX; a validação real continua no backend.
- Rotas de assinatura filtram por `user_id`; IDs de outro usuário retornam `404`.
- Sessão usa `HttpOnly`, `SameSite=Lax` e duração permanente de 8 horas.
- Em produção, sessão força `Secure=True`.
- Produção exige chave real via `FLASK_SECRET_KEY`.
- Respostas incluem CSP básica e cabeçalhos contra sniffing, clickjacking e vazamento de permissões.
- Formulário de assinatura rejeita valores não finitos, nome acima de 120, valor acima de R$ 1.000.000,00 e divisão acima de 1000.
- Notificações internas são calculadas no serviço a partir de `vencimento` e `notificar_dias_antes`.
- O ícone de notificações no `base.html` mostra apenas assinaturas ativas do usuário logado.
- O menu Minha Conta é exibido apenas para usuário autenticado.

Ponto de atenção:

- `SECRET_KEY` tem fallback local apenas em desenvolvimento. Em produção, configurar `FLASK_APP_ENV=production` e `FLASK_SECRET_KEY`.
- `SESSION_COOKIE_SECURE` deve ser `true` quando a aplicação estiver em HTTPS.

## Testes

Arquivo: `tests/test_app.py`

Cobre:

- Criação.
- Edição.
- Cálculo mensal/anual.
- Inativação.
- Reativação.
- Duplicação.
- Exemplos mensais e anuais com divisão.
- Página de dashboard.
- Presença do dark mode.
- CSRF em rotas de autenticação e assinatura.
- Cabeçalhos básicos de segurança.
- CSP e cookie seguro em produção.
- Falha segura quando produção usa chave local.
- Campo de notificação por assinatura.
- Página de perfil e menu Minha Conta.
- Validação e persistência da alteração de senha.

Comando:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

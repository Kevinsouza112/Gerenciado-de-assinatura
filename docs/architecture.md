# Arquitetura

## Visão Geral

A aplicação usa Flask com uma arquitetura simples em camadas:

```text
app/
|-- __init__.py
|-- database/
|   `-- connection.py
|-- models/
|   `-- subscription.py
|-- repositories/
|   `-- subscription_repository.py
|-- routes/
|   `-- subscription_routes.py
|-- services/
|   `-- subscription_service.py
`-- templates/
    |-- base.html
    |-- form.html
    |-- index.html
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

Rotas POST protegidas por CSRF:

- `/nova`
- `/editar/<id>`
- `/excluir/<id>`
- `/duplicar/<id>`
- `/reativar/<id>`

### Serviço

Arquivo: `app/services/subscription_service.py`

Responsabilidades:

- Validar dados do formulário.
- Centralizar regras de negócio.
- Montar dashboard.
- Montar relatórios.
- Calcular vencimentos próximos.

Funções importantes:

- `parse_subscription_form`
- `is_due_soon`
- `SubscriptionService.dashboard`
- `SubscriptionService.reports`

### Repositório

Arquivo: `app/repositories/subscription_repository.py`

Responsabilidades:

- Ler e escrever no SQLite.
- Converter linhas do banco em `Subscription`.
- Manter queries parametrizadas.

Métodos:

- `list_active`
- `list_inactive`
- `get_by_id`
- `create`
- `update`
- `deactivate`
- `activate`

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
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
)
```

## Templates

### `base.html`

Contém:

- HTML base.
- Sidebar.
- Topbar.
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

Tela de relatórios com:

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

## Segurança

Medidas atuais:

- Queries SQLite parametrizadas.
- CSRF manual com token em sessão.
- Validação backend de campos.
- Constraints no SQLite.
- Escape automático do Jinja.

Ponto de atenção:

- `SECRET_KEY` tem fallback local. Em produção, configurar via variável de ambiente.

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
- Página de relatórios.
- Presença do dark mode.

Comando:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

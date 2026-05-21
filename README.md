# Gerenciador de Assinaturas Pessoais

MVP web em Flask para controlar assinaturas pessoais, custos divididos e recorrências mensais/anuais.

## Funcionalidades

- Cadastro, edição e duplicação de assinaturas.
- Inativação e reativação sem apagar o histórico.
- Listagem principal com assinaturas ativas e seção separada para inativas.
- Filtros por categoria e frequência na tela de assinaturas.
- Cálculo de total bruto mensal, total real mensal, total bruto anual e total real anual.
- Destaque visual para vencimentos próximos.
- Dashboard com cartões financeiros, distribuição por categoria, frequência, status e maiores custos reais.
- Tema claro/escuro com preferência salva no navegador.
- Cadastro, login e logout com sessão.
- Isolamento por usuário: cada conta vê apenas as próprias assinaturas.
- Senha com regra mínima: 6 caracteres, uma letra maiúscula, uma minúscula e um caractere especial.
- Validação de formato de e-mail no cadastro e no login.
- Sugestão visual de domínio de e-mail no cadastro após digitar `@`.
- Confirmação de senha no cadastro.

## Stack

- Python 3 + Flask.
- SQLite local.
- Bootstrap 5 via CDN.
- Bootstrap Icons via CDN.
- CSS próprio em `app/templates/base.html`.
- Testes com `unittest` e Flask test client.

## Como Executar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Acesse:

```text
http://127.0.0.1:5000
```

O banco SQLite é criado automaticamente em:

```text
instance/assinaturas.sqlite3
```

## Configuração

Para uso local, a aplicação sobe com configurações de desenvolvimento. Para ambiente publicado, configure pelo menos:

```powershell
$env:FLASK_APP_ENV = "production"
$env:FLASK_SECRET_KEY = "troque-por-uma-chave-longa-e-aleatoria"
$env:FLASK_SESSION_COOKIE_SECURE = "true"
```

Se `FLASK_APP_ENV=production` for usado sem `FLASK_SECRET_KEY`, a aplicação não inicia. Isso evita publicar com a chave local `dev-change-me`.

Há um modelo em `.env.example` para orientar outro desktop ou deploy.

## Rodar Testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Se a virtualenv ainda não existir nesse desktop, use:

```powershell
python -m unittest discover -s tests -v
```

Checagem rápida de sintaxe:

```powershell
.\.venv\Scripts\python.exe -m compileall app tests
```

## Rotas Principais

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Tela de assinaturas com resumo, filtros, ativas e inativas |
| `/dashboard` | GET | Dashboard financeiro |
| `/relatorios` | GET | Redireciona para `/dashboard` |
| `/cadastro` | GET/POST | Cadastro de usuário |
| `/login` | GET/POST | Login de usuário |
| `/logout` | POST | Encerra a sessão |
| `/nova` | GET/POST | Cadastro de assinatura |
| `/editar/<id>` | GET/POST | Edição de assinatura |
| `/excluir/<id>` | POST | Marca assinatura como inativa |
| `/reativar/<id>` | POST | Reativa assinatura inativa |
| `/duplicar/<id>` | POST | Duplica uma assinatura |

## Modelo de Dados

Tabela `assinatura`:

- `id`: inteiro, chave primária.
- `nome`: texto.
- `valor`: decimal armazenado como `REAL`.
- `frequencia`: `mensal` ou `anual`.
- `vencimento`: dia do mês entre 1 e 31.
- `categoria`: `streaming`, `saúde`, `educação` ou `outros`.
- `divisao`: quantidade de pessoas na divisão, mínimo 1.
- `ativo`: `1` ativa, `0` inativa.
- `user_id`: dono da assinatura.

Tabela `usuario`:

- `id`: inteiro, chave primária.
- `nome`: texto.
- `email`: texto único.
- `password_hash`: hash da senha gerado pelo Werkzeug.

Regras de senha:

- Pelo menos 6 caracteres.
- Pelo menos uma letra maiúscula.
- Pelo menos uma letra minúscula.
- Pelo menos um caractere especial.

## Regras de Cálculo

- Assinatura mensal: `valor_mensal = valor`.
- Assinatura anual: `valor_mensal = valor / 12`.
- Custo real mensal: `valor_mensal / divisao`.
- Total bruto anual: `total_bruto_mensal * 12`.
- Total real anual: `total_real_mensal * 12`.
- Todos os totais consideram apenas assinaturas ativas do usuário logado.

## Documentação

- [Contexto do projeto](context.md)
- [Roadmap](roadmap.md)
- [Arquitetura](docs/architecture.md)
- [Auditoria e evidências](docs/audit.md)
- [Instruções para agentes](AGENTS.md)

## Skills do Codex

As skills customizadas usadas no projeto ficam versionadas em:

```text
.codex/skills/
```

Para instalar essas skills como globais em outro notebook, depois do `git pull`, rode:

```powershell
.\scripts\install-codex-skills.ps1
```

Para sobrescrever skills globais que já existam:

```powershell
.\scripts\install-codex-skills.ps1 -Force
```

Depois reinicie o Codex/VS Code para a lista de skills ser recarregada.

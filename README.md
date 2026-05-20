# Gerenciador de Assinaturas Pessoais

MVP web em Flask para controlar assinaturas pessoais, custos divididos e recorrências mensais/anuais.

## Funcionalidades

- Cadastro, edição e duplicação de assinaturas.
- Inativação e reativação sem apagar o histórico.
- Listagem principal com assinaturas ativas e seção separada para inativas.
- Filtros por categoria e frequência na tela de assinaturas.
- Cálculo de total bruto mensal, total real mensal, total bruto anual e total real anual.
- Destaque visual para vencimentos próximos.
- Página de relatórios com cartões financeiros, distribuição por categoria, frequência, status e maiores custos reais.
- Tema claro/escuro com preferência salva no navegador.

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

## Rodar Testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Checagem rápida de sintaxe:

```powershell
.\.venv\Scripts\python.exe -m compileall app tests
```

## Rotas Principais

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Tela de assinaturas com resumo, filtros, ativas e inativas |
| `/relatorios` | GET | Página de relatórios financeiros |
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

## Regras de Cálculo

- Assinatura mensal: `valor_mensal = valor`.
- Assinatura anual: `valor_mensal = valor / 12`.
- Custo real mensal: `valor_mensal / divisao`.
- Total bruto anual: `total_bruto_mensal * 12`.
- Total real anual: `total_real_mensal * 12`.

## Documentação

- [Contexto do projeto](context.md)
- [Roadmap](roadmap.md)
- [Arquitetura](docs/architecture.md)
- [Instruções para agentes](AGENTS.md)

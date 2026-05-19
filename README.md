# Gerenciador de Assinaturas Pessoais

MVP web em Flask para cadastrar, editar, excluir e acompanhar assinaturas pessoais com resumo mensal/anual.

## Stack escolhida

- Python 3 + Flask: simples, produtivo e adequado para CRUD pequeno/medio.
- SQLite: banco leve, local e sem servidor.
- Bootstrap 5 via CDN: interface responsiva com baixa complexidade.
- Camadas separadas: rotas, repositorio, servicos, modelos e templates.

## Como executar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Acesse `http://127.0.0.1:5000`.

O banco SQLite sera criado automaticamente em `instance/assinaturas.sqlite3`.

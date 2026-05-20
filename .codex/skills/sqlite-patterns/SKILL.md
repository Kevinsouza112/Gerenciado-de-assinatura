---
name: sqlite-patterns
description: Boas práticas e padrões para projetos web pequenos usando SQLite como banco de dados. Use esta skill sempre que o projeto usar SQLite — especialmente ao criar modelos, migrations, queries, relacionamentos entre tabelas, ou ao adicionar login/autenticação. Deve ser consultada antes de criar ou alterar a estrutura do banco de dados.
---

# SQLite Patterns — Boas Práticas para Projetos Pequenos

## Quando usar SQLite
- Projetos de uso pessoal ou pequenos grupos (até ~100 usuários simultâneos)
- MVP e protótipos
- Aplicações que rodam em um único servidor
- Quando não há necessidade de banco remoto

---

## Configuração base (Flask + SQLAlchemy)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

---

## Padrão de modelo

```python
from datetime import datetime

class Assinatura(db.Model):
    __tablename__ = 'assinaturas'

    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(100), nullable=False)
    valor      = db.Column(db.Float, nullable=False)
    frequencia = db.Column(db.String(10), nullable=False, default='mensal')
    vencimento = db.Column(db.Integer, nullable=False)
    categoria  = db.Column(db.String(50), nullable=False, default='outros')
    divisao    = db.Column(db.Integer, nullable=False, default=1)
    ativo      = db.Column(db.Boolean, nullable=False, default=True)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Assinatura {self.nome}>'
```

---

## Inicialização do banco

```python
# Sempre usar dentro do app context
with app.app_context():
    db.create_all()
```

Chamar isso no `app.py` na inicialização, antes de rodar o servidor.

---

## Queries comuns

### Listar apenas ativos
```python
assinaturas = Assinatura.query.filter_by(ativo=True).all()
```

### Listar inativos
```python
inativas = Assinatura.query.filter_by(ativo=False).all()
```

### Buscar por id (com 404 automático)
```python
assinatura = Assinatura.query.get_or_404(id)
```

### Filtrar por categoria
```python
assinaturas = Assinatura.query.filter_by(categoria='streaming', ativo=True).all()
```

### Ordenar por nome
```python
assinaturas = Assinatura.query.filter_by(ativo=True).order_by(Assinatura.nome).all()
```

---

## CRUD padrão

### Criar
```python
nova = Assinatura(nome='Netflix', valor=55.90, frequencia='mensal',
                  vencimento=15, categoria='streaming', divisao=1)
db.session.add(nova)
db.session.commit()
```

### Atualizar
```python
assinatura = Assinatura.query.get_or_404(id)
assinatura.valor = 59.90
db.session.commit()
```

### Deletar (evitar — preferir inativar)
```python
# Preferido: inativar
assinatura.ativo = False
db.session.commit()

# Só deletar se realmente necessário
db.session.delete(assinatura)
db.session.commit()
```

---

## Adicionando login (Flask-Login + User model)

### Modelo de usuário
```python
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    senha    = db.Column(db.String(256), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)
```

### Relacionamento User → Assinaturas
Adicionar ao modelo `Assinatura`:
```python
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```

Adicionar ao modelo `User`:
```python
assinaturas = db.relationship('Assinatura', backref='user', lazy=True)
```

### Query filtrada por usuário logado
```python
from flask_login import current_user

assinaturas = Assinatura.query.filter_by(user_id=current_user.id, ativo=True).all()
```

---

## Boas práticas gerais

- Sempre commitar após alterações: `db.session.commit()`
- Sempre usar `get_or_404()` em rotas que recebem `id` pela URL
- Nunca expor o arquivo `.db` publicamente — adicionar ao `.gitignore`
- Fazer backup do `.db` antes de alterações estruturais grandes
- Não usar `Float` para valores financeiros críticos em produção — preferir `Numeric(10, 2)` do SQLAlchemy

```python
# Mais seguro para valores monetários
valor = db.Column(db.Numeric(10, 2), nullable=False)
```

---

## .gitignore recomendado
```
*.db
*.sqlite
__pycache__/
.env
venv/
```

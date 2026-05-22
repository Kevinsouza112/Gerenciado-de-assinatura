# Auditoria e Evidências

Última auditoria local: 2026-05-22.

## Escopo Revisado

- Rotas Flask públicas e privadas.
- Cadastro, login, logout e sessão.
- CSRF em rotas POST.
- Isolamento de assinaturas por usuário.
- Queries SQLite.
- Templates Jinja e JavaScript inline.
- Configuração local/produção.
- Cabeçalhos de segurança e política CSP.
- Notificação interna de vencimento.
- Menu de conta e página Minha Conta.
- Alteração de senha autenticada.
- Documentação de handoff para outro desktop.

## Achados Corrigidos

### CSRF aceitava POST sem token em sessão nova

Impacto: rotas POST como `/login`, `/cadastro` e `/logout` podiam aceitar requisição sem `csrf_token` quando a sessão ainda não tinha token.

Correção: `app/security.py` agora exige que o token enviado e o token esperado existam antes de usar `compare_digest`.

Evidência: teste `test_auth_post_routes_require_existing_csrf_token`.

### `run.py` usava debug ligado

Impacto: `debug=True` não deve ser o padrão de execução, porque em ambiente exposto o debugger é perigoso.

Correção: `run.py` agora usa `app.config.get("DEBUG", False)`.

Evidência: varredura não encontra mais `debug=True` em código executável.

### Produção podia iniciar com chave local

Impacto: sessões Flask dependem de `SECRET_KEY`; usar chave previsível em produção compromete assinatura de sessão.

Correção: `create_app` falha se `APP_ENV=production` e `SECRET_KEY` continuar como `dev-change-me`.

Evidência: teste `test_production_requires_real_secret_key`.

### Respostas não tinham cabeçalhos básicos de segurança

Impacto: faltava defesa em profundidade contra sniffing, clickjacking e exposição excessiva de referrer/permissões.

Correção: `after_request` adiciona `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` e `Permissions-Policy`.

Evidência: teste `test_security_headers_are_set`.

### Produção podia manter cookie de sessão sem `Secure`

Impacto: se a aplicação fosse publicada com HTTPS, mas sem configurar `FLASK_SESSION_COOKIE_SECURE`, o cookie de sessão poderia trafegar sem a flag `Secure`.

Correção: quando `APP_ENV=production`, `create_app` força `SESSION_COOKIE_SECURE=True`.

Evidência: teste `test_production_forces_secure_session_cookie`.

### Validação financeira aceitava números não finitos

Impacto: valores como `NaN` e `Infinity` poderiam atravessar a conversão numérica.

Correção: `parse_subscription_form` exige `Decimal.is_finite()`, limita nome a 120 caracteres, valor a R$ 1.000.000,00 e divisão a 1000.

Evidência: teste `test_subscription_form_rejects_oversized_and_non_finite_values`.

### Perfil precisava de troca de senha segura

Impacto: o usuário ainda não tinha uma área própria para revisar dados da conta ou alterar a senha dentro da sessão.

Correção: criada a rota privada `/perfil`, menu de conta no topo, formulário com CSRF, validação de senha atual, regra de senha forte, confirmação da nova senha e persistência apenas do novo hash.

Evidência: testes `test_profile_page_shows_account_data_and_menu`, `test_profile_password_change_validates_current_and_new_password` e `test_profile_password_change_updates_login_password`.

## Evidência de Testes

Comandos executados:

```powershell
python -m unittest discover -s tests -v
python -m compileall app tests
```

Resultado conhecido:

```text
Ran 26 tests
OK
```

Também foi verificado com Flask test client adversarial:

```text
anonymous /, /dashboard, /relatorios, /nova, /editar/1, /perfil -> 302 /login
payload XSS em nome de assinatura -> escapado no HTML
POST sem CSRF em /nova, /editar/1, /excluir/1, /duplicar/1, /reativar/1, /perfil, /logout -> 400
GET/POST com id de outro usuário -> 404
login com payload SQLi-style -> rejeitado com mensagem genérica
```

Também foi verificado por HTTP local:

```powershell
curl.exe -s -o NUL -w "%{http_code} %{redirect_url}" http://127.0.0.1:5000/login
curl.exe -s -o NUL -w "%{http_code} %{redirect_url}" http://127.0.0.1:5000/dashboard
curl.exe -s -o NUL -w "%{http_code} %{redirect_url}" http://127.0.0.1:5000/relatorios
```

Resultado esperado quando anônimo:

```text
/login 200
/dashboard 302 -> /login
/relatorios 302 -> /login
```

## Deploy Check

- `debug=True` não aparece em código executável.
- `instance/`, `.env`, `*.log`, `.venv/` e `__pycache__/` estão ignorados pelo Git.
- Nenhum banco SQLite, log local ou cache Python está versionado.
- Para produção, definir `FLASK_APP_ENV=production` e `FLASK_SECRET_KEY` real.
- Em produção, a aplicação força cookie de sessão com `Secure`; use HTTPS.

## Observações Para Continuidade

- O banco local fica em `instance/assinaturas.sqlite3` e não deve ser versionado.
- Logs como `server.full.log` são ignorados pelo Git.
- Depois de `git pull` em outro desktop, rode os comandos do README.
- Para instalar skills customizadas globais, rode `.\scripts\install-codex-skills.ps1`.

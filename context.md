# Contexto do Projeto

## Resumo

Projeto web de Gerenciador de Assinaturas Pessoais criado como MVP. A aplicação ajuda uma pessoa a acompanhar assinaturas, valores mensais/anuais, divisões de custo e vencimentos.

## Estado Atual

O projeto já possui:

- Backend Flask funcional.
- Banco SQLite criado automaticamente.
- CRUD de assinaturas.
- Inativação e reativação sem exclusão física.
- Duplicação de assinaturas.
- Tela principal com filtros por categoria e frequência.
- Seção de assinaturas ativas e seção separada de inativas.
- Dashboard financeiro.
- Dark mode com paleta preto/cinza.
- Cadastro e login com sessão.
- Isolamento de assinaturas por usuário.
- Senhas exigem maiúscula, minúscula e caractere especial.
- Cadastro e login validam formato de e-mail no backend.
- Cadastro tem sugestão de domínio de e-mail e confirmação de senha.
- Menu de conta no topo com acesso a Minha Conta e Sair.
- Página de perfil com dados do usuário e alteração de senha validada pela senha atual.
- Dashboard é a tela inicial após login.
- `/relatorios` existe apenas como redirecionamento legado para `/dashboard`.
- Ícone interno de notificações no topo para assinaturas dentro do prazo configurado.
- Formulário de assinatura permite configurar `notificar_dias_antes` de 0 a 31.
- CSRF rejeita POST sem token enviado e sem token esperado na sessão.
- Produção exige `FLASK_SECRET_KEY` quando `FLASK_APP_ENV=production`.
- Produção força cookie de sessão com `Secure`.
- Respostas incluem cabeçalhos básicos de segurança.
- Respostas incluem CSP básica para reduzir superfície de XSS e recursos externos.
- Testes automatizados cobrindo fluxo principal e exemplos.

## Decisões Tomadas

- Flask foi escolhido por simplicidade e velocidade para MVP.
- SQLite foi escolhido por ser leve e local.
- Bootstrap 5 foi mantido para interface responsiva.
- O banco usa uma única tabela `assinatura`.
- O login usa a tabela `usuario` e `assinatura.user_id`.
- A exclusão virou inativação lógica.
- Regras financeiras ficam no modelo e no serviço, não nos templates.

## Regras de Negócio

- Frequências permitidas: `mensal`, `anual`.
- Categorias permitidas: `streaming`, `saúde`, `educação`, `outros`.
- `divisao` deve ser no mínimo 1.
- `vencimento` deve estar entre 1 e 31.
- Assinaturas anuais são convertidas para mensal com `valor / 12`.
- Custo real mensal é `valor_mensal / divisao`.
- Totais do painel consideram apenas assinaturas ativas.
- Inativas ficam visíveis, mas não entram nos totais.
- Usuários só podem listar, editar, inativar, duplicar e reativar assinaturas próprias.
- Senhas são salvas apenas como hash e devem ter pelo menos 6 caracteres, uma maiúscula, uma minúscula e um caractere especial.
- Alteração de senha exige senha atual correta, confirmação da nova senha e reaproveita a regra de senha forte.
- Valores de assinatura precisam ser finitos, não negativos e até R$ 1.000.000,00.
- O nome da assinatura tem limite backend de 120 caracteres.
- A divisão tem limite backend de 1000 pessoas.
- Notificações usam apenas assinaturas ativas do usuário logado.
- Se `notificar_dias_antes` for 0, a assinatura notifica apenas no dia do vencimento.

## Design Atual

O visual foi inspirado em dashboards administrativos:

- Sidebar lateral.
- Cards financeiros.
- Tabelas limpas.
- Ações em dropdown por assinatura.
- Tema claro com branco/cinza/azul.
- Tema escuro com preto/cinza e texto claro.

Tokens específicos:

- Dashboard:
  - títulos: `#000C63`
  - valores: `#000C2C`
- Assinaturas:
  - títulos: `#000C39`
  - textos auxiliares: `#516272`
  - contadores: `#34D399`
- Dark mode:
  - fundo: `#101010`
  - superfícies: `#18181b`
  - ativos: `#2a2a2e`

## Últimas Validações Conhecidas

Comandos rodados com sucesso:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall app tests
```

Também foram validados:

- `/` retorna 200.
- `/dashboard` retorna 200.
- `/relatorios` redireciona para `/dashboard`.
- `/nova` retorna 200.
- `/cadastro` retorna 200.
- `/login` retorna 200.
- `/perfil` retorna 200 quando autenticado e redireciona anônimo para `/login`.
- `/editar/999` retorna 404.
- POST sem CSRF retorna 400.
- POST sem CSRF em cadastro, login e logout retorna 400.
- Usuário anônimo é redirecionado para `/login`.
- IDs de outro usuário retornam 404.
- Formulário inválido mostra mensagens de erro.
- Cabeçalhos `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy` e `Permissions-Policy` são enviados.
- Cabeçalho `Content-Security-Policy` é enviado.
- `APP_ENV=production` com chave local falha na inicialização.
- `APP_ENV=production` força `SESSION_COOKIE_SECURE=True`.
- Troca de senha valida senha atual, senha forte, confirmação e permite login apenas com a nova senha.
- Teste adversarial confirmou XSS escapado, POST sem CSRF rejeitado, IDs de outro usuário com 404 e login com payload SQLi-style rejeitado.

## Observações Para o Próximo Desktop

- Se `python` não funcionar no PATH, use diretamente `.\.venv\Scripts\python.exe`.
- Se a virtualenv não existir, recrie com os comandos do README.
- O banco local fica em `instance/assinaturas.sqlite3`; ele pode não estar versionado.
- O fallback `SECRET_KEY="dev-change-me"` é aceitável em local, mas deve ser substituído por variável de ambiente se for publicar.
- As skills customizadas foram copiadas para `.codex/skills/`.
- Para instalar as skills como globais no outro notebook, rode `.\scripts\install-codex-skills.ps1` ou `.\scripts\install-codex-skills.ps1 -Force`.

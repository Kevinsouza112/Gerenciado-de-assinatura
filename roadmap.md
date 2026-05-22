# Roadmap

## Pronto

- Estrutura Flask com SQLite.
- Cadastro, edição e listagem.
- Inativação e reativação.
- Duplicação de assinaturas.
- Filtros na tela principal.
- Painel de totais.
- Dashboard financeiro.
- Melhorias visuais inspiradas em dashboard.
- Tema escuro.
- Cadastro/login com sessão.
- Isolamento de assinaturas por usuário.
- Auditoria de segurança com correções de CSRF, debug, chave de produção, cabeçalhos e validação financeira.
- CSP básica e cookie de sessão `Secure` forçado em produção.
- `.env.example` para orientar configuração fora do desenvolvimento local.
- Notificação interna por assinatura com configuração de dias antes do vencimento.
- Página Minha Conta com dados do usuário e alteração de senha.
- Menu de conta no topo com Minha Conta e Sair.
- Testes automatizados básicos.

## Próximas Melhorias Recomendadas

1. Melhorar cobertura de testes
   - Testar cálculos de relatório com banco vazio.
   - Testar responsividade visual do menu de conta em navegador real.
   - Testar expiração de sessão.

2. Separar CSS
   - Mover estilos de `base.html` para um arquivo estático.
   - Criar `app/static/css/app.css`.
   - Criar `app/static/js/app.js` para tema e filtros.

3. Melhorar persistência
   - Criar migrations simples para SQLite.
   - Adicionar índice em `ativo`, `categoria` e `frequencia` se a lista crescer.

4. Melhorar relatórios
   - Filtro de período.
   - Exportação CSV.
   - Totais por categoria.
   - Evolução mensal manual ou baseada em histórico.

5. Melhorar UX
   - Confirmação mais elegante para inativar.
   - Toasts em vez de alerts.
   - Estado vazio mais visual.
   - Busca por nome.

6. Preparar para produção
   - Configurar `SECRET_KEY` via ambiente.
   - Criar instruções de deploy.
   - Revisar CSP caso os scripts inline sejam movidos para arquivos estáticos.
   - Considerar expiração/rotação de sessão em ambiente público.

## Ideias Futuras

- Histórico de pagamentos.
- Importação/exportação de backup.
- PWA para uso como app simples.

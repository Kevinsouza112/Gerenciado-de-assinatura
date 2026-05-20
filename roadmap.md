# Roadmap

## Pronto

- Estrutura Flask com SQLite.
- Cadastro, edição e listagem.
- Inativação e reativação.
- Duplicação de assinaturas.
- Filtros na tela principal.
- Painel de totais.
- Página de relatórios.
- Melhorias visuais inspiradas em dashboard.
- Tema escuro.
- Testes automatizados básicos.

## Próximas Melhorias Recomendadas

1. Melhorar cobertura de testes
   - Testar validações individualmente.
   - Testar duplicação de assinatura inativa.
   - Testar cálculos de relatório com banco vazio.
   - Testar CSRF em todas as rotas POST.

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
   - Criar `.env.example`.
   - Criar instruções de deploy.
   - Adicionar proteção básica de headers HTTP se publicar.

## Ideias Futuras

- Login local.
- Multiusuário.
- Histórico de pagamentos.
- Notificações de vencimento.
- Importação/exportação de backup.
- PWA para uso como app simples.

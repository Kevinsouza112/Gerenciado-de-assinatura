# Design System: Gerenciador de Assinaturas

## 1. Visual Theme & Atmosphere
Interface de painel administrativo clara, compacta e polida, inspirada na referencia Vega Checkout: sidebar branca, area de trabalho cinza claro, cards brancos com raio consistente, acoes em azul intenso e textos em azul-marinho profundo.

## 2. Colour Palette & Roles
| Role | Name | Value | Usage |
|---|---|---|---|
| Primary | Vega Blue | `#2563eb` | botoes principais, badges, item ativo |
| Primary Dark | Ink Navy | `#020f34` | texto forte, pills ativas, marca |
| Report Heading | Vega Report Navy | `#000c63` | titulos, labels e abas da pagina de relatorios |
| Report Value | Deep Report Ink | `#000c2c` | valores financeiros e textos principais da pagina de relatorios |
| Subscription Heading | Checkout Navy | `#000c39` | titulos, labels e cabecalhos da tela de assinaturas |
| Subscription Muted | Soft Slate | `#516272` | textos auxiliares da tela de assinaturas |
| Subscription Success | Fresh Green | `#34d399` | contadores positivos e indicadores de quantidade |
| Background | Workspace Gray | `#f3f5f9` | fundo da area principal |
| Sidebar | Clean White | `#ffffff` | navegacao lateral e cards |
| Border | Soft Line | `#e3e8f2` | bordas de cards, inputs e tabelas |
| Muted Text | Slate Muted | `#6b7280` | legendas e textos secundarios |
| Success | Mint | `#14b87a` | status ativo e reativar |
| Warning | Warm Yellow | `#fff3cd` | vencimentos próximos |
| Dark Background | Near Black | `#101010` | fundo principal do modo escuro |
| Dark Surface | Charcoal | `#18181b` | cards, sidebar, dropdowns e inputs no modo escuro |
| Dark Active | Graphite | `#2a2a2e` | links e filtros selecionados no modo escuro |

## 3. Typography
| Element | Font | Weight | Size | Line Height |
|---|---|---|---|---|
| H1 | system UI | 700 | 1.75rem | 1.2 |
| H2/H3 | system UI | 700 | 1.1-1.35rem | 1.25 |
| Body | system UI | 400 | 0.95rem | 1.5 |
| Small labels | system UI | 700 | 0.72rem | 1.2 |

## 4. Component Styles
Cards usam fundo branco, borda `#e3e8f2`, raio de 18px e sombra suave. Botões principais são pills azuis, botões secundários são outline pills. Sidebar tem links com ícone, item ativo em azul com texto branco. Tabelas ficam dentro de painéis brancos com cabeçalho discreto e linhas espaçadas.

## 5. Layout Principles
Desktop usa sidebar de 264px fixa e conteúdo com padding de 32px. Mobile empilha sidebar no topo como navegação horizontal rolável. Conteúdo mantém largura fluida e componentes com responsividade Bootstrap.

## 6. Design System Notes for Generation
Use uma estética SaaS operacional: clara, organizada, com sidebar branca, fundo cinza claro, navy para hierarquia e azul forte para comandos. Evite decoração excessiva; priorize leitura rápida, cards financeiros, filtros compactos e tabelas limpas. O modo escuro usa preto e cinza: fundo `#101010`, superfícies `#18181b`, estados ativos `#2a2a2e`, bordas discretas e texto claro com bom contraste.

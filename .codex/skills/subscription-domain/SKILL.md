---
name: subscription-domain
description: Regras de negócio para o sistema de Gerenciador de Assinaturas Pessoais. Use esta skill sempre que o projeto envolver cálculo de custo real de assinaturas, conversão de frequência anual para mensal, lógica de vencimento, divisão de custo entre pessoas, ou qualquer lógica central do domínio de assinaturas. Deve ser consultada antes de implementar qualquer cálculo financeiro ou regra de negócio do sistema.
---

# Subscription Domain — Regras de Negócio

## Modelo de dados

```
Assinatura:
  id          → inteiro, chave primária
  nome        → texto (ex: "Netflix")
  valor       → decimal (ex: 55.90)
  frequencia  → "mensal" ou "anual"
  vencimento  → inteiro, dia do mês (1–28)
  categoria   → "streaming" | "saúde" | "educação" | "outros"
  divisao     → inteiro >= 1 (quantas pessoas dividem, padrão = 1)
  ativo       → booleano (True = ativa, False = cancelada/inativa)
```

---

## Regras de cálculo

### 1. Custo mensal normalizado
Sempre converter para mensal antes de qualquer cálculo de painel:

```python
if assinatura.frequencia == "anual":
    custo_mensal = assinatura.valor / 12
else:
    custo_mensal = assinatura.valor
```

### 2. Custo real (com divisão)
Aplicar divisão após normalizar para mensal:

```python
custo_real_mensal = custo_mensal / assinatura.divisao
```

### 3. Totais do painel
Calcular sobre todas as assinaturas com `ativo == True`:

```python
total_bruto_mensal = sum(custo_mensal(a) for a in assinaturas)
total_real_mensal  = sum(custo_real_mensal(a) for a in assinaturas)
total_bruto_anual  = total_bruto_mensal * 12
total_real_anual   = total_real_mensal * 12
```

### 4. Formatação de valores
Sempre exibir valores monetários com 2 casas decimais:

```python
f"R$ {valor:.2f}"
```

---

## Regras de vencimento

### Calcular dias até vencimento
O campo `vencimento` é o dia do mês (ex: 15). Comparar com o dia atual:

```python
from datetime import date

def dias_ate_vencimento(dia_vencimento: int) -> int:
    hoje = date.today()
    proximo = hoje.replace(day=dia_vencimento)
    if proximo < hoje:
        # vencimento já passou esse mês, calcular pro próximo
        if hoje.month == 12:
            proximo = proximo.replace(year=hoje.year + 1, month=1)
        else:
            proximo = proximo.replace(month=hoje.month + 1)
    return (proximo - hoje).days
```

### Classificação de alerta
| Dias até vencimento | Status | Cor sugerida |
|---|---|---|
| <= 3 dias | Urgente | Vermelho |
| 4 a 7 dias | Próximo | Amarelo |
| > 7 dias | Normal | Sem destaque |

---

## Regras de negócio gerais

- `divisao` nunca pode ser menor que 1. Validar no formulário.
- `vencimento` deve ser entre 1 e 28 (evitar problemas com fevereiro).
- Assinaturas inativas (`ativo = False`) NÃO entram nos cálculos do painel.
- Assinaturas inativas são exibidas em seção separada na listagem.
- Ao "cancelar" uma assinatura, setar `ativo = False` — nunca deletar diretamente (preservar histórico).

---

## Categorias válidas
```python
CATEGORIAS = ["streaming", "saúde", "educação", "outros"]
FREQUENCIAS = ["mensal", "anual"]
```

---

## Evolução futura (não implementar no MVP)
- Campo `nomes_divisao` → lista de quem divide (para calcular quem deve)
- Campo `moeda` → suporte a dólar com conversão automática
- Tabela `pagamento` → histórico de meses pagos por assinatura

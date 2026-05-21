---
name: subscription-domain
description: Regras de negócio para o sistema de Gerenciador de Assinaturas Pessoais. Use esta skill sempre que o projeto envolver cálculo de custo real de assinaturas, conversão de frequência anual para mensal, lógica de vencimento, divisão de custo entre pessoas, ou qualquer lógica central do domínio de assinaturas. Deve ser consultada antes de implementar qualquer cálculo financeiro ou regra de negócio do sistema.
---

# Subscription Domain - Regras de Negócio

## Modelo de Dados

```text
Assinatura:
  id          -> inteiro, chave primária
  nome        -> texto, até 120 caracteres
  valor       -> decimal finito, entre 0 e 1.000.000
  frequencia  -> "mensal" ou "anual"
  vencimento  -> inteiro, dia do mês (1 a 31)
  categoria   -> "streaming" | "saúde" | "educação" | "outros"
  divisao     -> inteiro de 1 a 1000, padrão = 1
  ativo       -> booleano (True = ativa, False = cancelada/inativa)
  user_id     -> dono da assinatura
```

## Regras de Cálculo

### 1. Custo mensal normalizado

Sempre converter para mensal antes de qualquer cálculo de painel:

```python
if assinatura.frequencia == "anual":
    custo_mensal = assinatura.valor / 12
else:
    custo_mensal = assinatura.valor
```

### 2. Custo real com divisão

Aplicar divisão após normalizar para mensal:

```python
custo_real_mensal = custo_mensal / assinatura.divisao
```

### 3. Totais do dashboard

Calcular apenas sobre assinaturas ativas do usuário logado:

```python
total_bruto_mensal = sum(custo_mensal(a) for a in assinaturas_ativas)
total_real_mensal = sum(custo_real_mensal(a) for a in assinaturas_ativas)
total_bruto_anual = total_bruto_mensal * 12
total_real_anual = total_real_mensal * 12
```

### 4. Formatação de valores

Exibir valores monetários com 2 casas decimais e padrão brasileiro:

```text
R$ 1.234,56
```

## Regras de Vencimento

O campo `vencimento` é o dia do mês. Para alerta de curto prazo, comparar com hoje e os próximos 7 dias:

```python
from datetime import date, timedelta

def is_due_soon(vencimento: int, today: date | None = None) -> bool:
    current_date = today or date.today()
    for offset in range(0, 8):
        if (current_date + timedelta(days=offset)).day == vencimento:
            return True
    return False
```

## Regras Gerais

- `divisao` nunca pode ser menor que 1.
- `divisao` deve ser no máximo 1000.
- `vencimento` deve ser entre 1 e 31.
- `valor` precisa ser finito; rejeitar `NaN` e `Infinity`.
- Assinaturas inativas (`ativo = False`) não entram nos cálculos do dashboard.
- Assinaturas inativas são exibidas em seção separada na listagem.
- Ao cancelar uma assinatura, setar `ativo = False`; não deletar fisicamente.
- Toda operação de assinatura deve filtrar por `user_id`.

## Categorias e Frequências Válidas

```python
CATEGORIAS = ("streaming", "saúde", "educação", "outros")
FREQUENCIAS = ("mensal", "anual")
```

## Evolução Futura

- Campo `nomes_divisao` para lista de quem divide.
- Campo `moeda` para suporte a dólar com conversão.
- Tabela `pagamento` para histórico de meses pagos por assinatura.

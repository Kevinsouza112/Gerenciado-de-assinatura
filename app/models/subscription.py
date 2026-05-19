from dataclasses import dataclass


FREQUENCIAS = ("mensal", "anual")
CATEGORIAS = ("streaming", "saúde", "educação", "outros")


@dataclass(frozen=True)
class Subscription:
    id: int | None
    nome: str
    valor: float
    frequencia: str
    vencimento: int
    categoria: str
    divisao: int = 1
    ativo: bool = True

    @property
    def valor_mensal(self) -> float:
        return self.valor / 12 if self.frequencia == "anual" else self.valor

    @property
    def custo_real_mensal(self) -> float:
        return self.valor_mensal / self.divisao

    @property
    def valor_anual(self) -> float:
        return self.valor_mensal * 12

    @property
    def custo_real_anual(self) -> float:
        return self.custo_real_mensal * 12

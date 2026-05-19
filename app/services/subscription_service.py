from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from app.models.subscription import CATEGORIAS, FREQUENCIAS, Subscription
from app.repositories.subscription_repository import SubscriptionRepository


class ValidationError(Exception):
    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        super().__init__("Dados invalidos")


def parse_subscription_form(form) -> Subscription:
    errors: dict[str, str] = {}

    nome = form.get("nome", "").strip()
    if not nome:
        errors["nome"] = "Informe o nome da assinatura."

    try:
        valor = float(Decimal(form.get("valor", "").replace(",", ".")))
        if valor < 0:
            errors["valor"] = "Informe um valor igual ou maior que zero."
    except (InvalidOperation, ValueError):
        valor = 0.0
        errors["valor"] = "Informe um valor numerico valido."

    frequencia = form.get("frequencia", "")
    if frequencia not in FREQUENCIAS:
        errors["frequencia"] = "Escolha uma frequencia valida."

    try:
        vencimento = int(form.get("vencimento", ""))
        if not 1 <= vencimento <= 31:
            errors["vencimento"] = "Informe um dia entre 1 e 31."
    except ValueError:
        vencimento = 1
        errors["vencimento"] = "Informe um dia valido."

    categoria = form.get("categoria", "")
    if categoria not in CATEGORIAS:
        errors["categoria"] = "Escolha uma categoria valida."

    try:
        divisao = int(form.get("divisao", "1"))
        if divisao < 1:
            errors["divisao"] = "A divisao deve ser no minimo 1."
    except ValueError:
        divisao = 1
        errors["divisao"] = "Informe um numero valido."

    ativo = form.get("ativo") == "on"

    if errors:
        raise ValidationError(errors)

    return Subscription(
        id=None,
        nome=nome,
        valor=valor,
        frequencia=frequencia,
        vencimento=vencimento,
        categoria=categoria,
        divisao=divisao,
        ativo=ativo,
    )


def is_due_soon(vencimento: int, today: date | None = None) -> bool:
    current_date = today or date.today()
    for offset in range(0, 8):
        if (current_date + timedelta(days=offset)).day == vencimento:
            return True
    return False


class SubscriptionService:
    def __init__(self, repository: SubscriptionRepository):
        self.repository = repository

    def dashboard(self) -> dict:
        subscriptions = self.repository.list_active()
        total_bruto_mensal = sum(item.valor_mensal for item in subscriptions)
        total_real_mensal = sum(item.custo_real_mensal for item in subscriptions)

        return {
            "subscriptions": subscriptions,
            "due_map": {item.id: is_due_soon(item.vencimento) for item in subscriptions},
            "summary": {
                "total_bruto_mensal": total_bruto_mensal,
                "total_real_mensal": total_real_mensal,
                "total_bruto_anual": total_bruto_mensal * 12,
                "total_real_anual": total_real_mensal * 12,
            },
        }

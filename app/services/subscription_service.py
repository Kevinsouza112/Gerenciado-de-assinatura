from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from app.models.subscription import CATEGORIAS, FREQUENCIAS, Subscription
from app.repositories.subscription_repository import SubscriptionRepository

REPORT_COLORS = {
    "streaming": "#2563eb",
    "saúde": "#14b87a",
    "educação": "#f59e0b",
    "outros": "#0aa2c0",
    "mensal": "#2563eb",
    "anual": "#14b87a",
    "ativas": "#14b87a",
    "inativas": "#ef4444",
}
MAX_SUBSCRIPTION_NAME_LENGTH = 120
MAX_SUBSCRIPTION_VALUE = Decimal("1000000")
MAX_DIVISION = 1000


class ValidationError(Exception):
    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        super().__init__("Dados inválidos")


def parse_subscription_form(form) -> Subscription:
    errors: dict[str, str] = {}

    nome = form.get("nome", "").strip()
    if not nome:
        errors["nome"] = "Informe o nome da assinatura."
    elif len(nome) > MAX_SUBSCRIPTION_NAME_LENGTH:
        errors["nome"] = "O nome deve ter no máximo 120 caracteres."

    try:
        valor_decimal = Decimal(form.get("valor", "").replace(",", "."))
        if not valor_decimal.is_finite():
            errors["valor"] = "Informe um valor numérico válido."
        elif valor_decimal < 0:
            errors["valor"] = "Informe um valor igual ou maior que zero."
        elif valor_decimal > MAX_SUBSCRIPTION_VALUE:
            errors["valor"] = "Informe um valor de até R$ 1.000.000,00."
        valor = float(valor_decimal) if "valor" not in errors else 0.0
    except (InvalidOperation, OverflowError, ValueError):
        valor = 0.0
        errors["valor"] = "Informe um valor numérico válido."

    frequencia = form.get("frequencia", "")
    if frequencia not in FREQUENCIAS:
        errors["frequencia"] = "Escolha uma frequencia valida."

    try:
        vencimento = int(form.get("vencimento", ""))
        if not 1 <= vencimento <= 31:
            errors["vencimento"] = "Informe um dia entre 1 e 31."
    except ValueError:
        vencimento = 1
        errors["vencimento"] = "Informe um dia válido."

    categoria = form.get("categoria", "")
    if categoria not in CATEGORIAS:
        errors["categoria"] = "Escolha uma categoria valida."

    try:
        divisao = int(form.get("divisao", "1"))
        if divisao < 1:
            errors["divisao"] = "A divisão deve ser no mínimo 1."
        elif divisao > MAX_DIVISION:
            errors["divisao"] = "A divisão deve ser no máximo 1000."
    except ValueError:
        divisao = 1
        errors["divisao"] = "Informe um número válido."

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


def _percent(value: float, total: float) -> int:
    if total == 0:
        return 0
    return round((value / total) * 100)


class SubscriptionService:
    def __init__(self, repository: SubscriptionRepository):
        self.repository = repository

    def dashboard(self, user_id: int) -> dict:
        subscriptions = self.repository.list_active(user_id)
        inactive_subscriptions = self.repository.list_inactive(user_id)
        total_bruto_mensal = sum(item.valor_mensal for item in subscriptions)
        total_real_mensal = sum(item.custo_real_mensal for item in subscriptions)

        return {
            "subscriptions": subscriptions,
            "inactive_subscriptions": inactive_subscriptions,
            "due_map": {item.id: is_due_soon(item.vencimento) for item in subscriptions},
            "summary": {
                "total_bruto_mensal": total_bruto_mensal,
                "total_real_mensal": total_real_mensal,
                "total_bruto_anual": total_bruto_mensal * 12,
                "total_real_anual": total_real_mensal * 12,
            },
        }

    def reports(self, user_id: int) -> dict:
        subscriptions = self.repository.list_active(user_id)
        inactive_subscriptions = self.repository.list_inactive(user_id)
        total_bruto_mensal = sum(item.valor_mensal for item in subscriptions)
        total_real_mensal = sum(item.custo_real_mensal for item in subscriptions)
        total_count = len(subscriptions) + len(inactive_subscriptions)

        category_rows = []
        category_segments = []
        category_degrees = 0
        for categoria in CATEGORIAS:
            items = [item for item in subscriptions if item.categoria == categoria]
            total = sum(item.custo_real_mensal for item in items)
            degrees = (total / total_real_mensal * 360) if total_real_mensal else 0
            next_degrees = category_degrees + degrees
            color = REPORT_COLORS.get(categoria, "#6b7280")
            if degrees > 0:
                category_segments.append(f"{color} {category_degrees:.1f}deg {next_degrees:.1f}deg")
            category_degrees = next_degrees
            category_rows.append(
                {
                    "name": categoria,
                    "count": len(items),
                    "total": total,
                    "percent": _percent(total, total_real_mensal),
                    "color": color,
                }
            )

        frequency_rows = []
        for frequencia in FREQUENCIAS:
            items = [item for item in subscriptions if item.frequencia == frequencia]
            frequency_rows.append(
                {
                    "name": frequencia,
                    "count": len(items),
                    "percent": _percent(len(items), len(subscriptions)),
                    "color": REPORT_COLORS.get(frequencia, "#6b7280"),
                }
            )

        status_rows = [
            {
                "name": "Ativas",
                "count": len(subscriptions),
                "percent": _percent(len(subscriptions), total_count),
                "color": REPORT_COLORS["ativas"],
            },
            {
                "name": "Inativas",
                "count": len(inactive_subscriptions),
                "percent": _percent(len(inactive_subscriptions), total_count),
                "color": REPORT_COLORS["inativas"],
            },
        ]

        today = date.today()
        due_counts = []
        for offset in range(7):
            current = today + timedelta(days=offset)
            due_counts.append((current, sum(1 for item in subscriptions if item.vencimento == current.day)))

        due_points = []
        max_due_count = max([count for _, count in due_counts] + [1])
        for offset, (current, count) in enumerate(due_counts):
            due_points.append(
                {
                    "label": current.strftime("%d/%m"),
                    "count": count,
                    "x": 48 + (offset * 120),
                    "y": 230 - (count / max_due_count * 170 if max_due_count else 0),
                }
            )

        return {
            "subscriptions": subscriptions,
            "inactive_subscriptions": inactive_subscriptions,
            "summary": {
                "total_bruto_mensal": total_bruto_mensal,
                "total_real_mensal": total_real_mensal,
                "total_bruto_anual": total_bruto_mensal * 12,
                "total_real_anual": total_real_mensal * 12,
            },
            "report": {
                "active_count": len(subscriptions),
                "inactive_count": len(inactive_subscriptions),
                "category_rows": category_rows,
                "frequency_rows": frequency_rows,
                "status_rows": status_rows,
                "due_points": due_points,
                "due_polyline": " ".join(f"{point['x']},{point['y']}" for point in due_points),
                "category_conic": ", ".join(category_segments) if category_segments else "#e4e7ec 0deg 360deg",
                "top_costs": sorted(subscriptions, key=lambda item: item.custo_real_mensal, reverse=True)[:5],
                "updated_at": date.today().strftime("%d/%m/%Y"),
            },
        }

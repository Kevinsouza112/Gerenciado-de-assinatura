from app.database.connection import get_db
from app.models.subscription import Subscription


def _row_to_subscription(row) -> Subscription:
    return Subscription(
        id=row["id"],
        nome=row["nome"],
        valor=float(row["valor"]),
        frequencia=row["frequencia"],
        vencimento=int(row["vencimento"]),
        categoria=row["categoria"],
        divisao=int(row["divisao"]),
        ativo=bool(row["ativo"]),
    )


class SubscriptionRepository:
    def list_active(self) -> list[Subscription]:
        rows = get_db().execute(
            """
            SELECT id, nome, valor, frequencia, vencimento, categoria, divisao, ativo
            FROM assinatura
            WHERE ativo = 1
            ORDER BY vencimento ASC, nome ASC
            """
        ).fetchall()
        return [_row_to_subscription(row) for row in rows]

    def list_inactive(self) -> list[Subscription]:
        rows = get_db().execute(
            """
            SELECT id, nome, valor, frequencia, vencimento, categoria, divisao, ativo
            FROM assinatura
            WHERE ativo = 0
            ORDER BY nome ASC
            """
        ).fetchall()
        return [_row_to_subscription(row) for row in rows]

    def get_by_id(self, subscription_id: int) -> Subscription | None:
        row = get_db().execute(
            """
            SELECT id, nome, valor, frequencia, vencimento, categoria, divisao, ativo
            FROM assinatura
            WHERE id = ?
            """,
            (subscription_id,),
        ).fetchone()
        return _row_to_subscription(row) if row else None

    def create(self, subscription: Subscription) -> None:
        get_db().execute(
            """
            INSERT INTO assinatura (nome, valor, frequencia, vencimento, categoria, divisao, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                subscription.nome,
                subscription.valor,
                subscription.frequencia,
                subscription.vencimento,
                subscription.categoria,
                subscription.divisao,
                int(subscription.ativo),
            ),
        )
        get_db().commit()

    def update(self, subscription_id: int, subscription: Subscription) -> None:
        get_db().execute(
            """
            UPDATE assinatura
            SET nome = ?, valor = ?, frequencia = ?, vencimento = ?, categoria = ?, divisao = ?, ativo = ?
            WHERE id = ?
            """,
            (
                subscription.nome,
                subscription.valor,
                subscription.frequencia,
                subscription.vencimento,
                subscription.categoria,
                subscription.divisao,
                int(subscription.ativo),
                subscription_id,
            ),
        )
        get_db().commit()

    def deactivate(self, subscription_id: int) -> None:
        get_db().execute("UPDATE assinatura SET ativo = 0 WHERE id = ?", (subscription_id,))
        get_db().commit()

    def activate(self, subscription_id: int) -> None:
        get_db().execute("UPDATE assinatura SET ativo = 1 WHERE id = ?", (subscription_id,))
        get_db().commit()

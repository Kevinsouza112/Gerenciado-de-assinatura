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
    def list_active(self, user_id: int) -> list[Subscription]:
        rows = get_db().execute(
            """
            SELECT id, nome, valor, frequencia, vencimento, categoria, divisao, ativo
            FROM assinatura
            WHERE ativo = 1 AND user_id = ?
            ORDER BY vencimento ASC, nome ASC
            """,
            (user_id,),
        ).fetchall()
        return [_row_to_subscription(row) for row in rows]

    def list_inactive(self, user_id: int) -> list[Subscription]:
        rows = get_db().execute(
            """
            SELECT id, nome, valor, frequencia, vencimento, categoria, divisao, ativo
            FROM assinatura
            WHERE ativo = 0 AND user_id = ?
            ORDER BY nome ASC
            """,
            (user_id,),
        ).fetchall()
        return [_row_to_subscription(row) for row in rows]

    def get_by_id(self, subscription_id: int, user_id: int) -> Subscription | None:
        row = get_db().execute(
            """
            SELECT id, nome, valor, frequencia, vencimento, categoria, divisao, ativo
            FROM assinatura
            WHERE id = ? AND user_id = ?
            """,
            (subscription_id, user_id),
        ).fetchone()
        return _row_to_subscription(row) if row else None

    def create(self, subscription: Subscription, user_id: int) -> None:
        get_db().execute(
            """
            INSERT INTO assinatura (nome, valor, frequencia, vencimento, categoria, divisao, ativo, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                subscription.nome,
                subscription.valor,
                subscription.frequencia,
                subscription.vencimento,
                subscription.categoria,
                subscription.divisao,
                int(subscription.ativo),
                user_id,
            ),
        )
        get_db().commit()

    def update(self, subscription_id: int, subscription: Subscription, user_id: int) -> None:
        get_db().execute(
            """
            UPDATE assinatura
            SET nome = ?, valor = ?, frequencia = ?, vencimento = ?, categoria = ?, divisao = ?, ativo = ?
            WHERE id = ? AND user_id = ?
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
                user_id,
            ),
        )
        get_db().commit()

    def deactivate(self, subscription_id: int, user_id: int) -> None:
        get_db().execute(
            "UPDATE assinatura SET ativo = 0 WHERE id = ? AND user_id = ?",
            (subscription_id, user_id),
        )
        get_db().commit()

    def activate(self, subscription_id: int, user_id: int) -> None:
        get_db().execute(
            "UPDATE assinatura SET ativo = 1 WHERE id = ? AND user_id = ?",
            (subscription_id, user_id),
        )
        get_db().commit()

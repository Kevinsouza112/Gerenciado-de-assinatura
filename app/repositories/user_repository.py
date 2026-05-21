from app.database.connection import get_db
from app.models.user import User


def _row_to_user(row) -> User:
    return User(
        id=row["id"],
        nome=row["nome"],
        email=row["email"],
        password_hash=row["password_hash"],
    )


class UserRepository:
    def get_by_id(self, user_id: int) -> User | None:
        row = get_db().execute(
            """
            SELECT id, nome, email, password_hash
            FROM usuario
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()
        return _row_to_user(row) if row else None

    def get_by_email(self, email: str) -> User | None:
        row = get_db().execute(
            """
            SELECT id, nome, email, password_hash
            FROM usuario
            WHERE email = ?
            """,
            (email,),
        ).fetchone()
        return _row_to_user(row) if row else None

    def create(self, nome: str, email: str, password_hash: str) -> User:
        cursor = get_db().execute(
            """
            INSERT INTO usuario (nome, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (nome, email, password_hash),
        )
        get_db().commit()
        return User(id=cursor.lastrowid, nome=nome, email=email, password_hash=password_hash)

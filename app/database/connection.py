from pathlib import Path
import sqlite3

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        db_path = Path(current_app.instance_path) / current_app.config["DATABASE"]
        db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection

    return g.db


def close_db(error=None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def _assinatura_column_exists(column: str) -> bool:
    rows = get_db().execute("PRAGMA table_info(assinatura)").fetchall()
    return any(row["name"] == column for row in rows)


def init_db() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS assinatura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL CHECK (valor >= 0),
            frequencia TEXT NOT NULL CHECK (frequencia IN ('mensal', 'anual')),
            vencimento INTEGER NOT NULL CHECK (vencimento BETWEEN 1 AND 31),
            categoria TEXT NOT NULL CHECK (categoria IN ('streaming', 'saúde', 'educação', 'outros')),
            divisao INTEGER NOT NULL DEFAULT 1 CHECK (divisao >= 1),
            ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
            notificar_dias_antes INTEGER NOT NULL DEFAULT 7 CHECK (notificar_dias_antes BETWEEN 0 AND 31),
            user_id INTEGER NOT NULL REFERENCES usuario(id)
        )
        """
    )
    if not _assinatura_column_exists("user_id"):
        db.execute("ALTER TABLE assinatura ADD COLUMN user_id INTEGER REFERENCES usuario(id)")
    if not _assinatura_column_exists("notificar_dias_antes"):
        db.execute(
            "ALTER TABLE assinatura ADD COLUMN notificar_dias_antes INTEGER NOT NULL DEFAULT 7 "
            "CHECK (notificar_dias_antes BETWEEN 0 AND 31)"
        )

    null_user_rows = db.execute("SELECT COUNT(*) AS total FROM assinatura WHERE user_id IS NULL").fetchone()["total"]
    if null_user_rows:
        current_app.logger.warning(
            "Existem %s assinatura(s) sem user_id; associe-as a um usuario antes de exigir NOT NULL no banco existente.",
            null_user_rows,
        )

    db.execute("CREATE INDEX IF NOT EXISTS idx_assinatura_user_ativo ON assinatura (user_id, ativo)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_assinatura_user_vencimento ON assinatura (user_id, ativo, vencimento)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuario (email)")
    db.commit()

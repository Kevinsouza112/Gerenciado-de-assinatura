from pathlib import Path
import sqlite3

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        db_path = Path(current_app.instance_path) / current_app.config["DATABASE"]
        db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        g.db = connection

    return g.db


def close_db(error=None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db() -> None:
    db = get_db()
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
            ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
        )
        """
    )
    db.commit()

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int | None
    nome: str
    email: str
    password_hash: str

import re
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.subscription_service import ValidationError


PASSWORD_REQUIREMENTS_MESSAGE = (
    "A senha deve ter pelo menos 6 caracteres, com uma letra maiúscula, "
    "uma letra minúscula e um caractere especial."
)
MAX_NAME_LENGTH = 120
MAX_EMAIL_LENGTH = 254
MAX_PASSWORD_LENGTH = 128
EMAIL_PATTERN = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.IGNORECASE)


def _password_is_strong(password: str) -> bool:
    return (
        len(password) >= 6
        and any(char.isupper() for char in password)
        and any(char.islower() for char in password)
        and any(not char.isalnum() and not char.isspace() for char in password)
    )


def _email_is_valid(email: str) -> bool:
    if len(email) > MAX_EMAIL_LENGTH:
        return False
    if not EMAIL_PATTERN.fullmatch(email):
        return False
    local_part, domain = email.rsplit("@", 1)
    return bool(local_part) and "." in domain and ".." not in email


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, form) -> User:
        errors: dict[str, str] = {}
        nome = form.get("nome", "").strip()
        email = form.get("email", "").strip().lower()
        senha = form.get("senha", "")
        confirmar_senha = form.get("confirmar_senha", "")

        if not nome:
            errors["nome"] = "Informe seu nome."
        elif len(nome) > MAX_NAME_LENGTH:
            errors["nome"] = "O nome deve ter no máximo 120 caracteres."
        if len(email) > MAX_EMAIL_LENGTH:
            errors["email"] = "O e-mail deve ter no máximo 254 caracteres."
        elif not _email_is_valid(email):
            errors["email"] = "Informe um e-mail válido."
        elif self.repository.get_by_email(email):
            errors["email"] = "Este e-mail já está cadastrado."
        if len(senha) > MAX_PASSWORD_LENGTH:
            errors["senha"] = "A senha deve ter no máximo 128 caracteres."
        elif not _password_is_strong(senha):
            errors["senha"] = PASSWORD_REQUIREMENTS_MESSAGE
        if senha != confirmar_senha:
            errors["confirmar_senha"] = "As senhas não conferem."

        if errors:
            raise ValidationError(errors)

        try:
            return self.repository.create(nome=nome, email=email, password_hash=generate_password_hash(senha))
        except sqlite3.IntegrityError as exc:
            if "usuario.email" in str(exc):
                raise ValidationError({"email": "Este e-mail já está cadastrado."}) from exc
            raise

    def authenticate(self, form) -> User:
        errors: dict[str, str] = {}
        email = form.get("email", "").strip().lower()
        senha = form.get("senha", "")

        if not _email_is_valid(email):
            errors["email"] = "Informe um e-mail válido."
            raise ValidationError(errors)

        user = self.repository.get_by_email(email)

        if user is None or not check_password_hash(user.password_hash, senha):
            errors["email"] = "E-mail ou senha inválidos."

        if errors:
            raise ValidationError(errors)

        return user

    def change_password(self, user: User, form) -> None:
        errors: dict[str, str] = {}
        senha_atual = form.get("senha_atual", "")
        nova_senha = form.get("nova_senha", "")
        confirmar_nova_senha = form.get("confirmar_nova_senha", "")

        if not check_password_hash(user.password_hash, senha_atual):
            errors["senha_atual"] = "Senha atual incorreta."
        if len(nova_senha) > MAX_PASSWORD_LENGTH:
            errors["nova_senha"] = "A senha deve ter no máximo 128 caracteres."
        elif not _password_is_strong(nova_senha):
            errors["nova_senha"] = PASSWORD_REQUIREMENTS_MESSAGE
        elif senha_atual and nova_senha == senha_atual:
            errors["nova_senha"] = "A nova senha deve ser diferente da senha atual."
        if nova_senha != confirmar_nova_senha:
            errors["confirmar_nova_senha"] = "As senhas não conferem."

        if errors:
            raise ValidationError(errors)

        self.repository.update_password(user.id, generate_password_hash(nova_senha))

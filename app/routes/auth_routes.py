from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.repositories.user_repository import UserRepository
from app.security import csrf_token, validate_csrf
from app.services.auth_service import AuthService
from app.services.subscription_service import ValidationError


auth_bp = Blueprint("auth", __name__)


def _auth_service() -> AuthService:
    return AuthService(UserRepository())


def _login_user(user) -> None:
    session.clear()
    session.permanent = True
    session["user_id"] = user.id
    session["user_name"] = user.nome


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.get("current_user") is None:
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user() -> None:
    user_id = session.get("user_id")
    g.current_user = UserRepository().get_by_id(user_id) if user_id else None


@auth_bp.app_context_processor
def inject_auth_globals():
    return {"current_user": g.get("current_user"), "csrf_token": csrf_token}


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def register():
    errors = {}
    form_data = {}

    if request.method == "POST":
        validate_csrf()
        form_data = request.form.to_dict()
        try:
            user = _auth_service().register(request.form)
            _login_user(user)
            flash("Cadastro realizado com sucesso.", "success")
            return redirect(url_for("subscriptions.dashboard"))
        except ValidationError as error:
            errors = error.errors

    return render_template("auth/register.html", errors=errors, form_data=form_data, title="Cadastro")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    errors = {}
    form_data = {}

    if request.method == "POST":
        validate_csrf()
        form_data = request.form.to_dict()
        try:
            user = _auth_service().authenticate(request.form)
            _login_user(user)
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("subscriptions.dashboard"))
        except ValidationError as error:
            errors = error.errors

    return render_template("auth/login.html", errors=errors, form_data=form_data, title="Login")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    validate_csrf()
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("auth.login"))

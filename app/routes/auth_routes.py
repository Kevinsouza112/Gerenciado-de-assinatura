from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.repositories.subscription_repository import SubscriptionRepository
from app.repositories.user_repository import UserRepository
from app.security import csrf_token, validate_csrf
from app.services.auth_service import AuthService
from app.services.subscription_service import SubscriptionService, ValidationError


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
    current_user = g.get("current_user")
    notifications = []
    if current_user:
        notifications = SubscriptionService(SubscriptionRepository()).notifications(current_user.id)
    return {
        "current_user": current_user,
        "account_initials": _user_initials(current_user) if current_user else "",
        "csrf_token": csrf_token,
        "notifications": notifications,
        "notifications_count": len(notifications),
    }


def _user_initials(user) -> str:
    parts = [part[0] for part in user.nome.strip().split() if part]
    if not parts:
        return user.email[:2].upper()
    return "".join(parts[:2]).upper()


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


@auth_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def profile():
    errors = {}

    if request.method == "POST":
        validate_csrf()
        try:
            _auth_service().change_password(g.current_user, request.form)
            flash("Senha alterada com sucesso.", "success")
            return redirect(url_for("auth.profile"))
        except ValidationError as error:
            errors = error.errors

    return render_template(
        "auth/profile.html",
        errors=errors,
        user=g.current_user,
        initials=_user_initials(g.current_user),
        title="Minha Conta",
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    validate_csrf()
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("auth.login"))

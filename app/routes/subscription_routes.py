from secrets import compare_digest, token_urlsafe

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.models.subscription import CATEGORIAS, FREQUENCIAS
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.subscription_service import SubscriptionService, ValidationError, parse_subscription_form


subscription_bp = Blueprint("subscriptions", __name__)


def _repository() -> SubscriptionRepository:
    return SubscriptionRepository()


def _service() -> SubscriptionService:
    return SubscriptionService(_repository())


def _csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = token_urlsafe(32)
    return session["csrf_token"]


def _validate_csrf() -> None:
    token = request.form.get("csrf_token", "")
    if not compare_digest(token, session.get("csrf_token", "")):
        abort(400)


def _subscription_to_form_data(subscription) -> dict:
    return {
        "nome": subscription.nome,
        "valor": subscription.valor,
        "frequencia": subscription.frequencia,
        "vencimento": subscription.vencimento,
        "categoria": subscription.categoria,
        "divisao": subscription.divisao,
        "ativo": subscription.ativo,
    }


@subscription_bp.context_processor
def inject_globals():
    return {
        "csrf_token": _csrf_token,
        "frequencias": FREQUENCIAS,
        "categorias": CATEGORIAS,
    }


@subscription_bp.app_template_filter("money")
def money_filter(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@subscription_bp.route("/")
def index():
    data = _service().dashboard()
    return render_template("index.html", **data)


@subscription_bp.route("/favicon.ico")
def favicon():
    return "", 204


@subscription_bp.route("/nova", methods=["GET", "POST"])
def create_subscription():
    errors = {}
    form_data = {"ativo": True, "divisao": 1, "frequencia": "mensal", "categoria": "outros"}

    if request.method == "POST":
        _validate_csrf()
        form_data = request.form.to_dict()
        try:
            subscription = parse_subscription_form(request.form)
            _repository().create(subscription)
            flash("Assinatura cadastrada com sucesso.", "success")
            return redirect(url_for("subscriptions.index"))
        except ValidationError as error:
            errors = error.errors

    return render_template("form.html", errors=errors, form_data=form_data, title="Nova assinatura")


@subscription_bp.route("/editar/<int:subscription_id>", methods=["GET", "POST"])
def edit_subscription(subscription_id: int):
    repository = _repository()
    existing = repository.get_by_id(subscription_id)
    if existing is None:
        abort(404)

    errors = {}
    form_data = _subscription_to_form_data(existing)

    if request.method == "POST":
        _validate_csrf()
        form_data = request.form.to_dict()
        try:
            subscription = parse_subscription_form(request.form)
            repository.update(subscription_id, subscription)
            flash("Assinatura atualizada com sucesso.", "success")
            return redirect(url_for("subscriptions.index"))
        except ValidationError as error:
            errors = error.errors

    return render_template("form.html", errors=errors, form_data=form_data, title="Editar assinatura")


@subscription_bp.route("/excluir/<int:subscription_id>", methods=["POST"])
def delete_subscription(subscription_id: int):
    _validate_csrf()
    _repository().delete(subscription_id)
    flash("Assinatura excluida com sucesso.", "success")
    return redirect(url_for("subscriptions.index"))

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.models.subscription import CATEGORIAS, FREQUENCIAS, Subscription
from app.repositories.subscription_repository import SubscriptionRepository
from app.routes.auth_routes import login_required
from app.security import csrf_token, validate_csrf
from app.services.subscription_service import SubscriptionService, ValidationError, parse_subscription_form


subscription_bp = Blueprint("subscriptions", __name__)


def _repository() -> SubscriptionRepository:
    return SubscriptionRepository()


def _service() -> SubscriptionService:
    return SubscriptionService(_repository())


def _subscription_to_form_data(subscription) -> dict:
    return {
        "nome": subscription.nome,
        "valor": subscription.valor,
        "frequencia": subscription.frequencia,
        "vencimento": subscription.vencimento,
        "categoria": subscription.categoria,
        "divisao": subscription.divisao,
        "ativo": subscription.ativo,
        "notificar_dias_antes": subscription.notificar_dias_antes,
    }


@subscription_bp.context_processor
def inject_globals():
    return {
        "csrf_token": csrf_token,
        "frequencias": FREQUENCIAS,
        "categorias": CATEGORIAS,
    }


@subscription_bp.app_template_filter("money")
def money_filter(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@subscription_bp.route("/")
@login_required
def index():
    data = _service().dashboard(session["user_id"])
    return render_template("index.html", **data)


@subscription_bp.route("/relatorios")
@login_required
def reports():
    return redirect(url_for("subscriptions.dashboard"))


@subscription_bp.route("/dashboard")
@login_required
def dashboard():
    data = _service().reports(session["user_id"])
    return render_template("reports.html", **data, title="Dashboard")


@subscription_bp.route("/favicon.ico")
def favicon():
    return "", 204


@subscription_bp.route("/nova", methods=["GET", "POST"])
@login_required
def create_subscription():
    errors = {}
    form_data = {
        "ativo": True,
        "divisao": 1,
        "frequencia": "mensal",
        "categoria": "outros",
        "notificar_dias_antes": 7,
    }

    if request.method == "POST":
        validate_csrf()
        form_data = request.form.to_dict()
        try:
            subscription = parse_subscription_form(request.form)
            _repository().create(subscription, session["user_id"])
            flash("Assinatura cadastrada com sucesso.", "success")
            return redirect(url_for("subscriptions.index"))
        except ValidationError as error:
            errors = error.errors

    return render_template("form.html", errors=errors, form_data=form_data, title="Nova assinatura")


@subscription_bp.route("/editar/<int:subscription_id>", methods=["GET", "POST"])
@login_required
def edit_subscription(subscription_id: int):
    repository = _repository()
    existing = repository.get_by_id(subscription_id, session["user_id"])
    if existing is None:
        abort(404)

    errors = {}
    form_data = _subscription_to_form_data(existing)

    if request.method == "POST":
        validate_csrf()
        form_data = request.form.to_dict()
        try:
            subscription = parse_subscription_form(request.form)
            repository.update(subscription_id, subscription, session["user_id"])
            flash("Assinatura atualizada com sucesso.", "success")
            return redirect(url_for("subscriptions.index"))
        except ValidationError as error:
            errors = error.errors

    return render_template("form.html", errors=errors, form_data=form_data, title="Editar assinatura")


@subscription_bp.route("/excluir/<int:subscription_id>", methods=["POST"])
@login_required
def delete_subscription(subscription_id: int):
    validate_csrf()
    repository = _repository()
    if repository.get_by_id(subscription_id, session["user_id"]) is None:
        abort(404)

    repository.deactivate(subscription_id, session["user_id"])
    flash("Assinatura marcada como inativa.", "success")
    return redirect(url_for("subscriptions.index"))


@subscription_bp.route("/duplicar/<int:subscription_id>", methods=["POST"])
@login_required
def duplicate_subscription(subscription_id: int):
    validate_csrf()
    repository = _repository()
    existing = repository.get_by_id(subscription_id, session["user_id"])
    if existing is None:
        abort(404)

    repository.create(
        Subscription(
            id=None,
            nome=f"{existing.nome} (copia)",
            valor=existing.valor,
            frequencia=existing.frequencia,
            vencimento=existing.vencimento,
            categoria=existing.categoria,
            divisao=existing.divisao,
            ativo=existing.ativo,
            notificar_dias_antes=existing.notificar_dias_antes,
        ),
        session["user_id"],
    )
    flash("Assinatura duplicada com sucesso.", "success")
    return redirect(url_for("subscriptions.index"))


@subscription_bp.route("/reativar/<int:subscription_id>", methods=["POST"])
@login_required
def reactivate_subscription(subscription_id: int):
    validate_csrf()
    repository = _repository()
    if repository.get_by_id(subscription_id, session["user_id"]) is None:
        abort(404)

    repository.activate(subscription_id, session["user_id"])
    flash("Assinatura reativada com sucesso.", "success")
    return redirect(url_for("subscriptions.index"))

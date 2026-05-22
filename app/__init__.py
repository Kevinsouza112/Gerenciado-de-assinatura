from datetime import timedelta
from secrets import token_urlsafe

from flask import Flask, g

from app.database.connection import close_db, init_db
from app.routes.auth_routes import auth_bp
from app.routes.subscription_routes import subscription_bp


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        APP_ENV="development",
        DATABASE="assinaturas.sqlite3",
        SECRET_KEY="dev-change-me",
        MAX_CONTENT_LENGTH=64 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
    )
    app.config.from_prefixed_env()
    if test_config:
        app.config.update(test_config)

    if app.config["APP_ENV"] == "production" and app.config["SECRET_KEY"] == "dev-change-me":
        raise RuntimeError("Configure FLASK_SECRET_KEY antes de iniciar em producao.")
    if app.config["APP_ENV"] == "production":
        app.config["SESSION_COOKIE_SECURE"] = True

    @app.before_request
    def set_csp_nonce() -> None:
        g.csp_nonce = token_urlsafe(16)

    @app.after_request
    def add_security_headers(response):
        nonce = getattr(g, "csp_nonce", "")
        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'"
        )
        response.headers.setdefault("Content-Security-Policy", csp)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        return response

    app.teardown_appcontext(close_db)
    app.register_blueprint(auth_bp)
    app.register_blueprint(subscription_bp)

    with app.app_context():
        init_db()

    return app

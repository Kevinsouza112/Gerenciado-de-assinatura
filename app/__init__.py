from datetime import timedelta

from flask import Flask

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

    @app.after_request
    def add_security_headers(response):
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

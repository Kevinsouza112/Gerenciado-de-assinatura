from flask import Flask

from app.database.connection import close_db, init_db
from app.routes.subscription_routes import subscription_bp


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE="assinaturas.sqlite3",
        SECRET_KEY="dev-change-me",
    )
    app.config.from_prefixed_env()
    if test_config:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)
    app.register_blueprint(subscription_bp)

    with app.app_context():
        init_db()

    return app

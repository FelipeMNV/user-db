import os
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db
from flask_bcrypt import Bcrypt

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(environment=os.environ.get("ENVIRONMENT", "Development")):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    # Create instance folder if it doesn't exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Registrando CLI Commands e inicializando extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Registrando blueprints
    from src.controllers import user, post, auth, role

    app.register_blueprint(user.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(role.bp)

    return app

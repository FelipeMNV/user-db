import os
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db
from flask_bcrypt import Bcrypt

# Instâncias das extensões Flask
migrate = Migrate()  # Para gerenciamento de migrações do banco de dados
jwt = JWTManager()  # Para gerenciamento de autenticação JWT
bcrypt = Bcrypt()  # Para hash e verificação de senhas


def create_app(environment=os.environ["ENVIRONMENT"]):
    """
    Função para criar e configurar a aplicação Flask.

    :param environment: O ambiente de configuração (Development, Testing, Production).
                        O padrão é obtido da variável de ambiente `ENVIRONMENT`.
    :return: Instância da aplicação Flask configurada.
    """
    # Cria uma instância do Flask
    app = Flask(__name__, instance_relative_config=True)

    # Carrega a configuração apropriada com base no ambiente
    app.config.from_object(f"src.config.{environment.title()}Config")

    # Cria a pasta da instância se não existir
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa as extensões com a aplicação
    db.init_app(app)  # Inicializa a extensão de banco de dados
    migrate.init_app(app, db)  # Inicializa a extensão de migrações com o banco de dados
    jwt.init_app(app)  # Inicializa a extensão JWT
    bcrypt.init_app(app)  # Inicializa a extensão Bcrypt

    # Importa e registra os blueprints
    from src.controllers import user, post, auth, role

    app.register_blueprint(user.bp)  # Registra o blueprint de usuário
    app.register_blueprint(post.bp)  # Registra o blueprint de postagens
    app.register_blueprint(auth.bp)  # Registra o blueprint de autenticação
    app.register_blueprint(role.bp)  # Registra o blueprint de papéis

    return app

from flask import Blueprint, request
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import create_access_token
from src.models import db, User
from src.app import bcrypt

# Cria um blueprint para a autenticação, com prefixo de URL '/auth'
bp = Blueprint("auth", __name__, url_prefix="/auth")


def _check_password(password_hash, password_raw):
    """
    Verifica se a senha fornecida corresponde ao hash da senha armazenada.

    :param password_hash: Hash da senha armazenada
    :param password_raw: Senha fornecida pelo usuário
    :return: True se a senha corresponder ao hash, False caso contrário
    """
    return bcrypt.check_password_hash(password_hash, password_raw)


@bp.route("/login", methods=["POST"])
def login():
    """
    Endpoint para login do usuário. Verifica o nome de usuário e a senha fornecidos,
    e se estiverem corretos, retorna um token de acesso JWT.

    :return: JSON com o token de acesso JWT se as credenciais forem válidas,
            ou uma mensagem de erro e status 401 se forem inválidas
    """
    # Obtém o nome de usuário e a senha do corpo da requisição JSON
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Busca o usuário no banco de dados pelo nome de usuário
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    # Verifica se o usuário existe e se a senha está correta
    if not user or not _check_password(user.password, password):
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    # Cria um token de acesso JWT com o ID do usuário como identidade
    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}

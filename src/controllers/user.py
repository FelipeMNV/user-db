from flask import Blueprint, request
from src.models import User, db
from http import HTTPStatus
from src.utils import requires_role
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required
from src.app import bcrypt

bp = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {"id": user.role.id, "name": user.role.name},
        }
        for user in users
    ]


@bp.route("/", methods=["GET", "POST"])
def list_or_create_user():
    if request.method == "POST":
        # Criação de usuário não requer autenticação
        _create_user()
        return {"message": "User created"}, HTTPStatus.CREATED
    else:
        # Listar usuários requer autenticação
        jwt_required()
        return {"users": _list_users()}


@bp.route("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return [
        {
            "id": user.id,
            "username": user.username,
        }
    ]


@bp.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return [
        {
            "id": user.id,
            "username": user.username,
        }
    ]


@bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT

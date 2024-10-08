from flask import Blueprint, request
from src.models import Role, db
from http import HTTPStatus

bp = Blueprint("role", __name__, url_prefix="/roles")


@bp.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created"}, HTTPStatus.CREATED

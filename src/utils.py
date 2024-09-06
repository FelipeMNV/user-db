from flask_jwt_extended import get_jwt_identity
from src.models import User, db
from http import HTTPStatus
from functools import wraps


def requires_role(role_name):
    """
    Decorador para restringir o acesso a uma função com base no papel do usuário.
    Verifica se o usuário possui o papel necessário para acessar o endpoint.

    :param role_name: Nome do papel que o usuário deve ter para acessar a função
    :return: Função decorada que verifica o papel do usuário antes de chamar a função original
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Obtém a identidade do usuário a partir do token JWT
            user_id = get_jwt_identity()
            # Obtém o usuário correspondente ao ID (ou retorna 404 se não encontrado)
            user = db.get_or_404(User, user_id)

            # Verifica se o papel do usuário corresponde ao papel exigido
            if user.role.name != role_name:
                return {"message": "User dont have access"}, HTTPStatus.FORBIDDEN

            # Chama a função original se o papel estiver correto
            return f(*args, **kwargs)

        return wrapped

    return decorator


def eleva_quadrado(x):
    """
    Função que eleva um número ao quadrado.

    :param x: Número a ser elevado ao quadrado
    :return: O quadrado do número fornecido
    """
    return x**2

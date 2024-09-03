from src.utils import eleva_quadrado, requires_role
from unittest.mock import patch
import pytest
from http import HTTPStatus


def test_requires_role(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decoreted_fuction = requires_role("admin")(lambda: "sucess")
    result = decoreted_fuction()
    assert result == "sucess"


def test_requires_role_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decoreted_fuction = requires_role("admin")(lambda: "fail")
    result = decoreted_fuction()

    assert result == ({"message": "User dont have acess"}, HTTPStatus.FORBIDDEN)

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import db


class User(db.Model):
    """
    Modelo de usuário para o banco de dados.
    Representa um usuário com um nome de usuário, senha e papel associado.
    """

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))

    # Relacionamento com Role
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    def __repr__(self) -> str:
        """
        Representação em string do modelo User.

        :return: Representação do usuário como uma string
        """
        return f"User(id={self.id!r}, username={self.username!r})"


class Role(db.Model):
    """
    Modelo de papel para o banco de dados.
    Representa um papel com um nome e uma lista de usuários associados.
    """

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    # Relacionamento com User
    users: Mapped[list[User]] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        """
        Representação em string do modelo Role.

        :return: Representação do papel como uma string
        """
        return f"Role(id={self.id!r}, name={self.name!r})"

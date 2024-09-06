from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    """
    Classe base para todos os modelos SQLAlchemy.
    Herda de `DeclarativeBase` para fornecer a funcionalidade de mapeamento objeto-relacional.
    """

    pass


# Cria uma instância do SQLAlchemy, usando a classe Base como a classe base para os modelos
db = SQLAlchemy(model_class=Base)

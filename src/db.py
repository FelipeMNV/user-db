import sqlite3
import click
from flask import current_app, g


def get_db():
    """
    Obtém uma conexão com o banco de dados SQLite.
    Se a conexão ainda não estiver disponível no contexto de aplicação global `g`,
    ela é criada e configurada.

    :return: Conexão com o banco de dados SQLite
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = (
            sqlite3.Row
        )  # Configura a fábrica de linhas para acessar as colunas pelo nome

    return g.db


def close_db(e=None):
    """
    Fecha a conexão com o banco de dados se estiver disponível.
    Remove a conexão do contexto global `g`.

    :param e: Exceção opcional que pode ser passada durante o fechamento
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Inicializa o banco de dados.
    Executa o script `schema.sql` para criar as tabelas e estruturas necessárias.
    """
    db = get_db()

    # Abre e lê o arquivo `schema.sql` para executar o script de criação do banco de dados
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """
    Comando CLI para inicializar o banco de dados.
    Limpa os dados existentes e cria novas tabelas.
    """
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """
    Inicializa o aplicativo Flask com comandos e handlers de banco de dados.

    :param app: Instância da aplicação Flask
    """
    app.teardown_appcontext(
        close_db
    )  # Garante que a conexão com o banco de dados seja fechada ao final da requisição
    app.cli.add_command(
        init_db_command
    )  # Adiciona o comando `init-db` ao CLI da aplicação

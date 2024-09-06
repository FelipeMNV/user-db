import os


class Config:
    """
    Classe base para a configuração da aplicação Flask.
    Define as configurações padrão que podem ser sobrescritas por subclasses.
    """

    TESTING = False  # Define se o modo de teste está ativado
    SECRET_KEY = os.getenv("SECRET_KEY")  # Chave secreta para segurança da aplicação
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )  # URI de conexão com o banco de dados
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Chave secreta para JWT


class ProductionConfig(Config):
    """
    Configurações específicas para o ambiente de produção.
    Herda da classe Config e sobrescreve as configurações padrão.
    """

    TESTING = False  # O modo de teste não está ativado em produção
    SECRET_KEY = "n#$>94JAb;_}@hRMeYLE6"  # Chave secreta para produção
    SQLALCHEMY_DATABASE_URI = "postgresql://felipe:w3ATnTZrE3lRqT2qPxWvCo4yBZDaExEM@dpg-crbdrnjtq21c73chjrjg-a.oregon-postgres.render.com:5432/fbank"  # URI do banco de dados PostgreSQL
    JWT_SECRET_KEY = "Y5n;g[cmCK9Z:.t/s{,yWN"  # Chave secreta para JWT em produção


class DevelopmentConfig(Config):
    """
    Configurações específicas para o ambiente de desenvolvimento.
    Herda da classe Config e sobrescreve as configurações padrão.
    """

    SECRET_KEY = "dev"  # Chave secreta para desenvolvimento
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///fbank.sqlite"  # URI do banco de dados SQLite para desenvolvimento
    )
    JWT_SECRET_KEY = "super-secret"  # Chave secreta para JWT em desenvolvimento
    TESTING = False  # O modo de teste não está ativado em desenvolvimento


class TestingConfig(Config):
    """
    Configurações específicas para o ambiente de teste.
    Herda da classe Config e sobrescreve as configurações padrão.
    """

    SECRET_KEY = "test"  # Chave secreta para teste
    SQLALCHEMY_DATABASE_URI = (
        "sqlite://"  # URI do banco de dados SQLite em memória para testes
    )
    JWT_SECRET_KEY = "test"  # Chave secreta para JWT em testes
    TESTING = True  # O modo de teste está ativado

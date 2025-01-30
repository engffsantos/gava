import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Criar a instância do banco de dados sem associar a nenhum app ainda
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Banco de dados SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões do SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa os modelos dentro do contexto da aplicação
    with app.app_context():
        from app.models import pessoa, produto, doacao, pedido_doacao  # IMPORTANTE: Certifique-se de que esses arquivos existem!
        db.create_all()  # Criar tabelas no SQLite se ainda não existirem

    # Registra as rotas principais
    from app.routes import main, init_routes
    app.register_blueprint(main)
    init_routes(app)

    return app

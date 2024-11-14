from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()  # Adicionando o Migrate aqui

def create_app():
    app = Flask(__name__)

    # Configurações de banco de dados e chave secreta
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gerenciamento.db'
    app.config['SECRET_KEY'] = 'mysecretkey'  # Em produção, use algo mais seguro

    # Inicializando extensões com a aplicação
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Configurando o Flask-Migrate com app e db

    # Configuração do login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import direto para evitar erro de importação
        return User.query.get(int(user_id))

    # Importação e registro de blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app

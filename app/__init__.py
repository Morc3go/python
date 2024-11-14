# Importando as bibliotecas necessárias do Flask e extensões
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Para manipulação do banco de dados
from flask_bcrypt import Bcrypt  # Para criptografia de senhas
from flask_login import LoginManager  # Para gerenciar a autenticação do usuário
from flask_migrate import Migrate  # Para gerenciar as migrações do banco de dados

# Inicializando as extensões
db = SQLAlchemy()  # Objeto para trabalhar com o banco de dados
bcrypt = Bcrypt()  # Objeto para criptografar senhas
login_manager = LoginManager()  # Objeto para gerenciar o login
migrate = Migrate()  # Objeto para gerenciar as migrações

def create_app():
    # Criando a instância da aplicação Flask
    app = Flask(__name__)

    # Configurações do aplicativo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gerenciamento.db'  # Define o URI do banco de dados
    app.config['SECRET_KEY'] = 'mysecretkey'  # Define uma chave secreta para sessões

    # Inicializando as extensões com o aplicativo
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Função que carrega o usuário com base no ID (necessário para o login com Flask-Login)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Importa o modelo de usuário
        return User.query.get(int(user_id))  # Retorna o usuário com o ID correspondente

    # Importando as rotas e registrando o blueprint principal
    from app.routes import main  # Importa as rotas definidas no módulo 'routes'
    app.register_blueprint(main)  # Registra o blueprint de rotas

    # Retorna a aplicação configurada
    return app

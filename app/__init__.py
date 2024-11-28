# Importando as bibliotecas necessárias do Flask e extensões
from flask import Flask  # Flask é a biblioteca principal para criar a aplicação web
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy é utilizado para manipulação do banco de dados
from flask_bcrypt import Bcrypt  # Bcrypt é utilizado para criptografia de senhas
from flask_login import LoginManager  # LoginManager é utilizado para gerenciar a autenticação do usuário
from flask_migrate import Migrate  # Migrate é usado para gerenciar as migrações do banco de dados

# Inicializando as extensões
db = SQLAlchemy()  # Objeto que será usado para interagir com o banco de dados
bcrypt = Bcrypt()  # Objeto para realizar a criptografia de senhas
login_manager = LoginManager()  # Objeto para gerenciar o login do usuário
migrate = Migrate()  # Objeto que auxilia na criação e aplicação das migrações no banco de dados

def create_app():
    # Criando a instância da aplicação Flask
    app = Flask(__name__)  # Instância do Flask, que representa o nosso aplicativo web

    # Configurações do aplicativo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gerenciamento.db'  # Define o URI do banco de dados (no caso, um banco SQLite)
    app.config['SECRET_KEY'] = 'mysecretkey'  # Define uma chave secreta para sessões (necessária para o gerenciamento de cookies de sessão)

    # Inicializando as extensões com o aplicativo
    db.init_app(app)  # Inicializa o banco de dados com o aplicativo
    bcrypt.init_app(app)  # Inicializa o Bcrypt para criptografia de senhas
    login_manager.init_app(app)  # Inicializa o LoginManager para autenticação
    migrate.init_app(app, db)  # Inicializa o Migrate para migrações do banco de dados

    # Função que carrega o usuário com base no ID (necessário para o login com Flask-Login)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Importa o modelo de usuário (necessário para consultar o banco)
        return User.query.get(int(user_id))  # Retorna o usuário correspondente ao ID fornecido

    # Importando as rotas e registrando o blueprint principal
    from app.routes import main  # Importa as rotas definidas no módulo 'routes'
    app.register_blueprint(main)  # Registra o blueprint de rotas para que o Flask saiba como lidar com as requisições

    # Retorna a aplicação configurada para ser executada
    return app

# Importando o módulo datetime para manipulação de datas e horas
from datetime import datetime
# Importando a instância de banco de dados configurada no app
from app import db
# Importando a classe UserMixin do flask_login para integrar com o sistema de login
from flask_login import UserMixin

# Definição do modelo User, que representa um usuário no sistema
class User(db.Model, UserMixin):
    # Definindo as colunas da tabela 'User'
    id = db.Column(db.Integer, primary_key=True)  # ID único do usuário (chave primária)
    username = db.Column(db.String(120), unique=True, nullable=False)  # Nome de usuário (único e obrigatório)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email do usuário (único e obrigatório)
    password = db.Column(db.String(60), nullable=False)  # Senha criptografada (obrigatória)
    is_active = db.Column(db.Boolean, default=True)  # Flag que indica se o usuário está ativo (por padrão, ativo)

    # Relacionamento entre o usuário e as tarefas
    tasks = db.relationship('Task', backref='owner', lazy=True)
    # O relacionamento cria um atributo 'tasks' no objeto User para acessar todas as tarefas associadas a esse usuário.
    # O 'backref' cria um atributo 'owner' no modelo Task que permite acessar o dono da tarefa diretamente.

    # Método especial para representação do objeto (útil para depuração e logs)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Definição do modelo Task, que representa uma tarefa no sistema
class Task(db.Model):
    # Definindo as colunas da tabela 'Task'
    id = db.Column(db.Integer, primary_key=True)  # ID único da tarefa (chave primária)
    title = db.Column(db.String(100), nullable=False)  # Título da tarefa (obrigatório)
    description = db.Column(db.Text, nullable=False)  # Descrição da tarefa (obrigatória)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Data e hora de criação da tarefa (por padrão, data atual)
    status = db.Column(db.String(20), default='Pendente')  # Status da tarefa (por padrão, "Pendente")
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID do dono da tarefa (chave estrangeira)

    # Método especial para representação do objeto (útil para depuração e logs)
    def __repr__(self):
        return f"Task('{self.title}', '{self.date_created}', '{self.status}')"

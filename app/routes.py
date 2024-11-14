# Importando as bibliotecas necessárias para rotas, templates, redirecionamentos e manipulação de formulários
from flask import Blueprint, render_template, url_for, flash, redirect, request
# Importando as instâncias de banco de dados e bcrypt para criptografar senhas
from app import db, bcrypt
# Importando os modelos User e Task do banco de dados
from app.models import User, Task
# Importando os gerenciadores de login
from flask_login import login_user, current_user, logout_user, login_required

# Criando o Blueprint para as rotas principais
main = Blueprint('main', __name__)

# Função auxiliar para validar o formulário de criação de tarefa
def validate_task_form(title, description):
    """Função para validar os campos do formulário da tarefa"""
    if not title or not description:
        flash("Por favor, preencha todos os campos.", "danger")  # Exibe uma mensagem de erro se algum campo estiver vazio
        return False
    return True

# Rota para a página de registro de novos usuários
@main.route('/', methods=['GET', 'POST'])
def register():
    # Se o usuário já estiver autenticado, redireciona para o dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Lógica para processar o formulário de registro (método POST)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validação de campos obrigatórios
        if not username or not password:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for('main.register'))

        # Verifica se o nome de usuário já existe no banco de dados
        if User.query.filter_by(username=username).first():
            flash("Usuário já existe.", "danger")
            return redirect(url_for('main.register'))

        # Criptografa a senha antes de salvar
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)

        # Adiciona o novo usuário ao banco de dados
        db.session.add(user)
        db.session.commit()

        flash("Conta criada com sucesso!", "success")
        return redirect(url_for('main.login'))

    # Renderiza o template de registro
    return render_template('register.html')

# Rota para login de usuários
@main.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver autenticado, redireciona para o dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Lógica para processar o formulário de login (método POST)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validação de campos obrigatórios
        if not username or not password:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for('main.login'))

        # Busca o usuário pelo nome de usuário e valida a senha
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Se a senha for válida, realiza o login do usuário
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Usuário ou senha incorretos.", "danger")

    # Renderiza o template de login
    return render_template('login.html')

# Rota para logout de usuários
@main.route('/logout')
@login_required  # Garante que apenas usuários autenticados possam fazer logout
def logout():
    logout_user()  # Desfaz a autenticação do usuário
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for('main.login'))  # Redireciona para a página de login

# Rota para o dashboard, que exibe as tarefas do usuário logado
@main.route('/dashboard')
@login_required  # Garante que apenas usuários autenticados possam acessar o dashboard
def dashboard():
    tasks = Task.query.filter_by(owner_id=current_user.id).all()  # Recupera todas as tarefas do usuário
    return render_template('dashboard.html', tasks=tasks)  # Renderiza o template do dashboard

# Rota para criação de novas tarefas
@main.route('/task/new', methods=['GET', 'POST'])
@login_required  # Garante que apenas usuários autenticados possam criar tarefas
def new_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        # Valida os campos do formulário de tarefa
        if not validate_task_form(title, description):
            return redirect(url_for('main.new_task'))

        # Cria a nova tarefa e a associa ao usuário logado
        task = Task(title=title, description=description, status="Pendente", owner_id=current_user.id)
        db.session.add(task)
        db.session.commit()

        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for('main.dashboard'))  # Redireciona para o dashboard

    return render_template('task.html', title="Nova Tarefa")  # Renderiza o formulário para nova tarefa

# Rota para editar uma tarefa existente
@main.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required  # Garante que apenas usuários autenticados possam editar tarefas
def update_task(task_id):
    task = Task.query.get_or_404(task_id)  # Busca a tarefa pelo ID ou retorna 404 se não encontrada

    # Verifica se o usuário logado é o proprietário da tarefa
    if task.owner_id != current_user.id:
        flash("Você não tem permissão para editar esta tarefa.", "danger")
        return redirect(url_for('main.dashboard'))  # Redireciona para o dashboard se o usuário não for o proprietário

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')

        # Valida os campos do formulário
        if not validate_task_form(task.title, task.description):
            return redirect(url_for('main.update_task', task_id=task.id))

        try:
            db.session.commit()  # Atualiza a tarefa no banco de dados
            flash("Tarefa atualizada com sucesso!", "success")
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()  # Reverte a transação em caso de erro
            flash(f"Erro ao atualizar a tarefa: {e}", "danger")

    return render_template('task.html', title="Editar Tarefa", task=task)  # Renderiza o formulário para editar a tarefa

# Rota para deletar uma tarefa
@main.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required  # Garante que apenas usuários autenticados possam deletar tarefas
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)  # Busca a tarefa pelo ID ou retorna 404 se não encontrada

    # Verifica se o usuário logado é o proprietário da tarefa
    if task.owner_id != current_user.id:
        flash("Você não tem permissão para deletar esta tarefa.", "danger")
        return redirect(url_for('main.dashboard'))  # Redireciona para o dashboard se o usuário não for o proprietário

    try:
        db.session.delete(task)  # Deleta a tarefa do banco de dados
        db.session.commit()
        flash("Tarefa deletada com sucesso!", "success")
    except Exception as e:
        db.session.rollback()  # Reverte a transação em caso de erro
        flash(f"Erro ao deletar a tarefa: {e}", "danger")

    return redirect(url_for('main.dashboard'))  # Redireciona para o dashboard

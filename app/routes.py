from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)


def validate_task_form(title, description):
    """Função para validar os campos do formulário da tarefa"""
    if not title or not description:
        flash("Por favor, preencha todos os campos.", "danger")
        return False
    return True


@main.route('/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for('main.register'))

        if User.query.filter_by(username=username).first():
            flash("Usuário já existe.", "danger")
            return redirect(url_for('main.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Conta criada com sucesso!", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for('main.login'))

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Usuário ou senha incorretos.", "danger")

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for('main.login'))


@main.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)


@main.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not validate_task_form(title, description):
            return redirect(url_for('main.new_task'))

        task = Task(title=title, description=description, status="Pendente", owner_id=current_user.id)
        db.session.add(task)
        db.session.commit()

        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('task.html', title="Nova Tarefa")


@main.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Verificar se o usuário logado é o proprietário da tarefa
    if task.owner_id != current_user.id:
        flash("Você não tem permissão para editar esta tarefa.", "danger")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')

        if not validate_task_form(task.title, task.description):
            return redirect(url_for('main.update_task', task_id=task.id))

        try:
            db.session.commit()
            flash("Tarefa atualizada com sucesso!", "success")
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar a tarefa: {e}", "danger")

    return render_template('task.html', title="Editar Tarefa", task=task)


@main.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Verificar se o usuário logado é o proprietário da tarefa
    if task.owner_id != current_user.id:
        flash("Você não tem permissão para deletar esta tarefa.", "danger")
        return redirect(url_for('main.dashboard'))

    try:
        db.session.delete(task)
        db.session.commit()
        flash("Tarefa deletada com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao deletar a tarefa: {e}", "danger")

    return redirect(url_for('main.dashboard'))

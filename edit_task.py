from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from main import db
from models import Task

bp = Blueprint('edit_task', __name__)

@bp.route('/task/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.status = request.form.get('status')
        db.session.commit()
        return redirect(url_for('adicionar.dashboard'))
    return render_template('edit_task.html', task=task)

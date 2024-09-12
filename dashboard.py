from flask import Blueprint, render_template
from flask_login import login_required, current_user
from main import db, Task

bp = Blueprint('dashboard', __name__)

@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from adicionar import adicionar_bp

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.secret_key = 'your_secret_key'

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(adicionar_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('E-mail já cadastrado. Por favor, use um e-mail diferente.')
                return redirect(url_for('signup'))
            hashed_password = generate_password_hash(senha, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Conta criada com sucesso! Por favor faça login.')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ocorreu um erro: {e}')
        return render_template('cadastro.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, senha):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Login inválido, tente novamente.')
        return render_template('login.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Você foi desconectado com sucesso.')
        return redirect(url_for('login'))

    return app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

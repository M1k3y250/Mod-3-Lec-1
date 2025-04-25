from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secreto_super_seguro'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Usuarios de ejemplo
users = {
    'admin': {'password': generate_password_hash('admin123'), 'role': 'admin'},
    'user': {'password': generate_password_hash('user123'), 'role': 'user'}
}

# Clase usuario
class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id]['role'])
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and check_password_hash(user['password'], password):
            user_obj = User(username, user['role'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        return 'Credenciales inválidas', 401
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.id, role=current_user.role)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

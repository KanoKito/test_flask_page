from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = (
    'Пожалуйста, войдите для доступа к этой странице.'
)


# Модель пользователя
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash


# "База данных" пользователей
users_db = {
    1: User(1, 'admin', generate_password_hash('password123')),
    2: User(2, 'user', generate_password_hash('123456')),
}


# Поиск пользователя по имени
def get_user_by_username(username):
    for user in users_db.values():
        if user.username == username:
            return user
    return None


# Загрузчик пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('index'))


@app.errorhandler(401)
def unauthorized(error):
    flash('Для доступа к этой странице необходимо авторизоваться', 'error')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

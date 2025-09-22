from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Важно заменить на случайный ключ!

# Простой словарь пользователей (в реальном приложении используйте базу данных)
users = {
    'admin': 'password123',
    'user': '123456'
}

@app.route('/')
def index():
    # Если пользователь уже авторизован, перенаправляем на главную страницу
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован, перенаправляем на главную страницу
    if 'username' in session:
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверяем существование пользователя и правильность пароля
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Неверное имя пользователя или пароль'

    return render_template('login.html', error=error)

@app.route('/home')
def home():
    # Если пользователь не авторизован, перенаправляем на страницу входа
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('home.html', username=session['username'])

@app.route('/logout')
def logout():
    # Удаляем пользователя из сессии
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

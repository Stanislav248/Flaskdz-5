from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_12345'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки.'
login_manager.login_message_category = 'info'

# Імітація бази даних (користувачі зберігаються у пам'яті до перезапуску сервера)
users = {}

class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = str(len(users) + 1)
        new_user = User(user_id, form.username.data, form.email.data, form.password.data)
        users[user_id] = new_user
        
        flash('Акаунт успішно створено! Тепер ви можете увійти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Реєстрація', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = next((u for u in users.values() if u.email == form.email.data), None)
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Помилка входу. Перевірте Email та пароль.', 'danger')
    return render_template('login.html', title='Вхід', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return f'<h1>Вітаємо, {current_user.username}! Це ваш особистий кабінет.</h1><a href="{url_for("logout")}">Вийти з акаунту</a>'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

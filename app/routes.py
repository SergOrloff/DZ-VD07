from flask import render_template, url_for, redirect, flash, request, make_response, Blueprint, send_file, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm, UpdateProfileForm
import io
from io import BytesIO

main = Blueprint('main', __name__)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.user_image.data = current_user.user_image
    if form.validate_on_submit():  # убрано elif
        print("Форма прошла валидацию")  # Отладка: форма прошла валидацию
        print(f"Новое имя пользователя: {form.username.data}")
        print(f"Новый email: {form.email.data}")
        print(f"Новое изображение: {form.user_image.data}")
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.user_image.data:
            # Чтение данных изображения
            image_data = form.user_image.data.read()
            # Обновление изображения пользователя
            current_user.user_image = image_data
        if form.password.data:
            current_user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Ваш профиль был обновлен!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('main.welcome'))
        else:
            flash('Ошибка входа. Пожалуйста, проверьте email и пароль.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Убедитесь, что файл действительно загружен
        if 'user_image' not in request.files:
            # Обработка случая, когда файл не загружен
            return "Файл не загружен", 400
        user_image = request.files['user_image']
        # Убедитесь, что файл был выбран
        if user_image.filename == '':
            # Обработка случая, когда файл не выбран
            return "Файл не выбран", 400

            # Прочитайте данные файла как байты
        file_data = user_image.read()
        user_image.seek(0)

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, user_image=file_data)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт создан! Теперь вы можете войти в систему.', 'success')
        login_user(user)
        return redirect(url_for('main.welcome'))
    return render_template('register.html', form=form)

def get_user_image(user_id):
    # Пример для SQLAlchemy
    user = User.query.get(user_id)
    if user and user.image_data:
        return user.image_data
    return None

@main.route('/user_image/<int:user_id>')
def user_image(user_id):
    user = User.query.get(user_id)
    if user and user.user_image:
        # Создаем объект BytesIO из бинарных данных
        image_data = BytesIO(user.user_image)
        # Возвращаем изображение как файл
        return send_file(image_data, mimetype='image/jpeg')  # Убедитесь, что mimetype соответствует типу изображения
    else:
        abort(404)  # Если пользователь или изображение не найдено, возвращаем 404

@main.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@main.route('/')
def home():
    return redirect(url_for('main.login'))

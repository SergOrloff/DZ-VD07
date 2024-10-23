from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin

# Создаем Flask приложение
app = Flask(__name__)

# Настройки приложения
app.config['SECRET_KEY'] = 'your_secret_key'  # Ключ для сессий и флеш-сообщений
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # База данных SQLite

# Инициализация базы данных
db = SQLAlchemy(app)

# Замените ниже строку подключения на вашу
engine = create_engine('sqlite:///instance/site.db')
# engine = create_engine('postgresql+psycopg2://username:password@localhost/mydatabase')

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Отражаем таблицу User
metadata = MetaData()
user_table = Table('User', metadata, autoload_with=engine)

# Выполняем запрос для получения всех записей из таблицы User
with engine.connect() as connection:
    result = connection.execute(user_table.select())
    users = result.fetchall()

# Выводим данные
for user in users:
    print(user)

# Определение модели пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_image = db.Column(db.LargeBinary, nullable=True)  # Поле для хранения изображений

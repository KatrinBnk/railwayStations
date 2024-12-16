from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db import db
import os
from populate_db import populate_all

# Путь к базе данных
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'railway.db')

# URL для подключения к SQLite базе данных
DATABASE_URL = f"sqlite:///{db_path}"

# Создаём подключение к базе данных напрямую
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Проверка, существует ли база данных
if not os.path.exists(db_path):
    # Создаём все таблицы
    db.metadata.create_all(engine)
    print("База данных и таблицы созданы.")

    # Вызов функции для заполнения данных
    populate_all(session)
    print("Данные успешно добавлены в базу данных.")
else:
    print("База данных уже существует.")

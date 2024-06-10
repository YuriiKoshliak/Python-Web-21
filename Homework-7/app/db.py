from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db_models import Base

# Функція для створення підключення до бази даних
def db_connect():
    # Створення з'єднання з базою даних PostgreSQL
    engine = create_engine('postgresql://postgres:1234@localhost:5432/postgres')
    return engine

# Функція для створення таблиць в базі даних
def create_tables(engine):
    # Створення всіх таблиць, визначених у моделях
    Base.metadata.create_all(engine)

# Функція для створення сесії
def create_session(engine):
    # Створення і повернення нової сесії для взаємодії з базою даних
    Session = sessionmaker(bind=engine)
    return Session()

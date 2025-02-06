import datetime

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, text


DB_ENGINE = 'postgresql'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'mineshop7_1'

# Строка подключения к базе данных
CONNECTION_STRING = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# Base = declarative_base()
# Создание движка
engine = create_engine(CONNECTION_STRING)
# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def select(table_name, keys, conditions):

    keys_string = ', '.join(keys)
    conditions_string = ' AND '.join(conditions)
    if conditions_string:
        conditions_string = 'WHERE ' + conditions_string
    execution_string = f"SELECT {keys_string} FROM {table_name} {conditions_string}"

    with Session() as session:
        rows = session.execute(text(execution_string))
        return rows.fetchall()

def insert(table_name, mapping):
    keys_string = ', '.join(mapping.keys())
    values_string = ', '.join(mapping. values())
    execution_string = f"INSERT INTO {table_name} ({keys_string}) VALUES ({values_string})"

    with Session() as session:
        session.execute(text(execution_string))
        session.commit()
        return True


if __name__ == "__main__":

    result = insert(
        'posts_post',
        {
            'name': "'Domovoi'",
            'review': "'Я один тут остался?'",
            'product_id': '2',
            'user_id': '9',
            'time_published': f"'{datetime.datetime.now()}'"
        }
    )

from datetime import datetime
import sqlalchemy as sqla

from pydantic import BaseModel, Field, ConfigDict, ValidationError
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, select
from typing_extensions import Annotated, Optional

DB_ENGINE = 'postgresql'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'mineshop7_1'

# Строка подключения к базе данных
CONNECTION_STRING = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(CONNECTION_STRING, echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


Base.metadata.create_all(bind=engine)


class PostORM(Base):
    __tablename__ = 'posts_post'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    review = Column(String)
    time_published = Column(DateTime(timezone=True))
    product_id = Column(Integer)
    user_id = Column(Integer)


class PostPydantic(BaseModel):
    id: Annotated[Optional[int], Field(default=None)]
    name: Annotated[str, Field(min_length=2, max_length=75)]
    review: Annotated[str, Field(min_length=2, max_length=500)]
    time_published: Annotated[datetime, Field()]
    product_id: Annotated[Optional[int], Field(default=None)]
    user_id: Annotated[int, Field(gt=0)]

    model_config = ConfigDict(from_attributes=True)


# def select(table_name, keys, conditions):
#
#     keys_string = ', '.join(keys)
#     conditions_string = ' AND '.join(conditions)
#     if conditions_string:
#         conditions_string = 'WHERE ' + conditions_string
#     execution_string = f"SELECT {keys_string} FROM {table_name} {conditions_string}"
#
#     with Session() as session:
#         rows = session.execute(text(execution_string))
#         return rows.fetchall()

# def insert(table_name, mapping):
#     keys_string = ', '.join(mapping.keys())
#     values_string = ', '.join(mapping. values())
#     execution_string = f"INSERT INTO {table_name} ({keys_string}) VALUES ({values_string})"
#
#     with Session() as session:
#         session.execute(text(execution_string))
#         session.commit()
#         return True


def get_posts_by_user_gt(user_id=None):
    if not user_id:
        return []
    with Session() as session:
        stmt = sqla.select(PostORM).where(PostORM.user_id > user_id)
        posts = session.execute(stmt).scalars().all()
        #posts = session.execute(stmt).fetchall()

    result = []
    if posts:
        for post in posts:
            post_pydantic = PostPydantic.model_validate(post)
            result.append(post_pydantic.model_dump())
    return result


def create_new_post(mapping):
    try:
        post_pydantic = PostPydantic.model_validate(mapping)
    except ValidationError as error:
        return str(error)

    new_post = PostORM(
        name=post_pydantic.name,
        review=post_pydantic.review,
        user_id=post_pydantic.user_id,
        product_id=post_pydantic.product_id,
        time_published=post_pydantic.time_published
    )

    new_post = add_data_to_db(new_post)

    return new_post.id


def add_data_to_db(orm_object):
    with Session() as session:
        session.add(orm_object)
        session.commit()
        session.refresh(orm_object)
    return orm_object



if __name__ == "__main__":

    print(create_new_post({
        # 'id': None,
        'name': 'Stepan Razin',
        'review': 'Не по Сеньке шапка',
        'user_id': 9,
        'product_id': 10,
        'time_published': datetime.now(),
    }))


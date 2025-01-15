from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, create_engine, DateTime, select
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, ConfigDict, Field

from sqlalchemy import create_engine
from typing_extensions import Annotated

DB_ENGINE = 'postgresql'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'mineshop7_1'

# Строка подключения к базе данных
CONNECTION_STRING = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


Base = declarative_base()
# Создание движка
engine = create_engine(CONNECTION_STRING)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class PostORM(Base):
    __tablename__ = "posts_post"
    id = Column(Integer, primary_key=True, autoincrement=True)
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


def get_post_by_user(user_id: int):
    with Session() as session:
        stmt = select(PostORM).filter_by(user_id=user_id)
        posts = session.execute(stmt).fetchall()

    result = []
    if posts:
        for post in posts:
            post_pydantic = PostPydantic.model_validate(post[0])
            result.append(post_pydantic.model_dump())
    return result


def get_post_by_id(id: int):
    with Session() as session:
        stmt = select(PostORM).filter_by(id=id)
        post = session.execute(stmt).scalar_one_or_none()

    if post:
        post_pydantic = PostPydantic.model_validate(post)
        return post_pydantic
    return None


def create_post(**data):

    post_pydantic = PostPydantic.model_validate(data)

    new_post = PostORM(
        name=post_pydantic.name,
        review=post_pydantic.review,
        time_published=post_pydantic.time_published,
        product_id=post_pydantic.product_id,
        user_id=post_pydantic.user_id
    )

    new_post = add_data_to_db(new_post)

    return new_post.id


def add_data_to_db(data_object):

    with Session() as session:
        session.add(data_object)
        session.commit()
        session.refresh(data_object)
    return data_object



if __name__ == "__main__":

    post_data = get_post_by_user(2)
    [print(post) for post in post_data]

    data = {
        'id': None,
        'name': 'Incognito',
        'review': 'А я сейчас как напишу здесь плохо :)',
        'time_published': datetime.now(),
        'product_id': None,
        'user_id': 9
    }

    #print(create_post(**data))

    posts = [print(i, get_post_by_id(i)) for i in range(100)]

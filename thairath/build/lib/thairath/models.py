from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
import pymysql
import os

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    pymysql.install_as_MySQLdb()
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")
    return create_engine((os.getenv("DATABASE_URL")))
    # CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}".format(
    #     # drivername="mysql",
    #     # user="user",
    #     # passwd="password",
    #     # host="localhost",
    #     # port="8080",
    #     # db_name="db",
    #     drivername="postgresql",
    #     user="nngpbmduikrokz",
    #     passwd="e50806caab773da9d1324ef81d8fc0e76b0ee6db2b6206d3525c3b55b54e65ab",
    #     host="ec2-54-86-170-8.compute-1.amazonaws.com",
    #     port="5432",
    #     db_name="d2se5r33ul7mim",
    # )

    # return create_engine(CONNECTION_STRING, client_encoding='utf8')


def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for Many-to-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
quote_tag = Table('news_tag', Base.metadata,
    Column('news_id', Integer, ForeignKey('news.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    news_topic = Column('news_topic', Text())
    news_content = Column('news_content', Text())
    date = Column('date',Text())
    author = Column('author',Text())
    url = Column('url', Text())
    tags = relationship('Tag', secondary='news_tag',
        lazy='dynamic', backref="news")  # M-to-M for quote and tag

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column('name', Text(), unique=True)
    quotes = relationship('News', secondary='news_tag',
        lazy='dynamic', backref="tag")  # M-to-M for quote and tag
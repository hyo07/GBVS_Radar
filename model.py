from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TEXT, DATETIME, ForeignKey
import sys
from get_env import get_env
import os

username = os.getlogin()

if username == "ec2-user":
    # mysqlのDBの設定
    DATABASE = 'mysql+mysqldb://{user_name}:{password}@{ip}/{db_name}?charset=utf8mb4'.format(
        user_name=get_env("MYSQL_USER"),
        password=get_env("MYSQL_PASS"),
        ip="localhost",
        db_name=get_env("DB_NAME"),
    )
    ENGINE = create_engine(
        DATABASE,
        encoding="utf-8",
        echo=False
    )
else:
    # sqliteの設定
    dir_name = os.path.dirname(__file__)
    sqlite_path = dir_name + "/test.sqlite3"
    ENGINE = create_engine('sqlite:///{}'.format(sqlite_path))

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

Base = declarative_base()
Base.query = session.query_property()


class Tweet(Base):
    __tablename__ = "tweets"

    tweet_id = Column('tweet_id', String(255), primary_key=True)
    twitter_id = Column('twitter_id', String(255), nullable=False)
    twitter_name = Column('twitter_name', String(255), nullable=False)
    tweeted_at = Column('tweeted_at', DateTime, nullable=False)
    rank_tier = Column('rank_tier', String(255))
    player_name = Column('player_name', String(255), nullable=False)
    character = Column('character', String(255), nullable=False)
    rank = Column('rank', String(255), nullable=False)
    vsid = Column('vsid', String(255), nullable=False)
    comment = Column('comment', String(255))

    # @staticmethod
    # def add_column(engine, column):
    #     column_name = column.compile(dialect=engine.dialect)
    #     column_type = column.type.compile(engine.dialect)
    #     engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (Channel.__tablename__, column_name, column_type))


def main(args):
    Base.metadata.create_all(bind=ENGINE)

    # ba_pass = Column('ba_pass', String(255), unique=False, nullable=True)
    # Channel.add_column(ENGINE, ba_pass)


if __name__ == "__main__":
    main(sys.argv)

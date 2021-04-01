import os

from databases import Database
from sqlalchemy import MetaData, create_engine


def get_variable(name: str) -> str:
    path = os.getenv(name)
    with open(path, 'r') as f:
        return f.readline().rstrip('\n')


DATABASE_URI = get_variable('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

database = Database(DATABASE_URI)

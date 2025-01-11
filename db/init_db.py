from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.db_tables import Base

engine = create_engine('sqlite:///database.db')

def init_db():
    Base.metadata.create_all(engine)
    print("Baza danych i tabele zostały utworzone.")

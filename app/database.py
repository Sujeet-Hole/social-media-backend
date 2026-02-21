from sqlalchemy import  create_engine
from sqlalchemy.orm import session , sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

DATABASE_URl = os.getenv("DATABASE_URl")

engine = create_engine(DATABASE_URl)

sessionlocal = sessionmaker(autocommit = False , autoflush=False , bind = engine)

Base = declarative_base()

def get_db ():
    db = sessionlocal()
    try:
        yield db

    finally :
        db.close()


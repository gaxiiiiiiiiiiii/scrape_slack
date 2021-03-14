from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.environ['DATABASE_URL']
engine=create_engine(DATABASE_URL)
SessionClass=sessionmaker(engine)
session=SessionClass()
Base=declarative_base(bind=engine)

class Cache(Base):
    __tablename__="cache" 
    __table_args__={"autoload": True}
    
    
def mkDiff(data):
    session = SessionClass()
    cache = session.query(Cache).all()
    session.close()
    cache = [(d.title, d.price, d.url) for d in cache]
    diff = list(set(data) - set(cache))
    return diff


def updateCache(data):
    session = SessionClass()
    cache = session.query(Cache).all()
    for c in cache:
        session.delete(c)
    for d in data:
        title, price, url = d
        c = Cache(title=title, price=price, url=url)
        session.add(c)
    session.commit()
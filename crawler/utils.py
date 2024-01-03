# utils.py
from sqlalchemy import create_engine, Column, String, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class CrawledData(Base):
    __tablename__ = 'crawled_data'
    id = Column(String, primary_key=True)
    url = Column(String)
    content = Column(Text)

def save_to_database(url, content):
    database_uri = os.getenv('DATABASE_URI')
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    data = CrawledData(url=url, content=content)
    session.add(data)
    session.commit()
    session.close()

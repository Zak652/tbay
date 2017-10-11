from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://zak:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

class Item(Base):
	__tablename__ = "items"

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	description = Column (String)
	start_time = Column(DateTime, default = datetime.utcnow)

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	user_name = Column(String, nullable = False)
	password = Column(String, nullable = False)

class Bid(Base):
	__tablename__ = "bids"

	id = Column(Integer, primary_key = True)
	price = Column(Integer, nullable = False)

	
Base.metadata.create_all(engine)
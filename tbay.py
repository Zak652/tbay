from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


engine = create_engine('postgresql://zak:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	user_name = Column(String, nullable = False)
	password = Column(String, nullable = False)

	items_owned = relationship("Item", backref = "users")
	bids_placed = relationship("Bid", backref = "users")


class Item(Base):
	__tablename__ = "items"

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	description = Column (String)
	start_time = Column(DateTime, default = datetime.utcnow)

	owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)

	item_bids = relationship("Bid", backref = "items")

class Bid(Base):
	__tablename__ = "bids"

	id = Column(Integer, primary_key = True)
	price = Column(Integer, nullable = False)

	bid_owner = Column(Integer, ForeignKey("users.id"), nullable = False)
	item_bidded = Column(Integer, ForeignKey("items.id"), nullable = False)

	
Base.metadata.create_all(engine)
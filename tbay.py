from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import getpass


engine = create_engine('postgresql://zak:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	username = Column(String, nullable = False)
	password = Column(String, nullable = False)

	owner = relationship("Item", backref = "owner")
	bidder = relationship("Bid", backref = "bidder")


class Item(Base):
	__tablename__ = "items"

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	description = Column (String)
	start_time = Column(DateTime, default = datetime.utcnow)

	item_owner = Column(Integer, ForeignKey("users.id"), nullable = False)

	item_bids = relationship("Bid", backref = "items")

class Bid(Base):
	__tablename__ = "bids"

	id = Column(Integer, primary_key = True)
	price = Column(Integer, nullable = False)

	bid_owner = Column(Integer, ForeignKey("users.id"), nullable = False)
	item_id = Column(Integer, ForeignKey("items.id"), nullable = False)

	
Base.metadata.create_all(engine)

def register_user():
	#Collect user's name and password
	newuser = None
	print("Please provide details for a new user")
	username = input("Username: ")
	password = input("Password: ")

	#Check if username already exists
	if username and password is not None:
		newuser = session.query(User).filter(User.username == username).first()

		if newuser == None:
			newuser = User(username = username, password = password)
			session.add(newuser)
			session.commit()
		else:
			print("User %s already exists.", (username))

def login():
	""" Login facility for registered users """
	global logged_in
	username = input("Username: ")
	# password = input("Password: ")
	password = getpass.getpass("Password: ")

	user = session.query(User).filter(User.username == username, User.password == password).first()
	if user == None:
		print("User is not registered, please register.")

	logged_in = user

	return user

def add_item():
	""" Facilitates adding items for auctioning """
	print("Please provide item name and description.")
	new_item = None
	add_more = None
	user = logged_in
	item_name = input("Item name: ")
	item_dscr = input("Item description: ")

	if item_name and item_dscr is not None:
		new_item = Item(name = item_name, description = item_dscr, item_owner = logged_in.id)
		session.add(new_item)
		session.commit()
		added = session.query(Item).filter(Item.description == item_dscr).first()
		print("{!r}, {!r} has been added.".format(added.name, added.description))

def biddable_items():
	""" Print out information of auctioned items """
	items_list = session.query(Item).all()

	for item in items_list:
		print(item.id, item.name, item.description)
		# print(vars(item))

def place_bid():
	""" Facilitates placing a bid for auctioned items """
	print("Enter an item number from the list below and provide you're bidding amount.")
	print(biddable_items())
	new_bid = None

	item_no = int(input("Item number: "))
	bid_amount = int(input("Bid amount: "))
	new_bid = Bid(item_id = item_no, price = bid_amount, bid_owner = logged_in.id)
	session.add(new_bid)
	session.commit()
	print("You've placed of ${!r} on item number: {!r}.".format(bid_amount, item_no))

def highest_bidder():
	""" Provides information about the highest bidder or bidders if the bid amount is the same """
	item = int(input("Check bids relating to item number: "))
	# highest_bid = session.query(func.max(Bid.price)).filter(Bid.item_id == item).all()
	highest_bid = session.query(desc(Bid.price)).filter(Bid.item_id == item).first()
	# highest_bid = session.query(func.max(Bid.price)).filter(Bid.item_id == item).order_by("id")
	print ("{!r} has the highest bid of USD {!r}".format(highest_bid, highest_bid))
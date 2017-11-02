from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from tbay import register_user, login, add_item, place_bid, highest_bidder, biddable_items


def main():
	user = None
	option = input("To Login press 'L', For registration press 'R': ")

	if option in ['L', 'l']:
		#User login
		while user is None:
			user = login()

			while True:
				#select activity after logging in
				activity = input("Enter 'A' To add new item, 'B' To place a bid, 'H' To view highest bid,"
								" 'X' To logout: ")
				#Load new items for auctioning
				if activity in ['A', 'a', 'add']:
					items_to_add = int(input("How many items would you like to add? "))

					for item in range(items_to_add):
						add_item()
					print("Total number of items added: {} \n".format(items_to_add))
					print("Please select a new activity")

				#Place bid on auctioned items
				elif activity in ['B', 'b', 'bid']:
					items_to_bid = int(input("How many bids will you place? "))

					for bid in range(items_to_bid):
						place_bid()
					print("Total number of bids processed: {}".format(items_to_bid))

				#View highest bid
				elif activity in ['H', 'h', 'view']:
					print(biddable_items(),'\n')
					print(highest_bidder(),'\n')
					print("Please select a new activity")

				#Logout
				elif activity in ['X', 'x', 'logout']:
					break

	#Register a new user
	elif option in ['R', 'r']:
		users_to_add = int(input("How many users are you registering? "))

		for item in range(users_to_add):
			register_user()

if __name__ == '__main__':
	main()
from abc import ABC

# the player interface that will be implemented by player class and player proxy class
class PlayerInterface(ABC):
	# the inital placement function which will ask each player
	# to place the very first tile and position his or her avatar on the board
	def initial_placement(self, gameboard, tiles, avatar):
		pass

	# the intermediate placement funtion which asks
	# player to place a tile during the game next to his or her avatar's port
	def placement(self, gameboard, tiles, avatar):
		pass

	# getter
	def get_name(self):
		pass
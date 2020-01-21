import sys

sys.path.insert(0, '../Common')

from tiles import Tile
from avatar import Avatar
from board import Board
from rules import Rule
from player_interface import PlayerInterface

# Player component which represents each individual player and how they make decisions
# regarding to game moves.
class Player(PlayerInterface):
	def __init__(self, name, strategy):
		self.strategy = strategy
		self.rule_checker = Rule()
		self.name = name

	# select the first available position on the board with the first available tile
	# by rotating it. Support two strategies now
	def initial_placement(self, gameboard_dict, tiles_dict, avatar_dict):
		'''
		:param gameboard_dict: the initial blank gameboard
		:param tiles_dict: The 3 initial given tiles for the player
		:param avatar_dict: The player's avatar
		:return: the first possible chosen tile which can be placed on the board based on the player's strategy with associated avatar
				second: try all the 3 tiles with rotation at the edge of the board (36 grids)
				dumb: only try the first tile at the edge of the board (36 grids), if it does not work, choose the third one directly
		'''
		gameboard, tiles, avatar = construct_obj(gameboard_dict, tiles_dict, avatar_dict)
		ports = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
		if self.strategy == 'second':
			for tile in tiles:
				board = gameboard.get_board()
				for i in range(36):
					x, y = get_xy(i)
					tile.updatePos(x, y)
					for _ in range(4):
						for port in ports:
							avatar.update_position((x, y), port)
							if self.rule_checker.check_initial_placement(gameboard, avatar, tile, tiles):
								return tile, avatar
						tile.rotate(90)

		if self.strategy == 'dumb':
			board = gameboard.get_board()
			tile = tiles[0]
			for i in range(36):
				x, y = get_xy(i)
				tile.updatePos(x, y)
				for port in ports:
					avatar.update_position((x, y), port)
					if self.rule_checker.check_initial_placement(gameboard, avatar, tile, tiles):
						return tile, avatar

		return tiles[2], avatar

	# how to choose later placements. Either 'dumb' or 'second' strategy
	def placement(self, gameboard_dict, tiles_dict, avatar_dict):
		'''
		:param gameboard_dict: the current running gameboard
		:param tiles_dict: the 2 given tiles for the player at this round
		:param avatar_dict: the avatar associated with this player
		:return:the first possible chosen tile which can be placed on the board based on the player's strategy with associated avatar
			    second: try all the 3 tiles with rotation
				dumb: only try the second tile, if it does not work, choose the first one directly
		'''
		gameboard, tiles, avatar = construct_obj(gameboard_dict, tiles_dict, avatar_dict);
		if self.strategy == 'dumb':
			tile = tiles[1]
			pos = avatar.get_new_pos()
			tile.updatePos(pos[0], pos[1])
			return tile, avatar

		if self.strategy == 'second':
			for t in tiles:
				pos = avatar.get_new_pos()
				t.updatePos(pos[0], pos[1])
			for i in range(0, 2):
				idx = len(tiles) - i
				tile = tiles[idx - 1]
				for _ in range(4):
					if self.rule_checker.check_placement(gameboard, avatar, tile, tiles):
						return tile, avatar
					tile.rotate(90)

		return tiles[0], avatar

	# get name
	def get_name(self):
		'''
		:return: the name of this player
		'''
		return self.name

	# render result to player, later will be shown as an image on the board
	def render_result(self, result):
		'''
		:param result: the game result of the player - win/lose
		:return: print the result
		'''
		print("You " + str(result) + "!")

# get the border x and y value by a single number.
def get_xy(num):
	'''
	:param num: the number of the 36 edge grids on the initial board
	:return: the x,y value accroding to the grid number
	'''
	if int(num / 9) == 0:
		return num % 9, 0
	if int(num / 9) == 1:
		return 9, num % 9
	if int(num / 9) == 2:
		return 9 - num % 9, 9
	if int(num / 9) == 3:
		return 0, 9 - num % 9

# construct objects from serializable lists
def construct_obj(board_dict, tiles_dict, avatar_dict):
	'''
	:param board_dict: dict containing board obj info
	:param tiles_dict: dict containing tiles obj info
	:param avatar_dict: dict containing avatar obj info
	:return: constructed board, tiles, avatar objects
	'''
	board = Board([], [])
	board.board = board_dict['board']
	for tiles in board_dict['board']:
		for t in tiles:
			if not t == None:
				pos = t['position']
				board.board[pos[1]][pos[0]] = construct_tile(t)

	for t in board_dict['tiles']:
		board.tiles.append(construct_tile(t))

	for a in board_dict['avatars']:
		board.avatars.append(construct_avatar(a))

	tiles = []
	for t in tiles_dict:
		tiles.append(construct_tile(t))

	avatar = construct_avatar(avatar_dict)
	for a in board.avatars:
		if a.color == avatar_dict['color']:
			avatar = a

	return board, tiles, avatar

# construct tile from list of attributes
def construct_tile(tile_dict):
	'''
	:param tile_dict: dict containing tile obj
	:return: constructed tile obj
	'''
	tile = Tile(tile_dict['idx'], None)
	if not tile_dict['position'] == None:
		tile.position = (tile_dict['position'][0], tile_dict['position'][1])
	tile.list_of_path = tile_dict['list_of_path']

	return tile

# construct avatar from list of attributes
def construct_avatar(avatar_dict):
	'''
	:param avatar_dict:	dict containing avatar obj info
	:return: constructed avatar obj
	'''
	avatar = Avatar(avatar_dict['color'], None)
	if not avatar_dict['position'] == None:
		pos = avatar_dict['position'][0]
		port = avatar_dict['position'][1]
		avatar.position = ((pos[0], pos[1]), port)

	return avatar

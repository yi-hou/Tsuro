from tiles import Tile
from avatar import Avatar

# the board class which represents the board in the Tsuro game
class Board:
	# constructor
	'''
		@param: list_of_tiles	list of tiles
				list_of_avatars	list of avatars
		@return: none
	'''
	def __init__(self, list_of_tiles, list_of_avatars):
		self.board = []
		self.avatars = list_of_avatars
		self.tiles = list_of_tiles
		for i in range(10):
			temp_list = []
			for j in range(10):
				temp_list.append(None)
			self.board.append(temp_list)

		valid_tiles = []
		# Check if the tiles are all on the edge of the board
		all_on_border(list_of_tiles, valid_tiles)

		# Check if the tile contains avatars in the list_of_avatars and the avatar
		# is placed on a port facing interior of the board
		valid_avatar_pos(valid_tiles, list_of_avatars)

		# There are no tiles neighboring other tiles
		check_neighbor_tiles(valid_tiles)

		# Saving all the valid tiles to board
		for vt in valid_tiles:
			pos = vt.get_position()
			self.board[pos[1]][pos[0]] = vt

		# update all avatars' port
		for a in self.avatars:
			a_tile = a.get_position()[0]
			a_port = a.get_position()[1]
			path_map = get_tile_path_map(a_tile, self.board)
			if not path_map == None:
				a_port = path_map[a_port]
				a.update_position(a_tile, a_port)

	# Initial placement of a tile and an avatar. In the method we call the contructor
	# one more time and assign the current board to the new board to use all the condition
	# checks in the init method
	def initial_placement(self, tile, avatar):
		'''
			@param: tile 	the tile to be placed
					avatar 	the avatar to be placed
			@return: none
		'''
		# try:
		# print(len(self.avatars))
		# find the entry port of each avatar
		for i in range(len(self.avatars)):
			# print("port_before: ", self.avatars[i].get_position()[1])
			port = self.tiles[i].find_exit(self.avatars[i].get_position()[1])
			# print("port: ", port)
			self.avatars[i].update_port(port)
		self.tiles.append(tile)
		self.avatars.append(avatar)
		list_tiles = self.tiles.copy()
		list_avatars = self.avatars.copy()
		new_board = Board(list_tiles, list_avatars)
		self.board = new_board.get_board()
		self.avatars = new_board.get_avatars()
		self.tiles = new_board.get_tiles()

	# Add a tile on to the board
	def add_tile(self, tile, avatar):
		'''
			@param: tile 	the tile to be placed
					avatar 	the avatar to be placed
			@return: none
		'''
		if not avatar in self.avatars:
			raise Exception('The avatar representing the given player does not exist')
		if not physical_condition(tile.get_position(), self.board):
			raise Exception('The tile placement is physically impossible on the board')
		a_pos = avatar.get_position()
		pos = tile.get_position()
		if not pos == new_pos(a_pos[0], a_pos[1], self.board):
			raise Exception('The tile needs to be placed next to avatar')
		self.board[pos[1]][pos[0]] = tile
		self.tiles.append(tile)
		self.update_avatars()

	# Go through list of avatars and update each avatars position
	# by moving it along the path untilt it can not be moved anymore
	def update_avatars(self):
		'''
			@param: none
			@return: none
		'''
		new_avatars = []
		for a in self.avatars:
			a_tile = a.get_position()[0]
			a_port = a.get_position()[1]
			while True:
				tile_port = connected_tile(a_tile, a_port, self.board)
				if tile_port == None:
					break
				a_tile, a_port = tile_port
				path_map = get_tile_path_map(a_tile, self.board)
				if not path_map == {}:
					a_port = path_map[a_port]
			a.update_position(a_tile, a_port)
			new_avatars.append(a)
		self.avatars = new_avatars

	# delete an avatar from the board.
	def del_avatar(self, avatar):
		'''
			@param: avatar 	the avatar to be deleted
			@return: none
		'''
		for a in self.avatars:
			if a.get_color() == avatar.get_color():
				self.avatars.remove(a)

	def del_tile(self, pos):
		'''
			@param: pos 	the position of tile to be deleted
			@return: none
		'''
		self.board[pos[1]][pos[0]] = None
		self.tiles = self.tiles[:-1]

	# getter methods
	def get_avatars(self):
		'''
			@param: none
			@return: the list of avatars
		'''
		return self.avatars

	def get_board(self):
		'''
			@param: none
			@return: the board of the board
		'''
		return self.board

	def get_tiles(self):
		'''
			@param: none
			@return: the list of tiles of board
		'''
		return self.tiles



# Check if the tile contains avatars in the list_of_avatars and the avatar
# is placed on a port facing interior of the board
def valid_avatar_pos(valid_tiles, list_of_avatars):
	'''
		@param: valid_tiles 	all the valid tiles to be checked
				list_of_avatars	the list of avatars
		@return: none
	'''
	for tile in valid_tiles:
			contains_avatar = False
			path = tile.get_list_of_path()
			path_map = {}
			for p in path:
				path_map[p[0]] = p[1]
				path_map[p[1]] = p[0]
			for a in list_of_avatars:
				a_pos = a.get_position()
				t_pos = tile.get_position()
				if tile.get_position() == a_pos[0]:
					contains_avatar = True
					exit_port = path_map[a_pos[1]]
					a_port = a_pos[1]
					if not check_border(t_pos, exit_port, a_port):
						raise Exception('Avatars are not placed on the correct port')
			if not contains_avatar:
				raise Exception('Some tiles does not contains avatar')

# There are no tiles neighboring other tiles
def check_neighbor_tiles(valid_tiles):
	'''
		@param: valid_tiles 	all the valid tiles to be checked
		@return: none
	'''
	for i1 in range(len(valid_tiles)):
		i2 = i1 + 1
		pos1 = valid_tiles[i1].get_position()
		while i2 < len(valid_tiles):
			pos2 = valid_tiles[i2].get_position()
			if (pos1[0] == pos2[0] and (pos1[1] == pos2[1] - 1 or pos1[1] == pos2[1] + 1)) \
					or (pos1[1] == pos2[1] and (pos1[0] == pos2[0] - 1 or pos1[0] == pos2[0] + 1)):
				raise Exception('Tiles can not be next to each other')
			i2 = i2 + 1

# Check if the tiles are all on the edge of the board
def all_on_border(list_of_tiles, valid_tiles):
	'''
		@param: list_of_tiles 	list of tiles to be checked
				valid_tiles 	list of valid tiles to be checked
		@return: none
	'''
	for tile in list_of_tiles:
		pos = tile.get_position()
		if pos[0] > 9 or pos[0] < 0 or pos[1] > 9 or pos[1] < 0:
			raise Exception('The position of tile is out of the board')
		if pos[0] == 0 or pos[0] == 9 or pos[1] == 0 or pos[1] == 9:
			dups = False
			for t in valid_tiles:
				if t.get_position == pos:
					dups = True
			if not dups:
				valid_tiles.append(tile)
			else:
				raise Exception('There are duplicate tile in the edge')
		else:
			raise Exception('Tile are not on the edge of the board')

# check if the given initial placement's avatar is valid
# meaning it will not exit on the first run and is placed
# on the side of the board
def check_border(t_pos, exit_port, a_port):
	'''
		@param: t_pos 		the position of tile
				exit_port	the exit port of the avatar
				a_port		the port of avatar
		@return: boolean indicating if it is valid
	'''
	if (t_pos[1] == 0 and (exit_port == 'A' or exit_port == 'B')) \
	or (t_pos[1] == 9 and (exit_port == 'E' or exit_port == 'F')) \
	or (t_pos[0] == 0 and (exit_port == 'H' or exit_port == 'G')) \
	or (t_pos[0] == 9 and (exit_port == 'C' or exit_port == 'D')):
		return False

	if (t_pos[1] == 0 and (a_port == 'A' or a_port == 'B')) or \
	(t_pos[1] == 9 and (a_port == 'E' or a_port == 'F')) or \
	(t_pos[0] == 0 and (a_port == 'H' or a_port == 'G')) or \
	(t_pos[0] == 9 and (a_port == 'C' or a_port == 'D')):
		return True
	return False

# check the physical condition of the board for given placement
def physical_condition(pos, board):
	'''
		@param: pos 	the position of tile
				board 	the board object
		@return: the boolean indicating if it's valid
	'''
	if pos[0] > 9 or pos[0] < 0 or pos[1] > 9 or pos[1] < 0:
		return False
	for tiles in board:
		for t in tiles:
			if (not t == None) and t.get_position() == pos:
				return False
	return True

# get the tile object's path map based on given position on board
def get_tile_path_map(pos, board):
	'''
		@param: pos 	the position of tile
				board 	the board object
		@return: the list of path of the tile
	'''
	tile = None
	path_map = {}
	for tiles in board:
		for t in tiles:
			if (not t == None) and t.get_position() == pos:
				tile = t
	if tile == None:
		return None
	for p in tile.get_list_of_path():
		path_map[p[0]] = p[1]
		path_map[p[1]] = p[0]

	return path_map


# given a tile and a port, give the tile position
# next to that port.
def new_pos(tile, port, board):
	'''
		@param: tile 	the tile
				port 	the port the avatar is one
				board 	the board object
		@return the position pair
	'''
	tile_pos_x = tile[0]
	tile_pos_y = tile[1]
	if port == 'A' or port == 'B':
		tile_pos_y -= 1
	if port == 'E' or port == 'F':
		tile_pos_y += 1
	if port == 'C' or port == 'D':
		tile_pos_x += 1
	if port == 'H' or port == 'G':
		tile_pos_x -= 1
	return (tile_pos_x, tile_pos_y)


# helper function for update_avatars. To check if the given port
# is connected to port on another tile
def connected_tile(tile, port, board):
	'''
		@param: tile 	the tile obejct
				port 	the port the avatar is one
				board 	the board object
		@return return the pair of avatar's position and port
	'''
	tile_pos_x = tile[0]
	tile_pos_y = tile[1]
	port_dir = ''
	path_map = {}
	connected_map = {
		'A': 'F',
		'F': 'A',
		'B': 'E',
		'E': 'B',
		'H': 'C',
		'C': 'H',
		'G': 'D',
		'D': 'G',
	}

	tile_pos = new_pos((tile_pos_x, tile_pos_y), port, board)
	port = connected_map[port]
	for tiles in board:
		for t in tiles:
			if (not t == None) and t.get_position() == tile_pos:
				for p in t.get_list_of_path():
					path_map[p[0]] = p[1]
					path_map[p[1]] = p[0]
				return (t.get_position(), port)

	return None

# ----- test ----
if __name__ == "__main__":
	b = Board([],[])

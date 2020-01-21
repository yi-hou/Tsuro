from tiles import Tile
from avatar import Avatar
from board import Board

# Rule Check class. This class checks if the rules of the game has been followed by the given information
# if not it will return False
class Rule:
	# take in a board, an avatar, a tile, and a list of tiles that are provided to player. Check if the 
	# tile placement and the avatar placement is legal.
	def check_initial_placement(self, gameboard, avatar, tile, list_of_tiles):
		'''

		:param gameboard: the board to place tile on
		:param avatar: avatar on the placed tile
		:param tile: tile that player chooses to place
		:param list_of_tiles: tiles given by referee
		:return: if the initial placement is legal or illegal
		'''
		board = gameboard.get_board()
		t_pos = tile.get_position()

		# checking if the tile is in the list of tiles provided
		if not check_in_list(tile, list_of_tiles):
			return False

		# the tile is placed on the border and have an avatar
		if not physical_condition(board, t_pos):
			return False
		if not (t_pos[0] == 0 or t_pos[1] == 0 or t_pos[0] == 9 or t_pos[1] == 9):
			return False
		if not avatar.get_position()[0] == t_pos:
			return False

		# avatar is being placed on the border side port and facing inside of the board
		if not avatar_on_border(board, t_pos, avatar):
			return False

		# get path map of the tile
		path_map = get_path_map(tile)
		exit_port = path_map[avatar.get_position()[1]]

		if (t_pos[0] == 0 and (exit_port == 'A' or exit_port == 'B'))\
		or (t_pos[0] == 9 and (exit_port == 'E' or exit_port == 'F'))\
		or (t_pos[1] == 0 and (exit_port == 'H' or exit_port == 'G'))\
		or (t_pos[1] == 9 and (exit_port == 'C' or exit_port == 'D')):
			# check if all 3 tiles given to the player will result exited upon initial placement no matter
			# what move player takes.
			legal_tile = False
			for t in list_of_tiles:
				temp_path_map = get_path_map(t)
				# there are legal initial tiles that can be placed.
				if not(temp_path_map['A'] == 'B' and temp_path_map['E'] == 'F' and temp_path_map['H'] == 'G'\
				and temp_path_map['C'] == 'D'):
					legal_tile = True
			# there are legal initial tile to be placed so the given placement is false
			if legal_tile:
				return False

		return True

	# take in a board, an avatar, a tile, and a list of tiles that are provided to player. Check if the 
	# tile placement is legal.
	def check_placement(self, gameboard, avatar, tile, list_of_tiles):
		'''

		:param gameboard: the board to place tile on
		:param avatar: avatar on the placed tile
		:param tile: tile that player chooses to place
		:param list_of_tiles: tiles given by referee
		:return: if the intermediate placement is legal or illegal
		'''
		new_gameboard = gameboard
		new_avatar = avatar
		old_pos = {}

		# checking if the tile is in the list of tiles provided
		if not check_in_list(tile, list_of_tiles):
			return False

		# check physical condition and whether the tile is next to avatar
		for a in gameboard.get_avatars():
			old_pos[a.get_color()] = a.get_position()
		if not physical_condition(new_gameboard.get_board(), tile.get_position()):
			return False
		a_pos = avatar.get_position()
		if not new_pos(a_pos[0], a_pos[1]) == tile.get_position():
			return False
			
		new_gameboard.add_tile(tile, new_avatar)
		# check the placement will not cause player's suicide unless
		# this is the only option.
		new_gameboard.update_avatars()
		# get avatar's updated position
		on_border = check_on_border(new_avatar)

		# if all tiles in list_of_tiles lead to suicide return true,
		# otherwise, return false.
		if on_border:
			for t in list_of_tiles:
				temp_tile = t
				temp_avatar = avatar
				# rotate temp_tile 3 times to check all possible rotations.
				for i in range(4):
					# reset board and avatars
					reset_pos(old_pos, gameboard.get_avatars())
					gameboard.del_tile(new_pos(a_pos[0], a_pos[1]))
					temp_board = gameboard
					temp_board.add_tile(temp_tile, temp_avatar)
					temp_board.update_avatars()
					# there are possible moves on tiles or selection of other tiles
					# to prevent suicide.
					if not check_on_border(temp_avatar):
						# reset board and avatars
						reset_pos(old_pos, gameboard.get_avatars())
						gameboard.del_tile(new_pos(a_pos[0], a_pos[1]))
						return False
					temp_tile.rotate(90)
		# reset board and avatars
		reset_pos(old_pos, gameboard.get_avatars())
		gameboard.del_tile(new_pos(a_pos[0], a_pos[1]))
		return True

	# check if a given player is dead
	def check_death(self, avatar):
		'''

		:param avatar: the avatar to be determined if it's dead
		:return: if the given avatar is dead or not
		'''
		a_pos = avatar.get_position()[0]
		a_port = avatar.get_position()[1]
		if (a_pos[1] == 0 and (a_port == 'A' or a_port == 'B')) or \
		(a_pos[1] == 9 and (a_port == 'E' or a_port == 'F')) or \
		(a_pos[0] == 0 and (a_port == 'G' or a_port == 'H')) or \
		(a_pos[0] == 9 and (a_port == 'C' or a_port == 'D')):
			return True
		return False

# avatar is being placed on the border side port and facing inside of the board
def avatar_on_border(board, t_pos, avatar):
	'''

	:param board: current board status
	:param t_pos: tile position
	:param avatar: avatar to be determined if it's placed on the border side port and facing inside of the board
	:return: if the avatar is placed on the border side port and facing inside of the board
	'''
	if not check_border(t_pos,avatar.get_position()[1]):
		return False
	if t_pos[0] == 0 or t_pos[0] == 9:
		if t_pos[1] + 1 <= 9 and (not board[t_pos[1] + 1][t_pos[0]] == None):
			return False
		if t_pos[1] - 1 >= 0 and (not board[t_pos[1] - 1][t_pos[0]] == None):
			return False
	if t_pos[1] == 0 or t_pos[1] == 9:
		if t_pos[0] + 1 <= 9 and (not board[t_pos[1]][t_pos[0] + 1] == None):
			return False
		if t_pos[0] - 1 >= 0 and (not board[t_pos[1]][t_pos[0] - 1] == None):
			return False

	return True

# get tile's port connection in a map and get exit port
def get_path_map(tile):
	'''

	:param tile: tile to be determined the exit port
	:return: path map of the given tile
	'''
	path = tile.get_list_of_path()
	path_map = {}
	for p in path:
		path_map[p[0]] = p[1]
		path_map[p[1]] = p[0]
	return path_map


# checking if the tile is in the list of tiles provided
def check_in_list(tile, list_of_tiles):
	'''

	:param tile: tile to be determined if it's in the given list
	:param list_of_tiles: tiles given by the referee
	:return: if the tile is in the given list of tiles
	'''
	tile_in_list = False
	for t in list_of_tiles:
		if t.idx == tile.idx:
			tile_in_list = True

	return tile_in_list

# check if the given initial placement's avatar is valid
# meaning it is placed on the side of the board
def check_border(t_pos, a_port):
	'''

	:param t_pos: tile's position
	:param a_port: the port that the avatar is on
	:return: if the avatar is placed on the side of the board
	'''
	if (t_pos[1] == 0 and (a_port == 'A' or a_port == 'B')) or \
	(t_pos[1] == 9 and (a_port == 'E' or a_port == 'F')) or \
	(t_pos[0] == 0 and (a_port == 'H' or a_port == 'G')) or \
	(t_pos[0] == 9 and (a_port == 'C' or a_port == 'D')):
		return True
	return False

# given a tile and a port, give the tile position
# next to that port.
def new_pos(tile, port):
	'''

	:param tile: current tile
	:param port: the port on the current tile
	:return: next position of the tile that is placed next to the current tile
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

# check the physical condition of the board for given placement
def physical_condition(board, t_pos):
	'''

	:param board: current board
	:param t_pos: tile's position that is going to be placed on the board
	:return: if the placement is obey physical condition
	'''
	if (not board[t_pos[1]][t_pos[0]] == None) or t_pos[0] < 0 or t_pos[1] < 0 or t_pos[0] > 9 or t_pos[1] > 9:
		return False
	return True

# check if the given avatar position is on border
def check_on_border(a):
	'''

	:param a: the avatar to be determined if it's placed on the border
	:return: if the avatar is placed on the border
	'''
	tile_pos = a.get_position()[0]
	port = a.get_position()[1]
	if tile_pos[0] == 0 and (port == 'H' or port == 'G'):
		return True
	if tile_pos[1] == 0 and (port == 'A' or port == 'B'):
		return True
	if tile_pos[0] == 9 and (port == 'C' or port == 'D'):
		return True
	if tile_pos[1] == 9 and (port == 'F' or port == 'E'):
		return True
	return False

# helper function to reset all avatars' position to previous position
def reset_pos(old_pos, list_of_avatars):
	'''

	:param old_pos: dict to store avatar's previous positions
	:param list_of_avatars: list of avatars in the game
	:return: reset all avatars' position to previous positions
	'''
	for a in list_of_avatars:
		a_pos = old_pos[a.get_color()]
		a.update_position(a_pos[0], a_pos[1])
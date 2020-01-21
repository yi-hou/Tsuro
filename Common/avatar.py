from tiles import Tile

# Avatar class that represents an avatar representing the player
class Avatar:
	# constructor
	def __init__(self, color, position):
		'''

		:param color: color that represents the avatar
		:param position: position of the avatar
		'''
		self.color = color
		self.position = position

	# getters
	def get_position(self):
		'''

		:return: position of the avatar
		'''
		return self.position

	def get_color(self):
		'''

		:return: color of the avatar
		'''
		return self.color

	# setter
	def update_position(self, tile, port):
		'''

		:param tile: tile's position
		:param port: port on the tile
		:return: update avatar's position on given tile and the given port
		'''
		tile_pos = tile
		if tile is Tile:
			tile_pos = tile.get_position()
		self.position = (tile_pos, port)

	def update_port(self, port):
		'''

		:param port: port to be updated
		:return: update avatar's position with given port
		'''
		new_pos = (self.get_position()[0], port)
		self.position = new_pos

	# return a map of path
	def get_next_port(self):
		'''

		:return: path map
		'''
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
		port = self.position[1]
		return connected_map[port]

	# get the position that could place tile next to the avatar
	def get_new_pos(self):
		'''

		:return: position to place next tile
		'''
		tile = self.position[0]
		port = self.position[1]
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
		if tile_pos_x > 9 or tile_pos_x < 0 or\
		tile_pos_y > 9 or tile_pos_y < 0:
			return tile
		return (tile_pos_x, tile_pos_y)
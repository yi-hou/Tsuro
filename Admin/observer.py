import sys
sys.path.insert(0, '../Common')

from tiles import Tile
from avatar import Avatar
from board import Board
from PIL import Image, ImageDraw


class Observer:
	# constructor
	def __init__(self, board):
		'''
		# The observers class that show the graphical representation of the current Tsuro game
		The constructor of Observer, it needs to take the a board
		:param board: Board, the object board
		'''
		self.tiles = board.get_tiles()
		self.avatars = board.get_avatars()

	# draw board
	def show_image(self):
		'''
		Render the graphical board by converting a board to image
		:return:Image, the current state of board
		'''

		# create a board's board
		img = Image.new('RGBA', (3000, 3000), (222,184,135))
		draw = ImageDraw.Draw(img)
		# draw grid
		for i in range(0, 10):
			linex = ((300+i*300,0), (300+i*300,3000))
			draw.line(linex, fill='black')
			liney = ((0,300+i*300), (3000,300+i*300))
			draw.line(liney, fill='black')
		# draw tiles and avatars
		for tile in self.tiles:
			pos = tile.get_position()
			img.paste(tile.display(),(pos[0]*300, pos[1]*300))

		for avatar in self.avatars:
			pos = avatar.get_position()
			draw_avatar(pos[0][0] * 300, pos[0][1] * 300, pos[1], avatar.get_color(),draw)
		img.show()


def get_port_pos(x, y, port):
	'''
	helper function to get a portPos with repective x and y position
	:param x: integer, the position of tile's x coordinate
	:param y: integer, the position of tile's y coordinate
	:param port: String, the port name
	:return: Tuple of integer, the position of the port
	'''
	portPos = {
		'A': (100, 0),
		'B': (200, 0),
		'C': (300, 100),
		'D': (300, 200),
		'E': (200, 300),
		'F': (100, 300),
		'G': (0, 200),
		'H': (0, 100)
			}
	pos = portPos[port]
	portPos[port] = (pos[0] + x, pos[1] + y)

	return portPos[port]


def draw_avatar(x, y, port, color, draw):
	'''
	# helper function to draw avatar
	:param x: integer, the position of tile's x coordinate
	:param y: integer, the position of tile's y coordinate
	:param port: String, the port name
	:param color: String, string is to represent color
	:param draw: Image, the backgroud/tile where avatat should on
	:return: Draw an avatar on the tile
	'''
	pos = get_port_pos(x, y, port)
	draw.ellipse([(pos[0]-10, pos[1]-10), (pos[0]+10, pos[1]+10)], fill = color, outline = color, width=8)
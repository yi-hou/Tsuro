# Implement pillow library
# In order to run the library,
# Python3: `pip3 install Pillow`
# Python2: `pip install Pillow`
from PIL import Image, ImageDraw
import ast

class Tile:
    def __init__(self, idx, position):
        '''
        The constructor of Tile, it needs to take the index of tile and the position of tile to construct a board
        :param idx: int, the index of tile in 35 tiles
        :param position: tuple of integer, the position (x,y) of tile on the 10x10 board
        '''
        self.idx = idx
        self.position = position
        self.list_of_path = get_tiles()[idx][1]

    def get_position(self):
        '''
        Getter method: get the position of tile
        :return: a tuple of integer,  the position of tile
        '''
        return self.position

    def get_list_of_path(self):
        '''
        Getter method: get the tile's list of path
        :return: list of tuples, tile's list of path
        '''
        return self.list_of_path.copy()

    def equals(self, tile):
        '''
        Check whether the given tile equals to the current tile. Even the tile is rotated, it should be the same.
        If both tiles have same list of path, but different location, it means that two tiles are different
        :param tile: Tile object, given tile
        :return: boolean, equals or not
        '''
        if self.position != tile.get_position():
            return False
        count = 0
        for path in tile.get_list_of_path():
            if path in self.list_of_path or (path[1], path[0]) in self.list_of_path:
                count += 1
        return count == 4

    def updatePos(self, x, y):
        '''
        Update the tile's position by the x and y
        :param x: int, x-axis
        :param y: int, y-axis
        '''
        self.position = (x, y)

    def updatePath(self, time, path_list):
        '''
        Update the list of path by the rotated times(times of 90 degrees)
        :param time: integer, times that the tile needs to be rotated by 90 degree clock wise
        :param path_list: list, tile's list of path
        :return: list, the new list of path based on the rotated times
        '''

        changeTable = {
            # We changed port representation to A - G by 90 degree clockwise,
            # like port of rotated 90 degree of port A is C
            'A' : 'C',
            'B' : 'D',
            'C' : 'E',
            'D' : 'F',
            'E' : 'G',
            'F' : 'H',
            'G' : 'A',
            'H' : 'B'
            }

        # rotate the tile 90 degree by times(degree/90)
        for i in range(time):
            path_rotate = []
            for pos in path_list:
                pos_start = (changeTable[pos[0]])
                pos_end = (changeTable[pos[1]])
                path_rotate.append([pos_start, pos_end])
            path_list = path_rotate

        return path_list

    def rotate(self, degree):
        '''
        Rotate the tile by the degree, the default rotate is clockwise,
        rotate the tile clockwise and change its path accordingly
        :param degree: integer, rotated degree
        :return: rotate the tile and update it's path or raise exception if the degree is not 0,90,180,270
        '''
        if degree == 0 or degree == 90 or degree == 180 or degree == 270:
            self.list_of_path = self.updatePath(int(degree / 90), self.list_of_path)
        else:
            raise Exception("Invalid degree")

    def find_exit(self, entry):
        '''
        Find the exit port by the entry port
        :param entry: string, the entry port
        :return: string, the exit port
        '''
        result = ''
        for path in self.list_of_path:
            if path[0] == entry:
                result = path[1]
            elif path[1] == entry:
                result = path[0]
        return result

    def drawLine(self, pos_start, pos_end, draw):
        '''
        Draw the path(line) on the tile
        :param pos_start: tuple of integer, the start position
        :param pos_end: tuple of integer, the end position
        :param draw: Image, the board image
        :return: draw lines on the board image
        '''
        # When the path's ports are on the same direction, it has four different cases
        # North and South side. y is same, x is different.`

        if pos_start[1] == pos_end[1] and abs(pos_start[0] - pos_end[0]) == 100:
            if pos_start[0] > pos_end[0]:
                draw.arc([(pos_end[0], pos_end[1] - 90), (pos_start[0], pos_start[1] + 90)], 180, 0, 'orange', width=6)
            else:
                draw.arc([(pos_start[0], pos_start[1] - 90), (pos_end[0], pos_end[1] + 90)], 0, 180, 'orange', width=6)
        # East and West side. x is same, y is different
        elif pos_start[0] == pos_end[0] and abs(pos_start[1] - pos_end[1]) == 100:
            if pos_start[1] > pos_end[1]:
                draw.arc([(pos_start[0] - 90, pos_end[1]), (pos_end[0] + 90, pos_start[1])], 270, 90, 'orange', width=6)
            else:
                draw.arc([(pos_start[0] - 90, pos_start[1]), (pos_end[0] + 90, pos_end[1])], 90, 270, 'orange', width=6)
        # Path's ports are on different directions
        else:
            draw.line((pos_start[0], pos_start[1], pos_end[0], pos_end[1]), fill='orange', width=6)


    def display(self):
        '''
        Render to display of image of tile by converting tile object to a image
        :return: image
        '''

        portPos = {
        # board to convert the port to location
        # We changed port representation to A - G
        'A': (100, 0),
        'B': (200, 0),
        'F': (200, 300),
        'E': (100, 300),
        'H': (300, 100),
        'G': (300, 200),
        'C': (0, 200),
        'D': (0, 100)
        }

        # create a tile's board
        im = Image.new('RGBA', (300, 300), (255, 255, 255))

        # Draw on the board
        draw = ImageDraw.Draw(im)

        # boarder of the board
        draw.rectangle([(0, 0), (299,299)], fill=(184, 134, 11), outline='darkgrey', width=1)

        # draw ports
        for port, pos in portPos.items():
            draw.ellipse([(pos[0] - 10, pos[1] - 10), (pos[0] + 10, pos[1] + 10)], fill='yellow', outline='yellow',
                         width=5)
        # draw path
        for pos_start, pos_end in self.list_of_path:
            self.drawLine(portPos[pos_start], portPos[pos_end], draw)
        return im

def get_tiles():
    '''
    Get 35 tiles from the existing json file.
    helper function for constructor. To translate idx to tiles from json file provided
    :return: list of 35 tiles
    '''
    f = open("../2/tiles.json", "r" )
    tiles = []
    for line in f.readlines():
        if line[-1] == '\n':
            line = line[:-1]
        tile = ast.literal_eval(line)
        tiles.append(tile)
    f.close()
    return tiles.copy()

#  --------------------- Function of generate 35 distinct tiles -----------------------

def check_dup(list_of_lines, line):
    '''
    Check if the list of lines and line has duplicated port.
    :param list_of_lines: list, list of path
    :param line: tuple, a pair of ports
    :return: boolean,whether there is a duplicate line in the list path
    '''
    for l in list_of_lines:
        if (line[0] in l) or (line[1] in l):
            return True
    return False


def valid_line(line, list_lines):
    '''
    Check if the line provided is valid within the list of lines
    :param list_of_lines: list, list of path
    :param line: tuple, a pair of ports
    :return: boolean, whether line provided is valid within the list of lines
    '''
    if line[0] == line[1]:
        return False
    for l in list_lines:
        if line[0] == l[0] and line[1] == l[1]:
            return False
        if line[1] == l[0] and line[0] == l[1]:
            return False
    return True


def valid_tile(tile, list_path):
    '''
    Check if the tile provided is valid within the list of tile path
    :param tile: Tile, tile object
    :param list_path: list, list of path
    :return: boolean, whether the tile provided is valid within the list of tile path
    '''
    tile90 = Tile(tile.get_list_of_path(), None)
    tile180 = Tile(tile.get_list_of_path(), None)
    tile270 = Tile(tile.get_list_of_path(), None)
    tile90.rotate(90)
    tile180.rotate(180)
    tile270.rotate(270)
    for path in list_path:
        t = Tile(path, None)
        if t.equals(tile) or t.equals(tile90) or t.equals(tile180) or t.equals(tile270):
            return False
    return True

def generate_35_tiles():
    '''
    Render the method to generate 35 distinct tiles
    :return: list of 35 tiles
    '''
    list_of_lines = []
    list_of_ports = []
    list_of_tiles = []
    list_of_path = []


    for port1 in list_of_ports:
        for port2 in list_of_ports:
            if valid_line((port1, port2), list_of_lines):
                list_of_lines.append((port1, port2))

    # Generate 105(7*5*3) tiles and remove duplicated tiles
    # looping over all lines, and pick the valid path to form
    # tile path and check if it's valid. Also improve performance
    # by check non-duplicate tiles.
    for l1 in range(len(list_of_lines)):
        tilePath = []
        tilePath.append(list_of_lines[l1])
        line1 = list_of_lines[l1]
        l2 = l1
        while l2 < len(list_of_lines):
            line2 = list_of_lines[l2]
            if check_dup(tilePath, line2):
                l2 += 1
                continue
            tilePath.append(line2)
            l3 = l2
            while l3 < len(list_of_lines):
                line3 = list_of_lines[l3]
                if check_dup(tilePath, line3):
                    l3 += 1
                    continue
                tilePath.append(line3)
                l4 = l3
                while l4 < len(list_of_lines):
                    line4 = list_of_lines[l4]
                    if check_dup(tilePath, line4):
                        l4 += 1
                        continue
                    tilePath.append(line4)
                    tile = Tile(tilePath, None)
                    if valid_tile(tile, list_of_path):
                        list_of_path.append(tilePath.copy())
                    tilePath.remove(line4)
                    l4 += 1
                tilePath.remove(line3)
                l3 += 1
            tilePath.remove(line2)
            l2 += 1
        tilePath.remove(line1)
    # Create tiles with the generated tile path and
    # add them into the list
    for path in list_of_path:
        list_of_tiles.append(Tile(path, None))

    ## printing out all tile path generated
    for tile in list_of_tiles:
        print(tile.get_list_of_path())

    # for check there are 35 tiles at the end
    print(len(list_of_tiles))

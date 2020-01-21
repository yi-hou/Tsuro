import sys

sys.path.insert(0, '../Common')
sys.path.insert(0, '../Player')
from player_interface import PlayerInterface
from tiles import Tile
from avatar import Avatar
import json

# the proxy class that function as a player proxy which will convert
# the data and transfer data between server and client
class Proxy(PlayerInterface):
    # constructor
    def __init__(self, sock, addr):
        '''

        :param sock: client connection
        :param addr: client address
        '''
        self.sock = sock
        self.addr = addr
        self.name = ''
        self.color = ''

    # the initial placement function
    def initial_placement(self, gameboard, tiles, avatar, color):
        '''

        :param gameboard: current board
        :param tiles: tiles given by referee
        :param avatar: avatar on the placed tile
        :param color: color of the avatar
        :return: client's response and constructed tile avatar objects based on client's response
        '''
        request = ['initial_placement', gameboard, tiles, avatar]
        self.sock.sendall(json.dumps(request, default=jdefault).encode('utf-8'))
        # self.sock.sendall(request.encode('utf-8'))
        result = self.sock.recv(1024).decode('utf-8')
        res = json.loads(result)
        self.name = res[0]
        self.color = color
        return construct_obj([res[1], res[2]]), result

    # the intermediate placement function
    def placement(self, gameboard, tiles, avatar):
        '''

        :param gameboard: current board
        :param tiles: tiles given by referee
        :param avatar: avatar placed on the tile
        :return: client's response and constructed tile, avatar objects based on client's response
        '''
        request = ['intermediate_placement', gameboard, tiles, avatar]
        self.sock.sendall(json.dumps(request, default=jdefault).encode('utf-8'))
        # self.sock.sendall(request.encode('utf-8'))
        result = self.sock.recv(1024).decode('utf-8')
        res = json.loads(result)
        return construct_obj(res), result

    # getters
    def get_sock(self):
        '''

        :return: client connection
        '''
        return self.sock

    def get_addr(self):
        '''

        :return: client address
        '''
        return self.addr


# turn unserializable object into a list of dict
def jdefault(o):
    return o.__dict__


# construct tile and avatar from the serialized list
def construct_obj(res):
    '''

    :param res: response received from client
    :return: constructed tile, and avatar object received from client
    '''
    tile_dict = res[0]
    avatar_dict = res[1]
    tile = Tile(tile_dict['idx'], None)
    if not tile_dict['position'] == None:
        tile.position = (tile_dict['position'][0], tile_dict['position'][1])
    tile.list_of_path = tile_dict['list_of_path']
    avatar = Avatar(avatar_dict['color'], None)
    if not avatar_dict['position'] == None:
        pos = avatar_dict['position'][0]
        port = avatar_dict['position'][1]
        avatar.position = ((pos[0], pos[1]), port)
    return tile, avatar

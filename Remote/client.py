import sys
sys.path.insert(0, '../Player')
import socket
from player import Player
import json
sys.path.insert(0, '../Common');

# turn unserializable object into a list of
def jdefault(o):
    return o.__dict__

def main(HOST, PORT, NAME, STRATEGY):
    '''

    :param HOST: the server host is going to connect to
    :param PORT: the server port is going to connect to
    :param NAME: name of the client/player
    :param STRATEGY: the strategy that the player plans to use
    :return: open the socket, connect to the server and communicate with the server
    '''
    # connect to socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server
    try:
        client.connect((HOST, PORT))
    except:
        raise Exception("please enter valid host and port")

    player = Player(NAME, STRATEGY)

    # exchange information with server
    while True:
        server_res = client.recv(20480).decode('utf-8')
        res = json.loads(server_res)

        if res[0] == 'initial_placement':
            tile, avatar = player.initial_placement(res[1], res[2], res[3])
            result = [player.name, tile, avatar]
            client.sendall(json.dumps(result, default=jdefault).encode('utf-8'))
        elif res[0] == 'intermediate_placement':
            tile, avatar = player.placement(res[1], res[2], res[3])
            result = [tile, avatar]
            client.sendall(json.dumps(result, default=jdefault).encode('utf-8'))
        elif res[0] == 'game over':
            player.render_result(res[1])
            break

    client.close()
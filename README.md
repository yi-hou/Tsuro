# Tsuro
A board game called Tsuro. A strategy game to 'connect' your friends out of the game board and win!!! <br>
Our team member: Tianwei Li, Jiangyun Wang, Yi Hou, Ziyi Zhao, Huisiyu Yu
# How to play
##### Term definitions
- Game Board - a 10x10 grids with four edges.
- Avatar - a figure to represent a player in the game.
- Tile - Each tile is a square with 8 ports, 2 per side. The four sides are called north, east, south, and west. Each tile specifies four distinct connections between two distinct ports; every port must have exactly one connection.
- Players: Automated pre-programmed player, which will think like a human.
##### Rules
- Each game consists from three to five players.
- Each players places their avatars at 4 edges randomly, choose their first tile from 3 assigned random tiles and place it on the game board.
- The picked tile can be rotated by 90, 180 or 270 degrees.
- Starting from round two, each player will draw two different tiles and pick one to place on the board.
- The avatar must move forward when there is path created by connected tiles.
- Once the avatar reaches the board’s periphery, it is out.
##### To WIN the game
- there is only one avatar left on the board; the avatar’s owner is the winner;
- all remaining avatars reach the board’s periphery during the same round; the owners of these avatars are joint winners.

# Folder Struture
```
.
├── 1
│   ├── allTiles.py
│   ├── tile-1.PNG
│   ├── tile-2.PNG
│   └── tile-3.PNG
├── 2
│   ├── tile-test
│   ├── tiles.json
│   └── xtiles
├── 3
│   ├── board-tests
│   │   ├── 1-in.json
│   │   ├── 1-out.json
│   │   ├── 2-in.json
│   │   ├── 2-out.json
│   │   ├── 3-in.json
│   │   ├── 3-out.json
│   │   ├── 4-in.json
│   │   ├── 4-out.json
│   │   ├── 5-in.json
│   │   └── 5-out.json
│   └── xboard
├── 4
│   ├── README-tests.md
│   ├── rules-tests
│   │   ├── 1-in.json
│   │   ├── 1-out.json
│   │   ├── 2-in.json
│   │   ├── 2-out.json
│   │   ├── 3-in.json
│   │   ├── 3-out.json
│   │   ├── 4-in.json
│   │   ├── 4-out.json
│   │   ├── 5-in.json
│   │   └── 5-out.json
│   └── xrules
├── 5
│   ├── README-tests.md
│   ├── obs-tests
│   │   ├── 1-in.json
│   │   ├── 1-out.png
│   │   ├── 2-in.json
│   │   └── 2-out.png
│   ├── ref-tests
│   │   ├── 1-in.json
│   │   ├── 1-out.json
│   │   ├── 2-in.json
│   │   └── 2-out.json
│   ├── xobs
│   └── xref
├── 6
│   ├── READEME-tests.md
│   ├── strategy.md
│   ├── xclient
│   ├── xrun
│   ├── xserver
│   └── xserver.log
├── Admin
│   ├── __pycache__
│   │   ├── observer.cpython-37.pyc
│   │   └── referee.cpython-37.pyc
│   ├── observer.py
│   └── referee.py
├── Common
│   ├── __pycache__
│   │   ├── avatar.cpython-37.pyc
│   │   ├── board.cpython-37.pyc
│   │   ├── player.cpython-37.pyc
│   │   ├── referee.cpython-37.pyc
│   │   ├── rules.cpython-37.pyc
│   │   └── tiles.cpython-37.pyc
│   ├── avatar.py
│   ├── board.py
│   ├── rules.py
│   └── tiles.py
├── Planning
│   ├── board.md
│   ├── observer.md
│   ├── plan.md
│   ├── player.md
│   ├── protocol.md
│   ├── referee.md
│   └── rules.md
├── Player
│   ├── __pycache__
│   │   ├── player.cpython-37.pyc
│   │   ├── player_interface.cpython-37.pyc
│   │   └── strategy.cpython-37.pyc
│   ├── player.py
│   └── player_interface.py
├── README.md
└── Remote
    ├── __pycache__
    │   ├── client.cpython-37.pyc
    │   ├── player_proxy.cpython-37.pyc
    │   └── server.cpython-37.pyc
    ├── client.py
    ├── player_proxy.py
    └── server.py
```

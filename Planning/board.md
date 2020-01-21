### Overview

The board can be represented by a 2D array, with each of the element be either `None`, which represents an empty grid, or a Tile object, which means the certain Tile object is being placed on the grid. The board's array indexes can be used to refer to certain Tile object or an empty grid. The board can be displayed to the players and referees with a graphical version of the 2D array displaying board with empty grid and Tile object using Tile object's own graphically display method.

##### Tile Class
Tile is a square with 8 ports, 2 per side, and it specifies four distinct connections between two distinct ports; every port must have exactly one connection. A Tile records its own path and the current position. The `position` variable is the Tile's position on the board and will be `None` if a tile is generated but hasn't been placed on board yet. The `list_of_path` variable is used to store the four path in between 8 ports. It contains 4 pairs each contains two pairs, with the representation `(direction, number)` to represent two ports on each side of the tile. The list should resemble this.
```
[(('north', 2), ('south', 1)), (('east', 2), ('south', 2)), (('east', 1), ('west', 2)), (('west', 1), ('north', 1))]
```

**Variables:**
- ``list: list_of_path``
- ``pair: position``

Tile class is intended to represent the tiles in the game. This Class should implement the following method. The `rotate(int degree)` will be called by the automated player and update the Tile class respectively. The `updatePos(int x, int y)` will be used to update it's position once the player decide where to place this tile in the game board. And `display()` method which is used to display Tile object graphically.

##### Avatar Class
Avatar is a color token which should be one of the colors: ``white, black, red, green, blue``. It represents a player on
a port of one of the placed tiles. An Avatar stores its own color and its current position. Moreover,it records its own path. 

**Variables:**
- ``str: color``
- ``pair: <tile, dir_port> ``
   - ``pair: dir_port = <direction, n>``
   - ``str: direction (north, east, south, west)``
   - ``int: n (1,2)``
- ``list: list_of_pos``

Avatar class is intend to represent the avatar in game and it should implement an update method `update(Tile t, (String dir, int n))`. The Tile is an Tile object and the pair contains a directions which is North, South, West, or East, and a number. This is used to represent the 8 port on each tile. This will be called by Game class to update avatar's position and the port it's currently on.

##### Referee Class
Referee class is the representation of the game referee who decides when the game should end and the status of each player and their avatars. The Referee class should be constructed with a Board object and a list of Players

**Variables**
- ``Board: board``
- ``list: list_of_players``

It should have a `checkAlive(Avatar a)` to determine if each avatar is still alive after the new round. And the method `updateAvatars()` to go thourgh the avatar list and update each avatar with their final position after traversing through to the end of their path. This function should call the `checkAlive(Avatar a)` function to determine if the given avatar is dead when arriving at certain position. This method should return an updated `list_of_avatars`. Referee Class should also contain a method `checkEnd()` to check if the game is ending, and return a boolean indicating whether the game is over or not. Referee Class should also contains method `deal(list list_of_tile)` which will deal a list of tiles to player and will return the tile the player decided to choose.

##### Board Class
Board is the game board which contains avatars representing each player, and all the tiles that are being placed by players. Board class should have a 2D array containing Tile objects and a list containing avatars indicating how many avatars are left and their positions. 

**Variables:**
- ``Tile[][]: board``
- ``list: list_of_avatars``
- ``Referee: referee``

Board should have method `addTile(Tile t, (int x, int y))` to add a Tile object in the given indexes of 2D array.  And the board class will have getter methods so the informations get be accessed by players to do prediction based on the current board, their avatar's position, and the new tiles they are provided. Board should also have `addAvatar(Avatar a)` method to add new avatars to the list and place it on the board. Board should also contains setter method fro `board` and `list_of_avatars` variables so they can be updated. Finally, board should have a display method to display the board graphically.
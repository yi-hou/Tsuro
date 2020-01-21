# Part 1
There are two identifiable components in our software system: an `automated player` and the `game software` in the server.
The server contains four classes: `Avatar`, `Tile`, `Player`, `Game`. 
 - `automated player`  has one piece: `Player`
 - `game software` has three pieces: `Avatar`, `Tile`, `Game`
### Tile
Tile is a square with 8 ports, 2 per side, and it specifies four distinct connections between two distinct ports; every 
port must have exactly one connection. A Tile records its own path and the current position.

**Variables:**
- ``list: list_of_path``
- ``pair: position``
### Avatar
Avatar is a color token which should be one of the colors: ``white, black, red, green, blue``. It represents a player on
a port of one of the placed tiles. An Avatar stores its own color and its current position. Moreover,it records its own 
path. 

**Variables:**
- ``str: color``
- ``pair: <tile, dir_port> ``
   - ``pair: dir_port = <direction, n>``
   - ``str: direction (north, east, south, west)``
   - ``int: n (1,2)``
- ``list: list_of_pos``
### Player
Player is a player who chooses a tile and decides its position on the board and the start position of 
the ``Avatar``. Furthermore, it knows the whole process of the ``Game`` and sends its own decision of the next tile to the 
``Game``. Meanwhile, it gets the information from the ``Game`` that it wins or loses.

**Variables:**
- ``Avatar: avatar``
- ``boolean: lose``
### Game
`Game` starts Tsuro and assigns ``Avatars`` to ``Players``. For each round, ``Player`` places the `tile` on the 
 `board`, and `Game` updates `Avatars` based on the new added tile. After that, it checks if any `Player`
 loses the game. If anyone loses, `Game` removes the `Avator` and sends to the related `Player` that he/she loses the game. Otherwise, 
 `Game` continues until someone wins.

**Variables:**
- ``list: list_of_Avatar``
- ``array[][]: board ``
- ``int: round``


# Part 2
### Player Class
Player class is intended to mock behavior of a basic human play. WIth the field Avatar object `avatar` and Boolean variable `lose`, each Player object will call the method `join(Game game)` to join the game . The Player class also contians the method `chooseTiles(list_of_tile)` to choose randomly from a list of tiles and make sure placement of that tile will not lead to the loss of he or she with the `predict(Tile tile)` method. The Player class also contains `generate(Tile tile)` which will randomly generate the the position of first tile and the port the avatar will start on while ensuring as much as possible that it will not loss in this beginning round by calling `predict(Tile tile)` inside it. The Player class can access information about the game by calling getter method in the Game class and use it to predict. The `generate(Tile tile)` method will only be called in the beginning round in the `chooseTiles(list_of_tile)` when it receives a list of three tiles so the player start the game and place avatar on it. And in the future rounds when it receives a list of two tiles only `predict(Tile tile)` method will be called to make sure the randomly selected tile will not lead to the lost of the play.

### Avatar Class
Avatar class is intend to represent the avatar in game and it should implement an update method `update(Tile t, (String dir, int n))`. The Tile is an Tile object and the pair contains a directions which is North, South, West, or East, and a number. This is used to represent the 8 port on each tile. This will be called by Game class to update avatar's position and the port it's currently on.

### Tile Class
Tile class is intended to represent the tiles in the game. This Class should implement the following method. The `rotate(int degree)` will be called by the automated player and update the Tile class respectively. The `updatePos(int x, int y)` will be used to update it's position once the player decide where to place this tile in the game board.

### Game Class
Game class is the class that represent the Tsuro Game as a whole. This class should implement the following methods. `addTile(Tile tile, (int x, int y))` which will be called by the player to place a tile of the game board. This tile will be added to the `board` variable in Game class with `(x, y)` as the column and row in the `board` 2D array. The `start(int num_of_players)` should start the game and decide how many players are in the game. This will include an while loop inside to represent each round of the game. The `checkAlive(Avatar avatar)` method which decide if each avatar is in a position where would cause the player to lose. The `updateAvatar()` method which will go through the `list_of_avatars` list and update the position of each avatar after each tile is placed on the game board and call `checkAlive()` to decide if the given avatar is dead and the player lost or not. The `updateAvatar()` method will also check the status of the game by checking if there is only one avatar left in the game or no avatar left in the game after the current round. The Game class does not need to know informations about Player other than what avatar is each player responsible to and only needs to pass information to the Player class when required and receive the actions from Player. The Game class should also contains getter method to be able to pass information to Player class while ensure encapsulation. Other helper method such as `checkEnd()` which will check if we should break from the while loop in `start(int num_of_players)` method or `getWinner()` which will return the winner or winners are recommended but not required.

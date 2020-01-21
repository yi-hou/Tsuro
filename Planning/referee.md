##### Referee Component
A referee, one may also indicate by game manager is the component that starts the game, provides tiles to players each turn, and decides if an avatar is dead or not. This component should take in a list of players and a board.

**Variables:**
- ``list_of_players``

The method referee component should have a `start_round(board, init)` method which takes in a Board object and a boolean variable indicating if this is the initial turn or not. Then inside the method the referee component should iterate through the list of players and provide each player with either 3 or 2 tiles and then place the tile on the board by first calling Rule Checker component to decide if the given placement is legal, then call Board method to place the tile. After each time a tile is placed, update the board and check if any avatars is exited or collided. Another `check_end()` method to check if there are currently only one player left or no player left, which indicates the game has ended. Also the class should have method `startGame()` which will include a while loop to keep the game running until it has ended. In the end of the while loop, the method should return a list of winners.
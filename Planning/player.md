##### Player Component
Player is a component interacts with game system in Tsuro game. The player interface should have functions to prompt the player to give their turn, update the state of the game, and notify the player about the game ending. It takes in an Avatar which represents himself/herself in the game, contains a boolean to represents its status in the game(lose/win).

**Variables:**
- ``Avatar: avatar``
- ``Boolean: lose``

It should have following methods:

`prompt()` which notifies player to give his/her turn.

`update_position(tile, port)` which calls `update_position` method in avatar's class and updates position in game.  

`place_tile(referee, tile, list_of_tiles, init)` which takes in a referee, a tile he/she chooses, a list of tiles given by referee and a boolean variable indicating if this is the initial turn or not, and inside of this method, it calls referee to check if the placement is valid or not(potentially Rule Checker component is called in referee to check legality of placement). 
 
`end_game()` which notifies the player about game ending. It could be the player loses, existing from the board or he/she wins, being the only one left in the game.  

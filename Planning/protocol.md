referee 	  player: P-1  ... ... player: P-N
| 					| 					 |
|------------------>| 					 | playing as: color
| 					| 					 |
				  . . .
| 					| 					 |
|-------------------|------------------->| playing as: color
| 					| 					 |
|-----------------> |					 | other players: colors
| 					| 					 | % the colors of the other players
				  . . .
| 					| 					 |
|--------------------------------------> | other players: colors
| 					|					 |
|-----------------> | 					 | initial placement: ['initial_placement', board, list_of_tiles, avatar]
| <================ | 					 | tile, avatar
				  . . .
|--------------------------------------> | initial placement: ['initial_placement', board, list_of_tiles, avatar]
| <===================================== | tile, avatar
				  . . .
| 					|  					 |
|-----------------> | 					 | take turn: ['intermediate_placement', board, list_of_tiles, avatar]
| <================ | 					 | tile, avatar
				  . . .
| -------------------------------------> | take turn: ['intermediate_placement', board, list_of_tiles, avatar]
| <===================================== | tile, avatar
| 					| 					 |
				  . . .
| 					|  					 |
|-----------------> | 					 | take turn: results
|					| 					 | ['game over', win or lose]
				  . . .
| -------------------------------------> | take turn: results
| 					|					 | ['game over', win or lose]
| 					| 					 |
##### Observing Component
Observer is a component observes the game, but not engage into it. The observer interface should have functions that get updated by the game system about the game state and provide renderings of the current game state.

**Variables:**
- ``Board: board``

It should have following methods:

`update_game_state(referee)` which takes in a referee, and referee should update the board in the class.

`render_game_state()` which calls update_game_state(referee) and renders the current game board to observer.
    
`end_game()` which notifies the observer about game ending.  

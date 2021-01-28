#!/usr/bin/python3

import engine
import pieces
import players
import test_states
import state
import copy

class Game:
    """The Game class contains the game state and engine objects. The
    main game loop is handled here."""
    def __init__(self, resolution):
        self.resolution = resolution
        self.engine = engine.GfxEngine(self.resolution)
        self.game_state = state.GameState([])
        self.history = []
        # one player by default
        self.player_list = [players.Human("white"), players.AI("black", "random")]
    
    def new_game(self):
        """Sets up a GameState object for a new game."""
        self.game_state.piece_list = test_states.new_game_pieces
        self.game_state = state.update_state(self.game_state)
        self.history.append(copy.deepcopy(self.game_state))
    
    def undo(self):
        """Rolls the game back to its state two moves (one white, one black) ago."""
        # First check we're not on the first move
        if len(self.history) <= 1:
            print("Nothing has moved, nothing to undo.")
            self.engine.undo = False
            return None
        else:
            # Reset game_state to the last move made
            self.game_state = copy.deepcopy(self.history[-2])
            del self.history[-1]
            self.engine.undo = False
            return None


# Main loop
if __name__ == "__main__":
    game = Game((800, 600))
    game.new_game()
    #game.game_state = test_states.state_maker(test_states.stalemate_test)
    #game.game_state.whose_turn = "white"
    #game.player_list = [players.Human("white"), players.Human("black")]

    while not game.engine.done:
        while not game.game_state.game_over:
            for player in game.player_list:
                if player.colour == game.game_state.whose_turn and not game.game_state.game_over:
                    game.game_state = game.engine.turn(player, game.game_state)
                    # Once move made, save GameState object into history for undos
                    if game.engine.undo:
                        game.undo()
                    else:
                        game.history.append(copy.deepcopy(game.game_state))
                if game.engine.done:
                    # game.engine.done is a kill signal- as soon as this is True, window 
                    # should close.
                    print("Window closed. Exiting...")
                    game.game_state.game_over = True
                    break
    
    game.engine.close()
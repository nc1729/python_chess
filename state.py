import pieces
import moves
import copy
from typing import List

class GameState:
    """A GameState object contains all the information necessary to encode the 
    state of a game of chess."""
    def __init__(self, piece_list, whose_turn="white"):
        self.piece_list = piece_list
        self.pieces_by_position = dict(zip([piece.position 
                                for piece in self.piece_list], self.piece_list))
        self.captured_pieces = []
        self.whose_turn = whose_turn
        self.move_history = []
        self.can_castle = {"white": {"o-o": True, "o-o-o": True},
                           "black": {"o-o": True, "o-o-o": True}}
        self.possible_moves = {"white": all_possible_moves(self, "white"),
                               "black": all_possible_moves(self, "black")}
        self.can_castle = can_castle(self)
        self.legal_moves = {"white": all_legal_moves(self, "white"),
                            "black": all_legal_moves(self, "black")}
        self.game_over = False
    
    def __str__(self):
        output_string = "Game state dump\n"
        # Print piece list
        output_string += "---Piece list---\n"
        piece_list_string = ""
        for piece in self.piece_list:
            piece_list_string += (piece.colour + " " + piece.name + " at " + moves.square_str(piece.position) + 
                                ", moved={}".format(piece.moved) + "\n")
        output_string += piece_list_string
        # Print whose turn it is
        output_string += "---Whose turn---\n"
        output_string += self.whose_turn
        # Print captured pieces
        output_string += "\n---Captured pieces---\n"
        piece_list_string = ""
        for piece in self.captured_pieces:
            piece_list_string += (piece.colour + " " + piece.name + "\n")
        output_string += piece_list_string
        # Print castle status
        output_string += "---Castle status---\n"
        castle_string = "white, o-o: {}, white, o-o-o: {} ".format(self.can_castle["white"]["o-o"], self.can_castle["white"]["o-o-o"])
        castle_string += "black, o-o: {}, black, o-o-o: {}\n".format(self.can_castle["black"]["o-o"], self.can_castle["black"]["o-o-o"])
        output_string += castle_string
        # Print check status
        output_string += "---Check status---\n"
        if in_check(self, "white"):
            if in_checkmate(self, "white"):
                output_string += "White is in checkmate.\n"
            else:
                output_string += "White is in check.\n"
        elif in_check(self, "black"):
            if in_checkmate(self, "black"):
                output_string += "Black is in checkmate.\n"
            else:
                output_string += "Black is in check.\n"
        elif in_stalemate(self, "white"):
            output_string += "White is in stalemate.\n"
        elif in_stalemate(self, "black"):
            output_string += "Black is in stalemate.\n"
        else:
            output_string += "Normal.\n"
        # Print move list
        output_string += "---Moves made---\n"
        move_history_string = ""
        for move in self.move_history:
            move_history_string += (str(move) +"\n")
        output_string += move_history_string
        # Print all 'possible' moves for white
        output_string += "---'Possible' moves for white---\n"
        possible_move_list_string = ""
        for move in self.possible_moves["white"]:
            possible_move_list_string += (str(move) + "\n")
        output_string += possible_move_list_string
        # Print all legal moves for white
        output_string += "---Possible legal moves for white---\n"
        legal_move_list_string = ""
        for move in self.legal_moves["white"]:
            legal_move_list_string += (str(move) + "\n")
        output_string += legal_move_list_string
        # Print all 'possible' moves for black
        output_string += "---'Possible' moves for black---\n"
        possible_move_list_string = ""
        for move in self.possible_moves["black"]:
            possible_move_list_string += (str(move) + "\n")
        output_string += possible_move_list_string
        # Print all legal moves for black
        output_string += "---Possible legal moves for black---\n"
        legal_move_list_string = ""
        for move in self.legal_moves["black"]:
            legal_move_list_string += (str(move) + "\n")
        output_string += legal_move_list_string
        # Print game_over status
        output_string += "Game over: {}".format(self.game_over)

        return output_string            
    

def update_state(game_state: GameState) -> GameState:
    """This method should be run before every turn to make sure
    game state data is up to date."""
    game_state.pieces_by_position = dict(zip([piece.position 
                            for piece in game_state.piece_list], game_state.piece_list))
    game_state.possible_moves = {"white": all_possible_moves(game_state, "white"),
                                 "black": all_possible_moves(game_state, "black")}
    game_state.can_castle = can_castle(game_state)
    game_state.legal_moves = {"white": all_legal_moves(game_state, "white"),
                              "black": all_legal_moves(game_state, "black")}
    return game_state
    
def all_possible_moves(game_state, colour):
    """This method runs through all pieces of a given colour and returns a list 
    of all possible Move objects, whether they're legal or not."""
    move_list = []
    pieces = []
    if colour == "white":
        pieces = [piece for piece in game_state.piece_list if piece.colour == "white"]
        for piece in pieces:
            move_list += piece.possible_moves(game_state)
        return move_list
    elif colour == "black":
        pieces = [piece for piece in game_state.piece_list if piece.colour == "black"]
        for piece in pieces:
            move_list += piece.possible_moves(game_state)
        return move_list
    else:
        raise ValueError("Given colour must be white or black.")

def all_legal_moves(game_state, colour):
    """This method run through all pieces of a given colour and returns a list of
    all legal moves."""
    possible_moves_list = game_state.possible_moves[colour]
    legal_moves_list = []
    for move in possible_moves_list:
        if valid_move(game_state, move, colour):
            legal_moves_list.append(move)
    return legal_moves_list   

def can_castle(game_state):
    """This method checks whether white or black can castle, and returns
    a dictionary of the form

    {"white": {"o-o": bool, "o-o-o": bool}, "black": {"o-o": bool, "o-o-o": bool}}

    The king and a given rook can castle if and only if:
    1. The king hasn't moved
    2. The rook hasn't moved
    3. There are no pieces, allied or enemy, between the king and the rook
    4. The king isn't in check
    5. The two spaces the king will move through during the castle are not threatened.
    
    Conditions 4 and 5 is checked by the valid_move function. All other conditions are
    checked here."""

    can_castle = {"white": {"o-o": False, "o-o-o": False}, 
                  "black": {"o-o": False, "o-o-o": False}}

    colours = ("white", "black")
    for colour in colours:
        ### Find king
        king_list = [piece for piece in game_state.piece_list if str(piece) == "K" 
                    and piece.colour == colour and piece.moved == False]

        if len(king_list) == 0:
            # Condition 1 - the king has moved
            can_castle[colour]["o-o"] = False
            can_castle[colour]["o-o-o"] = False
            continue
        
        ### Find rooks
        rook_list = [piece for piece in game_state.piece_list if str(piece) == "R"
                    and piece.colour == colour and piece.moved == False]
        back_rank = 0 if colour == "white" else 7
        queenside_rook = game_state.pieces_by_position.get((0, back_rank))
        kingside_rook = game_state.pieces_by_position.get((7, back_rank))

        if len(rook_list) == 0:
            # Condition 2 - rooks have moved (or have been captured)
            can_castle[colour]["o-o"] = False
            can_castle[colour]["o-o-o"] = False
            continue

        # Check queenside castling:
        if queenside_rook:
            # Condition 3 - are there pieces in between the king and the rook?
            condition3 = not (game_state.pieces_by_position.get((1, back_rank))
                or game_state.pieces_by_position.get((2, back_rank))
                or game_state.pieces_by_position.get((3, back_rank)))
            if condition3:
                can_castle[colour]["o-o-o"] = True
            else:
                can_castle[colour]["o-o-o"] = False
        else:
            # No suitable queenside rook
            can_castle[colour]["o-o-o"] = False
        
        # Check kingside castling:
        if kingside_rook:
            # Condition 3 - are there pieces in between the king and the rook?
            condition3 = not (game_state.pieces_by_position.get((5, back_rank))
                or game_state.pieces_by_position.get((6, back_rank)))
            if condition3:
                can_castle[colour]["o-o"] = True
            else:
                can_castle[colour]["o-o"] = False
        else:
            # No suitable kingside rook
            can_castle[colour]["o-o"] = False
    
    return can_castle

def in_check(game_state, colour):
    """This method checks whether a King of a given colour is in check."""
    
    # Find king
    king_list = [piece for piece in game_state.piece_list if str(piece) == "K" and piece.colour == colour]
    # No kings failsafe- will never happen in normal games
    if len(king_list) == 0:
        # can't be in check if there's no king...
        return False
    else:
        king = king_list[0] 
    
    # Get the opposing side's colour
    if colour == "white":
        other_colour = "black"
    elif colour == "black":
        other_colour = "white"
    else:
        raise ValueError("Given colour must be white or black.")

    # Check all the possible enemy moves (disregarding whether they'd be in check) 
    # and see if they can capture the king
    for enemy_move in game_state.possible_moves[other_colour]:
        if enemy_move.new_position == king.position:
            return True
    return False

def valid_move(game_state, move, colour):
    """This method a given Move produces a valid GameState when applied
    to the given GameState.
    Regarding castling: conditions 4 and 5, as explained in the function 
    can_castle, is dealt with here."""
    
    # Make temporary copy of GameState object for testing
    test_state = copy.deepcopy(game_state)
            
    # Get the opposing side's colour
    if colour == "white":
        other_colour = "black"
    elif colour == "black":
        other_colour = "white"
    else:
        raise ValueError("Given colour must be white or black.")

    # Apply move to GameState
    test_state = move.apply_move(test_state)

    # Update relevant GameState metadata
    test_state.pieces_by_position = dict(zip([piece.position 
                            for piece in test_state.piece_list], test_state.piece_list))
    test_state.possible_moves = {"white": all_possible_moves(test_state, "white"),
                                 "black": all_possible_moves(test_state, "black")}
    test_state.can_castle = can_castle(test_state)

    # Find possible squares the enemy can move to
    enemy_squares = [move.new_position for move in test_state.possible_moves[other_colour]]
    
    # Find king
    king_list = [piece for piece in test_state.piece_list if str(piece) == "K" and piece.colour == colour]
    # No kings failsafe- will never happen in normal games
    if len(king_list) == 0:
        # no friendly king - no need to worry about checking for check.
        # Given move can't be a Castle either, so no need to worry about that
        return True
    else:
        king = king_list[0]
    
    # Deal with castling (conditions 1 and 5) here
    if move.move_type == "Castle":
        back_rank = 0 if colour == "white" else 7
        if in_check(game_state, colour):
            # condition 1 - can't castle if king is in check
            return False
        if move.old_rook_position[0] == 0:
            # Queenside castle
            king_movement_squares = [(2, back_rank), (3, back_rank)]
            for square in king_movement_squares:
                if square in enemy_squares:
                    # Condition 5 - castling now would result in the king
                    # passing through danger
                    return False
        if move.old_rook_position[0] == 7:
            # Kingside castle
            king_movement_squares = [(5, back_rank), (6, back_rank)]
            for square in king_movement_squares:
                if square in enemy_squares:
                    # Condition 5 - castling now would result in the king
                    # passing through danger
                    return False

    # Check all the possible enemy squares and see if they can capture the king
    for square in enemy_squares:
        if square == king.position:
            # Allied king will be in check after this move, so move is invalid
            del test_state
            return False
    
    del test_state
    return True

def in_checkmate(game_state, colour):
    """This method checks whether a King of a given colour is in checkmate."""
    if len(game_state.legal_moves[colour]) == 0:
        # King must be in check too, but in_checkmate will only be called if in_check is True
        return True
    
    # King has at least one legal move, not in checkmate
    return False

def in_stalemate(game_state, colour):
    """This method checks whether a given colour is in stalemate, i.e. they have no
    legal moves to play."""
    piece_names = [piece.name for piece in game_state.piece_list]

    if len(game_state.legal_moves[colour]) == 0:
        # the pieces of this colour have no legal moves
        print(f"{colour.capitalize()} has no legal moves- stalemate!")
        return True
    elif len(piece_names) == 2 and piece_names.count("King") == 2:
        # only kings left on the board
        print("Insufficient material left on board- stalemate!")
        return True
    elif len(piece_names) == 3 and piece_names.count("King") == 2:
        if "Bishop" or "Knight" in piece_names:
            # there's two kings and a bishop/knight on the board; it's a draw by insufficient material
            print("Insufficient material left on board- stalemate!")
            return True
        else:
            # get rid of this later
            return False
    else:
        # check move history at some point?
        return False

if __name__ == "__main__":
    kingside_castle_test = [pieces.King((4,0), "white"), pieces.King((4,7), "black"),
                            pieces.Rook((7,0), "white"), pieces.Rook((7,7), "black")]
    test_state = GameState(kingside_castle_test)
    print(test_state.can_castle)
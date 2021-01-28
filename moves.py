#!/usr/bin/python

import pieces
import state
import copy


def square_str(position):
    """Gives the chess co-ordinates of a position (i,j)."""

    files = ("a", "b", "c", "d", "e", "f", "g", "h")
    ranks = ("1", "2", "3", "4", "5", "6", "7", "8")

    return files[position[0]] + ranks[position[1]]

class Move:
    def __init__(self, piece, old_position, new_position):
        self.piece = piece
        self.old_position = old_position
        self.new_position = new_position

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def apply_move(self, game_state: state.GameState) -> state.GameState:
        return game_state

class Translation(Move):
    def __init__(self, piece, old_position, new_position):
        super().__init__(piece, old_position, new_position)
        self.move_type = "Translation"

    def __str__(self):
        return str(self.piece) + square_str(self.old_position) + "-" + square_str(self.new_position)
    
    def __repr__(self):
        return str(self)

    def apply_move(self, game_state: state.GameState) -> state.GameState:
        """Return a new GameState object with the Move applied to it."""
        moving_piece = game_state.pieces_by_position[self.old_position]
        
        # Apply move
        moving_piece.position = self.new_position
        moving_piece.moved = True

        # Add to move list
        game_state.move_history.append(self)
      
        return game_state


class PromotionByTranslation(Translation):
    def __init__(self, piece, old_position, new_position, new_piece_name):
        super().__init__(piece, old_position, new_position)
        self.new_piece_name = new_piece_name
        self.move_type = "PromotionByTranslation"

    def __str__(self):
        return (square_str(self.old_position) + "-" + square_str(self.new_position) + "=" + self.new_piece_name)
    
    def __repr__(self):
        return str(self)

    def apply_move(self, game_state: state.GameState) -> state.GameState:
        """Return a new GameState object with the Move applied to it."""
        promoting_piece = game_state.pieces_by_position[self.old_position]

        # Add new piece
        if self.new_piece_name == "Q":
            game_state.piece_list.append(pieces.Queen(self.new_position, self.piece.colour, True))
        elif self.new_piece_name == "R":
            game_state.piece_list.append(pieces.Rook(self.new_position, self.piece.colour, True))
        elif self.new_piece_name == "B":
            game_state.piece_list.append(pieces.Bishop(self.new_position, self.piece.colour, True))
        elif self.new_piece_name == "N":
            game_state.piece_list.append(pieces.Knight(self.new_position, self.piece.colour, True))
        else:
            raise ValueError("Invalid new piece! Promotion routine went wrong- aborting...")

        # Delete old pawn
        game_state.piece_list.remove(promoting_piece)

        # Add to move list
        game_state.move_history.append(self)

        return game_state


class Capture(Move):
    def __init__(self, piece, old_position, new_position, captured_piece):
        super().__init__(piece, old_position, new_position)
        self.captured_piece = captured_piece
        self.move_type = "Capture"

    def __str__(self):
        return (str(self.piece) + square_str(self.old_position) + "x"
                + str(self.captured_piece) + square_str(self.new_position))
    
    def __repr__(self):
        return str(self)

    def apply_move(self, game_state: state.GameState) -> state.GameState:
        """Return a new GameState object with the Move applied to it."""
        attacking_piece = game_state.pieces_by_position[self.old_position]
        captured_piece = game_state.pieces_by_position[self.captured_piece.position]

        # Apply move
        attacking_piece.position = self.new_position
        attacking_piece.moved = True
        game_state.captured_pieces.append(captured_piece)
        game_state.piece_list.remove(captured_piece)

        # Add to move list
        game_state.move_history.append(self)

        return game_state


class PromotionByCapture(Capture):
    def __init__(self, piece, old_position, new_position, captured_piece, new_piece_name):
        super().__init__(piece, old_position, new_position, captured_piece)
        self.new_piece_name = new_piece_name
        self.move_type = "PromotionByCapture"

    def __str__(self):
        return (square_str(self.old_position) + "x" + square_str(self.new_position) + "=" + self.new_piece_name)
    
    def __repr__(self):
        return str(self)

    def apply_move(self, game_state: state.GameState) -> state.GameState:

        promoting_piece = game_state.pieces_by_position[self.old_position]
        captured_piece = game_state.pieces_by_position[self.captured_piece.position]

        # Add new piece
        if self.new_piece_name == "Q":
            game_state.piece_list.append(pieces.Queen(self.new_position, self.piece.colour, True))
        elif self.new_piece_name == "R":
            game_state.piece_list.append(pieces.Rook(self.new_position, self.piece.colour, True))
        elif self.new_piece_name == "B":
            game_state.piece_list.append(pieces.Bishop(self.new_position, self.piece.colour, True))
        elif self.new_piece_name == "N":
            game_state.piece_list.append(pieces.Knight(self.new_position, self.piece.colour, True))
        else:
            raise ValueError("Invalid new piece! Promotion routine went wrong- aborting...")

        # Delete old pawn and captured piece
        game_state.piece_list.remove(promoting_piece)
        game_state.piece_list.remove(captured_piece)

        # Add to move list
        game_state.move_history.append(self)

        return game_state

class EnPassant(Capture):
    def __init__(self, piece, old_position, new_position, captured_piece):
        super().__init__(piece, old_position, new_position, captured_piece)
        self.move_type = "EnPassant"

    def __str__(self):
        return (square_str(self.old_position) + "x" 
                + square_str(self.new_position) + "e.p.")


class Castle(Move):
    def __init__(self, piece, old_position, new_position, rook, old_rook_position, new_rook_position):
        super().__init__(piece, old_position, new_position)
        self.rook = rook
        self.old_rook_position = old_rook_position
        self.new_rook_position = new_rook_position
        self.move_type = "Castle"

    def __str__(self):
        if abs(self.old_rook_position[0] - self.new_rook_position[0]) == 2:
            return "o-o"
        elif abs(self.old_rook_position[0] - self.new_rook_position[0]) == 3:
            return "o-o-o"
    
    def __repr__(self):
        return str(self)

    def apply_move(self, game_state: state.GameState) -> state.GameState:
        # Create state
        king = game_state.pieces_by_position[self.old_position]
        rook = game_state.pieces_by_position[self.old_rook_position]

        # Apply move
        king.position = self.new_position
        rook.position = self.new_rook_position
        king.moved = True
        rook.moved = True

        # Add to move list
        game_state.move_history.append(self)

        return game_state
#!/usr/bin/python3

import moves

class Piece:
    """Class representing a Piece on the board."""
    def __init__(self, position, colour, moved=False):
        self.position = position
        self.colour = colour
        self.moved = moved
        self.path = ""
    
    def __str__(self):
        return ""
    
    def possible_moves(self, game_state):
        return []


class King(Piece):
    def __init__(self, position, colour, moved=False):
        super().__init__(position, colour, moved)
        if self.colour == "white":
            self.path = "pieces/white_king.png"
        elif self.colour == "black":
            self.path = "pieces/black_king.png"
        self.name = "King"
    
    def __str__(self):
        return "K"
    
    def __repr__(self):
        return str(self)
    
    def possible_moves(self, game_state):
        possible_moves = []
        other_pieces = game_state.pieces_by_position
        offsets = [[-1,-1],[-1,0],[-1,1],
                   [0,-1], [0,1],
                   [1,-1], [1,0], [1,1]]
        
        for offset in offsets:
            new_position = (self.position[0] + offset[0], 
                          self.position[1] + offset[1])
            
            # Check if new square is on the board
            if 0 <= new_position[0] <= 7 and 0 <= new_position[1] <= 7:
                if new_position not in other_pieces:
                    # Square is empty, add to possible_moves
                    possible_moves.append(moves.Translation(self, self.position, new_position))
                elif other_pieces[new_position].colour == self.colour:
                    # Square is occupied by friendly piece, can't do anything
                    pass
                else:
                    # Square is occupied by enemy piece, can capture
                    possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
            
        # Handle castling
        can_castle = game_state.can_castle[self.colour]
        if can_castle["o-o"]:
            if self.colour == "white":
                rook = other_pieces.get((7,0))
                if rook and rook.colour == "white":
                    possible_moves.append(moves.Castle(self, self.position, (6,0), rook, rook.position, (5,0)))
            elif self.colour == "black":
                rook = other_pieces.get((7,7))
                if rook and rook.colour == "black":
                    possible_moves.append(moves.Castle(self, self.position, (6,7), rook, rook.position, (5,7)))
        if can_castle["o-o-o"]:
            if self.colour == "white":
                rook = other_pieces.get((0,0))
                if rook and rook.colour == "white":
                    possible_moves.append(moves.Castle(self, self.position, (2,0), rook, rook.position, (3,0)))
            elif self.colour == "black":
                rook = other_pieces.get((0,7))
                if rook and rook.colour == "black":
                    possible_moves.append(moves.Castle(self, self.position, (2,7), rook, rook.position, (3,7)))
            
        return possible_moves

           

class Queen(Piece):
    def __init__(self, position, colour, moved=False):
        super().__init__(position, colour, moved)
        if self.colour == "white":
            self.path = "pieces/white_queen.png"
        elif self.colour == "black":
            self.path = "pieces/black_queen.png"
        self.name = "Queen"
    
    def __str__(self):
        return "Q"
    
    def __repr__(self):
        return str(self)
    
    def possible_moves(self, game_state):
        possible_moves = []
        other_pieces = game_state.pieces_by_position

        # Moving left
        k = 1
        while self.position[0] - k >= 0:
            new_position = self.position[0] - k, self.position[1]
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving right
        k = 1
        while self.position[0] + k <= 7:
            new_position = self.position[0] + k, self.position[1]
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving up
        k = 1
        while self.position[1] + k <= 7:
            new_position = self.position[0], self.position[1] + k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving down
        k = 1
        while self.position[1] - k >= 0:
            new_position = self.position[0], self.position[1] - k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving up-left
        k = 1
        while self.position[0] - k >= 0 and self.position[1] + k <= 7:
            new_position = self.position[0] - k, self.position[1] + k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving up-right
        k = 1
        while self.position[0] + k <= 7 and self.position[1] + k <= 7:
            new_position = self.position[0] + k, self.position[1] + k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving down-left
        k = 1
        while self.position[0] - k >= 0 and self.position[1] - k >= 0:
            new_position = self.position[0] - k, self.position[1] - k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving down-right
        k = 1
        while self.position[0] + k <= 7 and self.position[1] - k >= 0:
            new_position = self.position[0] + k, self.position[1] - k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
            
        return possible_moves


class Rook(Piece):
    def __init__(self, position, colour, moved=False):
        super().__init__(position, colour, moved)
        if self.colour == "white":
            self.path = "pieces/white_rook.png"
        elif self.colour == "black":
            self.path = "pieces/black_rook.png"
        self.name = "Rook"
    
    def __str__(self):
        return "R"
    
    def __repr__(self):
        return str(self)
    
    def possible_moves(self, game_state):
        possible_moves = []
        other_pieces = game_state.pieces_by_position

        # Moving left
        k = 1
        while self.position[0] - k >= 0:
            new_position = self.position[0] - k, self.position[1]
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving right
        k = 1
        while self.position[0] + k <= 7:
            new_position = self.position[0] + k, self.position[1]
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving up
        k = 1
        while self.position[1] + k <= 7:
            new_position = self.position[0], self.position[1] + k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving down
        k = 1
        while self.position[1] - k >= 0:
            new_position = self.position[0], self.position[1] - k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
            
        return possible_moves


class Bishop(Piece):
    def __init__(self, position, colour, moved=False):
        super().__init__(position, colour, moved)
        if self.colour == "white":
            self.path = "pieces/white_bishop.png"
        elif self.colour == "black":
            self.path = "pieces/black_bishop.png"
        self.name = "Bishop"
    
    def __str__(self):
        return "B"
    
    def __repr__(self):
        return str(self)
    
    def possible_moves(self, game_state):
        possible_moves = []
        other_pieces = game_state.pieces_by_position
        
        # Moving up-left
        k = 1
        while self.position[0] - k >= 0 and self.position[1] + k <= 7:
            new_position = self.position[0] - k, self.position[1] + k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving up-right
        k = 1
        while self.position[0] + k <= 7 and self.position[1] + k <= 7:
            new_position = self.position[0] + k, self.position[1] + k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving down-left
        k = 1
        while self.position[0] - k >= 0 and self.position[1] - k >= 0:
            new_position = self.position[0] - k, self.position[1] - k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
        
        # Moving down-right
        k = 1
        while self.position[0] + k <= 7 and self.position[1] - k >= 0:
            new_position = self.position[0] + k, self.position[1] - k
            if new_position not in other_pieces:
                # Square is empty, add to possible_moves
                possible_moves.append(moves.Translation(self, self.position, new_position))
                k += 1
            elif other_pieces[new_position].colour == self.colour:
                # Square is occupied by friendly piece, stop
                break
            else:
                # Square is occupied by enemy piece, can capture
                possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))
                break
            
        return possible_moves
    

class Knight(Piece):
    def __init__(self, position, colour, moved=False):
        super().__init__(position, colour, moved)
        if self.colour == "white":
            self.path = "pieces/white_knight.png"
        elif self.colour == "black":
            self.path = "pieces/black_knight.png"
        self.name = "Knight"
    
    def __str__(self):
        return "N"
    
    def __repr__(self):
        return str(self)
    
    def possible_moves(self, game_state):
        possible_moves = []
        other_pieces = game_state.pieces_by_position

        offsets = [[-2, -1], [-2, 1],
                   [-1, -2], [-1, 2],
                   [1, -2], [1, 2],
                   [2, -1], [2, 1]]
        
        for offset in offsets:
            new_position = (self.position[0] + offset[0],
                          self.position[1] + offset[1])
            
            # check if new square is on the board...
            if 0 <= new_position[0] <= 7 and 0 <= new_position[1] <= 7:
                if new_position not in other_pieces:
                    # Square is empty, add to possible_moves
                    possible_moves.append(moves.Translation(self, self.position, new_position))
                elif other_pieces[new_position].colour == self.colour:
                    # Square is occupied by friendly piece, do nothing
                    pass
                else:
                    # Square is occupied by enemy piece, can capture
                    possible_moves.append(moves.Capture(self, self.position, new_position, other_pieces[new_position]))

        return possible_moves
    

class Pawn(Piece):
    def __init__(self, position, colour, moved=False):
        super().__init__(position, colour, moved)
        if self.colour == "white":
            self.path = "pieces/white_pawn.png"
        elif self.colour == "black":
            self.path = "pieces/black_pawn.png"
        self.name = "Pawn"
    
    def __str__(self):
        return ""
    
    def __repr__(self):
        return str(self)
    
    def possible_moves(self, game_state):
        possible_moves = []
        other_pieces = game_state.pieces_by_position

        if self.colour == "white":
            # can only move upwards
            if self.moved:
                possible_squares = [(self.position[0], self.position[1] + 1)]
                for square in possible_squares:
                    if not (0 <= square[0] <= 7 and 0 <= square[1] <= 7):
                        # Square not on board, can't go further
                        break
                    elif square not in other_pieces:
                        # Space is empty, add to possible_moves
                        possible_moves.append(moves.Translation(self, self.position, square))
                    elif other_pieces[square].colour == self.colour:
                        # Space is occupied by friendly piece, stop
                        break
                    else:
                        # Space is occupied by enemy piece, stop
                        break
            else:
                possible_squares = [(self.position[0], self.position[1] + 1),
                                    (self.position[0], self.position[1] + 2)]
                for square in possible_squares:
                    if not (0 <= square[0] <= 7 and 0 <= square[1] <= 7):
                        # Square not on board, can't go further
                        break
                    elif square not in other_pieces:
                        # Space is empty, add to possible_moves
                        possible_moves.append(moves.Translation(self, self.position, square))
                    elif other_pieces[square].colour == self.colour:
                        # Space is occupied by friendly piece, stop
                        break
                    else:
                        # Space is occupied by enemy piece, stop
                        break
            
            # now deal with standard captures
            possible_capture_squares = [(self.position[0] - 1, self.position[1] + 1),
                                        (self.position[0] + 1, self.position[1] + 1)]
            for square in possible_capture_squares:
                # if square is on the board...
                if 0 <= square[0] <= 7 and 0 <= square[1] <= 7:
                    # if square is occupied by an enemy piece
                    if square in other_pieces and other_pieces[square].colour != self.colour:
                        possible_moves.append(moves.Capture(self, self.position, square, other_pieces[square]))
            
            # now deal with en passant
            # we make sure we have a last made move; i.e. this isn't the first turn
            if len(game_state.move_history) > 0:
                if self.position[1] == 4:
                    # white pawn must be on its fifth rank
                    adjacent_squares = [(self.position[0] - 1, self.position[1]),
                                        (self.position[0] + 1, self.position[1])]
                    last_move_made = game_state.move_history[-1]
                    # need to check:
                    # - the last move was a pawn double move
                    # - into an adjacent square
                    conditions = (isinstance(last_move_made, moves.Translation) and
                                isinstance(last_move_made.piece, Pawn) and
                                last_move_made.piece.position in adjacent_squares and
                                abs(last_move_made.old_position[1] - last_move_made.new_position[1]) == 2)
                    if conditions:
                        square = (last_move_made.piece.position[0], last_move_made.piece.position[1] + 1)
                        possible_moves.append(moves.EnPassant(self, self.position, square, last_move_made.piece)) 
        else:
            # handle black pawns- they can only move down
            if self.moved:
                possible_squares = [(self.position[0], self.position[1] - 1)]
                for square in possible_squares:
                    if not (0 <= square[0] <= 7 and 0 <= square[1] <= 7):
                        # Square not on board, can't go further
                        break
                    elif square not in other_pieces:
                        # Space is empty, add to possible_moves
                        possible_moves.append(moves.Translation(self, self.position, square))
                    elif other_pieces[square].colour == self.colour:
                        # Space is occupied by friendly piece, stop
                        break
                    else:
                        # Space is occupied by enemy piece, stop
                        break
            else:
                possible_squares = [(self.position[0], self.position[1] - 1),
                                    (self.position[0], self.position[1] - 2)]
                for square in possible_squares:
                    if not (0 <= square[0] <= 7 and 0 <= square[1] <= 7):
                        # Square not on board, can't go further
                        break
                    elif square not in other_pieces:
                        # Space is empty, add to possible_moves
                        possible_moves.append(moves.Translation(self, self.position, square))
                    elif other_pieces[square].colour == self.colour:
                        # Space is occupied by friendly piece, stop
                        break
                    else:
                        # Space is occupied by enemy piece, stop
                        break
            
            # now deal with standard captures
            possible_capture_squares = [(self.position[0] - 1, self.position[1] - 1),
                                        (self.position[0] + 1, self.position[1] - 1)]
            for square in possible_capture_squares:
                # if square is on the board...
                if 0 <= square[0] <= 7 and 0 <= square[1] <= 7:
                    # if square is occupied by an enemy piece
                    if square in other_pieces and other_pieces[square].colour != self.colour:
                        possible_moves.append(moves.Capture(self, self.position, square, other_pieces[square]))
            
            # now deal with en passant
            # we make sure we have a last made move; i.e. this isn't the first turn
            if len(game_state.move_history) > 0:
                if self.position[1] == 3:
                    # black pawn must be on its fifth rank
                    adjacent_squares = [(self.position[0] - 1, self.position[1]),
                                        (self.position[0] + 1, self.position[1])]
                    last_move_made = game_state.move_history[-1]
                    # need to check:
                    # - the last move was a pawn double move
                    # - into an adjacent square
                    conditions = (isinstance(last_move_made, moves.Translation) and
                                isinstance(last_move_made.piece, Pawn) and
                                last_move_made.piece.position in adjacent_squares and
                                abs(last_move_made.old_position[1] - last_move_made.new_position[1]) == 2)
                    if conditions:
                        square = (last_move_made.piece.position[0], last_move_made.piece.position[1] - 1)
                        possible_moves.append(moves.EnPassant(self, self.position, square, other_pieces[square]))
            
        return possible_moves
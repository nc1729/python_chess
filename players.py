import pygame
import random
import moves

class Player:
    def __init__(self, colour):
        self.colour = colour
        self.score = 0


class Human(Player):
    def __init__(self, colour):
        super().__init__(colour)
        self.my_turn = False
    
    def promotion_handler(self, move):
        """Before move is applied to a GameState, the promotion handler
        checks if the move was a Pawn move and if the Pawn moved to its back rank.
        If it did, the move is replaced by a Promotion move."""
        back_rank = 7 if move.piece.colour == "white" else 0
        if move.piece.name == "Pawn" and move.new_position[1] == back_rank:
            # Pawn just moved to back rank - promote it
            new_piece_name = ""
            print("Promote your pawn!")
            print("Press Q for a Queen, R for a Rook,")
            print("B for a Bishop or N for a Knight.")
            while not new_piece_name:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return None
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            new_piece_name = 'Q'
                        elif event.key == pygame.K_r:
                            new_piece_name = 'R'
                        elif event.key == pygame.K_b:
                            new_piece_name = 'B'
                        elif event.key == pygame.K_n:
                            new_piece_name = 'N'

            if move.move_type == "Translation":
                new_move = moves.PromotionByTranslation(move.piece, move.old_position,
                                                        move.new_position, new_piece_name)
                return new_move
            elif move.move_type == "Capture":
                new_move = moves.PromotionByCapture(move.piece, move.old_position,
                                                    move.new_position, move.captured_piece,
                                                    new_piece_name)
                return new_move
        else:
            # No promotion detected; return move
            return move


class AI(Player):
    def __init__(self, colour, mode):
        super().__init__(colour)
        self.my_turn = False
        self.mode = mode # difficulty, personality etc?
    
    def promotion_handler(self, move):
        back_rank = 7 if move.piece.colour == "white" else 0
        if move.piece.name == "Pawn" and move.new_position[1] == back_rank:
            # Pawn just moved to back rank, promote it
            if self.mode == "random":
                choice = random.randrange(0, 4)
                if choice == 0:
                    new_piece_name = 'Q'
                elif choice == 1:
                    new_piece_name = 'R'
                elif choice == 2:
                    new_piece_name = 'B'
                elif choice == 3:
                    new_piece_name = 'N'
            
            if move.move_type == "Translation":
                new_move = moves.PromotionByTranslation(move.piece, move.old_position,
                                                        move.new_position, new_piece_name)
                return new_move
            elif move.move_type == "Capture":
                new_move = moves.PromotionByCapture(move.piece, move.old_position,
                                                    move.new_position, move.captured_piece,
                                                    new_piece_name)
                return new_move
        else:
            # No promotion detected; return move
            return move

            

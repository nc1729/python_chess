import pieces
import state
import moves

def state_maker(piece_list):
    output_state = state.GameState([])
    output_state.piece_list = piece_list
    output_state.pieces_by_position = dict(zip([piece.position 
                                for piece in output_state.piece_list], 
                                output_state.piece_list))
    output_state.captured_pieces = []
    output_state.whose_turn = "white"
    output_state.can_castle = state.can_castle(output_state)
    output_state.move_history = []

    return output_state   

new_game_pieces = [pieces.Rook((0,7), "black"),
                   pieces.Knight((1,7), "black"),
                   pieces.Bishop((2,7), "black"),
                   pieces.Queen((3,7), "black"),
                   pieces.King((4,7), "black"),
                   pieces.Bishop((5,7), "black"),
                   pieces.Knight((6,7), "black"),
                   pieces.Rook((7,7), "black"),
                   pieces.Pawn((0,6), "black"),
                   pieces.Pawn((1,6), "black"),
                   pieces.Pawn((2,6), "black"),
                   pieces.Pawn((3,6), "black"),
                   pieces.Pawn((4,6), "black"),
                   pieces.Pawn((5,6), "black"),
                   pieces.Pawn((6,6), "black"),
                   pieces.Pawn((7,6), "black"),
                   pieces.Pawn((0,1), "white"),
                   pieces.Pawn((1,1), "white"),
                   pieces.Pawn((2,1), "white"),
                   pieces.Pawn((3,1), "white"),
                   pieces.Pawn((4,1), "white"),
                   pieces.Pawn((5,1), "white"),
                   pieces.Pawn((6,1), "white"),
                   pieces.Pawn((7,1), "white"),
                   pieces.Rook((0,0), "white"),
                   pieces.Knight((1,0), "white"),
                   pieces.Bishop((2,0), "white"),
                   pieces.Queen((3,0), "white"),
                   pieces.King((4,0), "white"),
                   pieces.Bishop((5,0), "white"),
                   pieces.Knight((6,0), "white"),
                   pieces.Rook((7,0), "white")]
queen_test_pieces = [pieces.Queen((3,3), "white")]
knight_test_pieces = [pieces.Knight((2,2), "white")]
check_test1_pieces = [pieces.King((0,7), "white"), 
                      pieces.Knight((3,4), "white"), 
                      pieces.Queen((7,0), "black"),
                      pieces.King((5,0), "black")]
pawn_test = [pieces.Pawn((0,6), "black"),
             pieces.Pawn((1,6), "black"),
             pieces.Pawn((2,6), "black"),
             pieces.Pawn((3,6), "black"),
             pieces.Pawn((4,6), "black"),
             pieces.Pawn((5,6), "black"),
             pieces.Pawn((6,6), "black"),
             pieces.Pawn((7,6), "black"),
             pieces.Pawn((0,1), "white"),
             pieces.Pawn((1,1), "white"),
             pieces.Pawn((2,1), "white"),
             pieces.Pawn((3,1), "white"),
             pieces.Pawn((4,1), "white"),
             pieces.Pawn((5,1), "white"),
             pieces.Pawn((6,1), "white"),
             pieces.Pawn((7,1), "white")]
pawn_test_with_kings = [pieces.Pawn((0,6), "black"),
                        pieces.Pawn((1,6), "black"),
                        pieces.Pawn((2,6), "black"),
                        pieces.Pawn((3,6), "black"),
                        pieces.Pawn((4,6), "black"),
                        pieces.Pawn((5,6), "black"),
                        pieces.Pawn((6,6), "black"),
                        pieces.Pawn((7,6), "black"),
                        pieces.Pawn((0,1), "white"),
                        pieces.Pawn((1,1), "white"),
                        pieces.Pawn((2,1), "white"),
                        pieces.Pawn((3,1), "white"),
                        pieces.Pawn((4,1), "white"),
                        pieces.Pawn((5,1), "white"),
                        pieces.Pawn((6,1), "white"),
                        pieces.Pawn((7,1), "white"),
                        pieces.King((4,7), "black"),
                        pieces.King((4,0), "white")]
king_queen_and_king = [pieces.King((2,1), "white"), pieces.Queen((5,0), "white"), pieces.King((1,4), "black")]
two_kings = [pieces.King((3,3), "white"), pieces.King((5,3), "black")]
castle_test = [pieces.King((4,0), "white"), pieces.Rook((0,0), "white"), pieces.Rook((7,0), "white"),
               pieces.King((4,7), "black"), pieces.Rook((0,7), "black"), pieces.Rook((7,7), "black")]
castle_test_black = [pieces.King((4,0), "white"), pieces.King((4,7), "black"),
                     pieces.Rook((0,7), "black"), pieces.Rook((7,7), "black")]
promotion_test = [pieces.King((4,0), "white", True), pieces.Pawn((4,6), "white", True),
                  pieces.King((0,7), "black", True)]
stalemate_test = [pieces.King((0,5), "white", True), pieces.Bishop((1,5), "white", True), pieces.King((0,7), "black", True)]

if __name__ == "__main__":
    test_state = state_maker(castle_test_black)
    print(state.can_castle(test_state))
#!/usr/bin/python3

import pygame
import os
import players
import moves
import state
import random
import time

pygame.init()

class GfxEngine:
    """The Engine object handles the graphics. All drawing functions are 
    contained here."""
    def __init__(self, resolution):
        # Graphics constants
        self.resolution = resolution
        self.board_size = (resolution[1], resolution[1])
        self.square_size = self.board_size[0] // 8
        self.square_palette = {"light": (255, 248, 220),
                               "dark": (244, 164, 96),
                               "light_highlighted": (144, 238, 144),
                               "dark_highlighted": (34, 139, 34),
                               "threatened": (128, 0, 0),
                               "selected": (166, 198, 255)}

        # Image variables
        self.image_library = {}

        # Pygame objects
        self.screen = pygame.display.set_mode(self.resolution)
        self.board = pygame.Surface(self.board_size)
        self.clock = pygame.time.Clock()

        # UI variables - used to pass information from the Game object
        # to the engine (when a piece is clicked for example)
        self.piece_selected = None
        self.game_over = False
        # Undo flag to pass to game to retrieve earlier states
        self.undo = False
        # Game might be over, but might want to keep program open-
        # done = True will kill the program completely
        self.done = False

    def load_image(self, path):
        """load_image takes a path and loads the corresponding image.
        If image has been loaded already, load_image just returns it rather
        than loading again."""
        image = self.image_library.get(path)
        if image is None:
            # first make path work in Windows or Linux by replacing back/forward
            # slashes as necessary
            canonicalised_path = path.replace('/', os.sep).replace('\\', os.sep)

            # load image
            image = pygame.image.load(canonicalised_path).convert()

            # get rid of the pink, make it transparent
            image.set_colorkey((255, 0, 255))

            # scale as necessary and add image to image_library
            image = pygame.transform.scale(image, (self.square_size,
                                                   self.square_size))
            self.image_library[path] = image
            return image
        else:
            return image
    
    def draw_square(self, position, colour):
        """draw_square draws a square of length square_size and given
        colour at position (i,j) (in chess co-ords, (0,0) == a1 and (7,7) == h8) 
        onto the board."""
        i = position[0]
        j = 7 - position[1]
        pygame.draw.rect(self.board, colour, (i * self.square_size, j * self.square_size,
                                              self.square_size, self.square_size))
    
    def draw_piece(self, piece):
        """draw_piece draws a given piece onto the board."""
        image = self.load_image(piece.path)
        i = piece.position[0]
        j = 7 - piece.position[1]

        self.board.blit(image, (i * self.square_size, j * self.square_size))
    

    def draw_board(self, game_state):
        """draw_board takes a GameState object and redraws the board to match,
        along with any selected piece and its possible moves."""
        # Clear board
        self.board = pygame.Surface(self.board_size)

        # Draw all squares
        for i in range(8):
                for j in range(8):
                    if (i + 7 - j) % 2 == 0:
                        # Square is white
                        self.draw_square((i,j), self.square_palette["light"])
                    else:
                        # Square is black
                        self.draw_square((i,j), self.square_palette["dark"])
        
        # If piece selected, redraw piece's square and possible squares
        # it can move to. Then draw all pieces
        if self.piece_selected:
            piece = self.piece_selected
            piece_legal_moves = [move for move in game_state.legal_moves[piece.colour]
                                 if move.piece == piece]

            # Draw selected piece's square
            self.draw_square(piece.position, self.square_palette["selected"])

            # Draw the possible moves of the selected piece
            possible_squares = [move.new_position for move in piece_legal_moves]
            for square in possible_squares:
                i, j = square
                if (i + 7 - j) % 2 == 0:
                    # Square is white
                    self.draw_square((i,j), self.square_palette["light_highlighted"])
                else:
                    # Square is black
                    self.draw_square((i,j), self.square_palette["dark_highlighted"])
            
            # Once squares all drawn, draw pieces on top
            for piece in game_state.piece_list:
                self.draw_piece(piece)

        else:
            # No piece selected, just draw all pieces
            for piece in game_state.piece_list:
                self.draw_piece(piece)
    
    def input_handler(self, game_state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_square = (mouse_pos[0] // self.square_size,
                                  7 - mouse_pos[1] // self.square_size)
                if 0 <= clicked_square[0] <= 7 and 0 <= clicked_square[1] <= 7:
                    return clicked_square
                else:
                    # Add menu co-ordinates/functionality here?
                    return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print("Saving game_state to dump.txt")
                    f = open("dump.txt", 'w')
                    f.write(str(game_state))
                    f.close()
                if event.key == pygame.K_u:
                    self.undo = True
                    
    def turn(self, player: players.Player, game_state: state.GameState) -> state.GameState:
        player.my_turn = True
        
        if len([piece for piece in game_state.piece_list if piece.colour == player.colour]) == 0:
            # No friendly pieces on board, end turn immediately
            print(f"No {player.colour} pieces on board, skipping turn...")
            player.my_turn = False
        
        # Update game state and redraw it to screen
        game_state = state.update_state(game_state)
        self.refresh(game_state)
        
        # Check for check, checkmate, stalemate
        if state.in_check(game_state, player.colour):
            if state.in_checkmate(game_state, player.colour):
                print(f"{player.colour.capitalize()} is in checkmate!")
                self.done = True
                clicked_square = None
                player.my_turn = False
                game_state.game_over = True
                time.sleep(5)
                return game_state
            else:
                print(f"{player.colour.capitalize()} is in check!")
        elif state.in_stalemate(game_state, player.colour):
            print(f"{player.colour.capitalize()} is in stalemate!")
            clicked_square = None
            player.my_turn = False
            game_state.game_over = True
            return game_state
        else:
            pass
            #print(f"It's {player.colour}'s turn!")
        
        # Main turn loop
        if isinstance(player, players.Human):
            while player.my_turn:               
                clicked_square = self.input_handler(game_state)
               
                if self.done:
                    # Game has been closed - break out of loop
                    clicked_square = None
                    player.my_turn = False
                    game_state.game_over = True
                    return game_state
                
                if self.undo:
                    # Undo button has been pressed - break out of loop
                    clicked_square = None
                    player.my_turn = False
                    return game_state
                
                if clicked_square:
                    if self.piece_selected:
                        piece = self.piece_selected
                        piece_legal_moves = [move for move in game_state.legal_moves[piece.colour] if move.piece == piece]
                        possible_squares = [move.new_position for move in piece_legal_moves]
                        if clicked_square in possible_squares:
                            # Perform selected move
                            move = [move for move in piece_legal_moves if move.new_position == clicked_square][0]
                            # Check for promotion before applying move
                            move = player.promotion_handler(move)
                            if move is not None:
                                # Apply move, deselect piece, turn is over
                                game_state = move.apply_move(game_state)
                                self.piece_selected = None
                                player.my_turn = False
                                if game_state.whose_turn == "white":
                                    game_state.whose_turn = "black"
                                else:
                                    game_state.whose_turn = "white"
                                self.refresh(game_state)
                                return game_state
                        else:
                            # clicked on other square, deselect piece
                            self.piece_selected = None
                            self.refresh(game_state)
                    else:
                        # was a friendly piece selected?
                        clicked_piece = game_state.pieces_by_position.get(clicked_square)
                        if clicked_piece and clicked_piece.colour == player.colour:
                            # friendly piece selected
                            self.piece_selected = clicked_piece
                            self.refresh(game_state)
                        else:
                            # selected enemy piece or empty square, do nothing
                            self.refresh(game_state)
                else:
                    # didn't click a square, do nothing
                    self.refresh(game_state)

        elif isinstance(player, players.AI):
            mode = player.mode
            colour = player.colour

            if mode == "random":
                # Find all legal moves
                legal_moves = game_state.legal_moves[colour]
                number_of_legal_moves = len(legal_moves)

                # Make a random choice of legal move
                choice = random.randrange(0, number_of_legal_moves)
                move = legal_moves[choice]

                # Check for promotion
                move = player.promotion_handler(move)
                if move is not None:
                    # Apply move, deselect piece, turn is over
                    game_state = move.apply_move(game_state)
                    self.piece_selected = None
                    player.my_turn = False
                    if game_state.whose_turn == "white":
                        game_state.whose_turn = "black"
                    else:
                        game_state.whose_turn = "white"
                    self.refresh(game_state)
                    return game_state
            pass

    def refresh(self, game_state):
        """Redraws the board and updates the Pygame window. Runs every frame."""
        self.draw_board(game_state)
        self.screen.blit(self.board, (0,0)) # top-left corner of board is in top-left
        pygame.display.flip()
        self.clock.tick(30) # Hold at 30FPS
    
    def end_game(self, player, game_state):
        clicked_square = None
        player.my_turn = False
        game_state.game_over = True

    
    def close(self):
        """Exits Pygame cleanly. Call after main loop."""
        pygame.quit()
        os._exit(0)
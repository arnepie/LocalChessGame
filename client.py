import pygame
from network import Network
import copy
pygame.font.init()
n = Network()

# Create the screen
size = (1600, 1200)
rows, columns = 8, 8
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")

player_clicks = []  # List to store cords of player clicks
piece_holding = None  # Variable to keep track of the piece that the user is holding
valid_moves = []  # List of all the valid moves possible


def draw_board(p):
    """
    Function to draw the board and let the user know if they are white or black
    :param p: Number of the client to decide if the user is white or black
    """

    # Define the colors of the squares
    first_color = gray = 128, 128, 128  # RGB color code gray
    second_color = white = 255, 255, 255  # RGB color code white

    pos_y = 100  # Starting Y position

    for i in range(rows):
        # Alternate colors for each row
        first_color = gray if first_color == white else white
        second_color = gray if second_color == white else white

        pos_y += 80  # Increment Y position for the next row
        pos_x = 400  # Reset x position for each row

        # Loop trough each column
        for j in range(int(columns / 2)):
            pos_x += 80  # Increment X position for each column

            # Draw first color square
            pygame.draw.rect(screen, first_color, pygame.Rect(pos_x, pos_y, 80, 80))

            pos_x += 80  # Increment X position for each column

            # Draw second color square
            pygame.draw.rect(screen, second_color, pygame.Rect(pos_x, pos_y, 80, 80))

    # Let the user know if they are white or black
    font = pygame.font.SysFont("comicsans", 40)
    if p % 2 == 0:  # If reminder when dividing by 2 is 0 then user is white
        text = font.render("You are playing white", 1, (255, 255, 255))
    else:  # If reminder when dividing by 2 is 1 then user is black
        text = font.render("You are playing black", 1, (255, 255, 255))
    screen.blit(text, (50, 50))


def load_images():
    """
    Function to load the pieces images
    :return images: Returns a list of all the images of the pieces
    """

    images = []  # Empty list for images
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]  # List of all pieces

    # Load images for each piece and append them to the images list
    for piece in pieces:
        images.append(pygame.image.load("images/" + piece + ".png"))

    return images  # Return the images


def draw_pieces(board):
    """
    Function to draw the piece on the board
    :param board: Current state of the board to know where the pieces need to be drawn
    """

    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]  # List of all pieces

    # Loop through the board and draw the pieces
    for row in board:
        for square in row:
            if square != "---":  # If the square is not empty
                # Get the image for the piece and draw it on the screen
                image = images[pieces.index(square[:2])]
                screen.blit(image, (487 + (row.index(square) * 80), 187 + (board.index(row) * 80)))


def check_move(game, p):
    """
    Function that checks the user's clicks and checks which move the user played
    :param game: game class to get current state of board and the color that is playing
    :param p: Number of the client to decide if the user is white or black
    """

    # Global variables so they don't get reset if player clicks for the second time
    global player_clicks
    global piece_holding
    global valid_moves

    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()  # Getting mouse position
    player_clicks.append(pygame.mouse.get_pos())  # Add mouse position to player clicks list
    if len(player_clicks) == 1:  # If it is the user's first click
        for row in game.board:
            for square in row:
                if (game.white_to_move and square[:1] == "w" and p % 2 == 0) or (not game.white_to_move and square[:1] == "b" and p % 2 == 1):
                    piece_pos_y = 215 + (80 * game.board.index(row))  # Get Y position of piece
                    piece_pos_x = 515 + (80 * row.index(square))  # Get X position of piece

                    # Check if mouse position is on square of piece
                    if piece_pos_x - 40 < mouse_pos_x < piece_pos_x + 40 and piece_pos_y - 40 < mouse_pos_y < piece_pos_y + 40:
                        piece_holding = square  # Set piece_holding to the selected piece
                        # Get valid moves for the selected piece
                        temp_valid_moves, en_passant_target, castling_rook1, castling_rook2 = game.get_valid_moves(piece_holding, game.board)
                        # Filter the moves where you would be in check
                        valid_moves = game.filter_moves_in_check(temp_valid_moves, piece_holding)
        if piece_holding is None:
            player_clicks = []  # If player is not holding a piece, the clicks get reset
            draw_board(p)
            draw_pieces(game.board)
        else:
            try:
                draw_board(p)  # Draw the board
                highlight_selected_piece(piece_holding, game.board)  # Highlight the selected piece
                highlight_possible_moves(valid_moves, en_passant_target, castling_rook1, castling_rook2, game.board)  # Highlight possible moves
                draw_pieces(game.board)  # Draw the pieces
            except:
                pass

    if len(player_clicks) == 2:
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()  # Get mouse position

        # Loop through the board to find the clicked square
        for row_number, row in enumerate(game.board):
            for square_number, square in enumerate(row):
                square_pos_y = 215 + (80 * row_number)  # Y position of the square
                square_pos_x = 515 + (80 * square_number)  # X position of the square

                # Check on which square mouse position is
                if square_pos_x - 40 < mouse_pos_x < square_pos_x + 40 and square_pos_y - 40 < mouse_pos_y < square_pos_y + 40:
                    row_set_index = row_number  # Row index of the selected square
                    square_set_index = square_number  # Square index of the selected square

                    row = game.board[row_set_index]  # Get the row
                    if row[square_set_index] == piece_holding:  # If player clicked the same square
                        player_clicks = []  # Reset player clicks
                        piece_holding = None  # Reset the piece held

                    temp_board = copy.deepcopy(game.board)  # Create a temp board
                    if piece_holding is not None:
                        for find_row_number, find_row in enumerate(temp_board):
                            for find_square_number, find_square in enumerate(find_row):
                                if find_square == piece_holding:
                                    if game.check_for_en_passant(piece_holding, temp_board)[0]:  # Check for en passant
                                        move_changer = -1 if game.white_to_move else 1  # Change in row index for both colors

                                        # En passant
                                        if find_row_number + move_changer == row_set_index and find_square_number + 1 == square_set_index:
                                            temp_board[find_row_number][find_square_number + 1] = "---"
                                        elif find_row_number + move_changer == row_set_index and find_square_number - 1 == square_set_index:
                                            temp_board[find_row_number][find_square_number - 1] = "---"

                                    # Castling
                                    long_castle, short_castle = game.check_for_castling(temp_board, piece_holding[0])  # Check if castling is possible
                                    row = 7 if piece_holding[0] == "w" else 0  # Back row index
                                    if long_castle and row_number == row and square_number == 2 and piece_holding[1] == "K":  # Castling long
                                        temp_board[row][4] = "---"
                                        temp_board[row][0] = "---"
                                        temp_board[row][2] = piece_holding
                                        temp_board[row][3] = f"{piece_holding[0]}R1"
                                    if short_castle and row_number == row and square_number == 6 and piece_holding[1] == "K":  # Castling short
                                        temp_board[row][4] = "---"
                                        temp_board[row][7] = "---"
                                        temp_board[row][6] = piece_holding
                                        temp_board[row][5] = f"{piece_holding[0]}R2"

                                    find_row[find_row.index(piece_holding)] = "---"  # Set original square to empty
                                    temp_board[row_set_index][square_set_index] = piece_holding  # Change square selected to piece selected

                                    # Promotion
                                    back_row = 0 if piece_holding[0] == "w" else 7  # Back row index for promotion
                                    if row_set_index == back_row and piece_holding[1] == "p":
                                        # Ask the user what piece it wants to promote to
                                        promoted_piece = draw_promotion_screen(piece_holding[0])

                                        max_number = 0
                                        for count_row in temp_board:
                                            for count_square in count_row:
                                                if count_square.startswith(piece_holding[0] + promoted_piece):  # Check if the square starts with the piece
                                                    number_str = count_square[-1]  # Get the number from that square
                                                    if number_str.isdigit():
                                                        number = int(number_str)
                                                        max_number = max(max_number, number)  # Update the max number
                                        next_number = max_number + 1  # Next number that isn't already on the board
                                        temp_board[row_set_index][square_set_index] = piece_holding[0] + promoted_piece + str(next_number)  # Change the square to the promoted piece

                                    for move in valid_moves:
                                        if temp_board == move:
                                            if len(game.moves) < 1 or temp_board != game.moves[-1]:
                                                game.moves.append(temp_board)  # Add the temp board to the list of moves
                                                game.white_to_move = not game.white_to_move  # Switch the color to move each turn
                                                game.board = temp_board  # Set the actual board to the temp board
                                                n.send(game.board)  # Send the new board

        player_clicks = []  # Reset player clicks
        piece_holding = None  # Reset the piece holding
        draw_board(p)  # Draw the board
        draw_pieces(game.board)  # Draw the pieces


def highlight_selected_piece(selected_piece, board):
    """
    Function to highlight the piece that is selected by the user
    :param selected_piece: The piece selected by the user to highlight it
    :param board: The current state of the board to check the position of the piece selected
    """

    red = (255, 0, 0)  # RGB color code red

    # Loop through the board and highlight the selected piece in red
    for row_number, row in enumerate(board):
        for square_number, square in enumerate(row):
            if square == selected_piece:
                pygame.draw.rect(screen, red, pygame.Rect(400 + (80 * (square_number + 1)), 100 + (80 * (row_number + 1)), 80, 80))

    pygame.display.flip()  # Update the display


def highlight_possible_moves(possible_moves, en_passant_target, castling_rook1, castling_rook2, board):
    """
    Function to highlight all the possible moves in a position
    :param possible_moves: A list of all the possible moves to highlight them
    :param en_passant_target: Do not highlight the piece taken by the en passant
    :param castling_rook1: Do not highlight the original position of the short castling rook
    :param castling_rook2: Do not highlight the original position of the long castling rook
    :param board: Current state of the board
    """
    transparent_green = (0, 255, 0, 100)  # RGB color code green (128 is for transparency level)
    transparent_surface = pygame.Surface((80, 80), pygame.SRCALPHA)  # Make transparent surface

    # Loop through the board and get the row index and column index of the piece that is being held
    for row_index, row in enumerate(board):
        for col_index, square in enumerate(row):
            if square == piece_holding:
                piece_holding_row = row_index
                piece_holding_square = col_index

    # Loop through possible moves and highlight them in green
    for move in possible_moves:
        for row_number, row in enumerate(move):
            for square_number, square in enumerate(row):
                if square_number == piece_holding_square and row_number == piece_holding_row:  # Prevent that selected square is also highlighted
                    continue
                elif square == en_passant_target:  # Prevent that en passant target is highlighted
                    continue
                elif board[row_number][square_number] == castling_rook1:  # Prevent that the rook from castling short is highlighted
                    continue
                elif board[row_number][square_number] == castling_rook2:  # Prevent that the rook from castling long is highlighted
                    continue
                elif square != board[row_number][square_number]:  # Highlight possible moves
                    pygame.draw.rect(transparent_surface, transparent_green, transparent_surface.get_rect())
                    screen.blit(transparent_surface, (400 + (80 * (square_number + 1)), 100 + (80 * (row_number + 1))))

    pygame.display.flip()  # Update the display


def draw_promotion_screen(color):
    """
    Function to draw a screen to choose which piece to promote to
    :param color:  The color that promoted to know which color the pieces in the screen need to be
    """

    # Create a surface for the promotion options
    surface = pygame.Surface((300, 200))
    surface.fill((255, 255, 255))  # Make the surface white

    promotion_options = ["Q", "R", "B", "N"]  # Option to promote to
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]  # Pieces in order of images list

    x_offset = 0  # Starting x offset

    # Loop through each promotion option
    for option in promotion_options:
        # Get the image for the promotion option and draw it on the surface
        button_image = images[pieces.index(color + option)]
        surface.blit(button_image, (x_offset, 70))
        x_offset += 80  # Increment the x offset

    # Draw the surface on the screen
    screen.blit(surface, (650, 400))
    pygame.display.flip()  # Update the screen

    # Wait for the player to select a promotion option
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()  # Get the mouse position
                if 600 <= mouse_pos_x <= 1000:  # Check if inside surface
                    selected_option_index = (mouse_pos_x - 640) // 80  # Calculate index
                    if 0 <= selected_option_index < len(promotion_options):
                        selected_option = promotion_options[selected_option_index]  # Get the selected option
                        return selected_option  # Return the selected promotion option


def draw_end_screen(message):
    """
    Function that draws a screen when the game is over to let the user know which player won or if it is a draw
    :param message: Draw / the color that won the game
    """

    white = (255, 255, 255)  # RGB color code white
    black = (0, 0, 0)  # RGB color code black
    font = pygame.font.Font(None, 36)  # Define font

    # Draw the background
    pygame.draw.rect(screen, black, pygame.Rect(600, 450, 400, 100))

    # Render the message
    checkmate_text = font.render(message, True, white) if message == "Draw!" else font.render(f"{message} won!", True, white)
    checkmate_rect = checkmate_text.get_rect(center=(800, 500))
    screen.blit(checkmate_text, checkmate_rect)

    pygame.display.flip()  # Update the display


images = load_images()  # Load the piece images
def main(player):
    run = True
    clock = pygame.time.Clock()
    print("You are player", player)

    # Make a second board to detect if game.board has changed
    board = [
            ["bR1", "bN1", "bB1", "bQ1", "bK", "bB2", "bN2", "bR2"],
            ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"],
            ["wR1", "wN1", "wB1", "wQ1", "wK", "wB2", "wN2", "wR2"]]

    while run:
        clock.tick(60)
        try:  # Try to get the game class
            game = n.send("get")
        except:  # If not, cancel the game
            run = False
            print("Couldn't get game")
            break

        color_won = game.check_for_checkmate(game.board)  # Check for checkmate
        game.check_for_draw(game.board, game.white_to_move)  # Check for draw

        # Check if the game has ended
        if game.checkmate:  # If it is checkmate, draw an end screen with the color that has won
            message = color_won
            draw_end_screen(message)
        elif game.draw:  # If it is a draw, draw an end screen with: "Draw!"
            message = "Draw!"
            draw_end_screen(message)

        # If the board has changed, redraw the pieces
        if board != game.board:
            board = game.board
            draw_board(player)
            draw_pieces(board)

        for event in pygame.event.get():  # Handle events
            if event.type == pygame.QUIT:  # If player has quit, stop running
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
                check_move(game, player)  # Check the move of the player

        pygame.display.flip()  # Update the display


def menu():
    run = True
    clock = pygame.time.Clock()
    player = int(n.getP())  # Get the client id

    while run:
        try:  # Try to get the game class
            game = n.send("get")
        except:  # If not, cancel the game
            run = False
            print("Couldn't get game")
            break

        clock.tick(60)
        screen.fill((0, 0, 0))
        if not (game.connected()):  # If both players have not connected yet, waiting for player is rendered
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render("Waiting for Player...", 1, (255, 255, 255), True)
            screen.blit(text, (50, 125))
        else:  # If both players connected, the game starts
            draw_board(player)
            draw_pieces(game.board)
            main(player)

        pygame.display.flip()  # Update the display
        

menu()

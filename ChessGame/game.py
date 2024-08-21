import copy


class GameState:
    def __init__(self, id):
        # Board is a 8x8 2d list, each element in list has 2 characters.
        # The first character represents the color of the piece: 'b' or 'w'.
        # The second character represents the type of the piece: 'R', 'N', 'B', 'Q', 'K' or 'p'.
        # The third character represents which of the multiple pieces of the same type it is.
        # "---" represents an empty space with no piece.
        self.board = [
            ["bR1", "bN1", "bB1", "bQ1", "bK", "bB2", "bN2", "bR2"],
            ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"],
            ["wR1", "wN1", "wB1", "wQ1", "wK", "wB2", "wN2", "wR2"]]
        self.moves = []  # Store all the moves made in the game
        self.white_to_move = True  # Indicates whether it's white's turn to move
        self.checkmate = False  # True if one player is in checkmate
        self.draw = False  # True if the game is drawn
        self.id = id  # Id of the game
        self.ready = False  # Ready if both player are ready to play

    @staticmethod
    def get_rook_moves(piece_selected, board):
        valid_moves = []  # Empty list to store the valid moves in

        for row_index, row in enumerate(board):
            for col_index, square in enumerate(row):
                if square == piece_selected:
                    # Horizontal to the right
                    for j in range(col_index + 1, len(row)):
                        if row[j] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[row_index][j] = piece_selected
                            valid_moves.append(valid_move)
                        elif row[j][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[row_index][j] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

                    # Horizontal to the left
                    for j in range(col_index - 1, -1, -1):
                        if row[j] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[row_index][j] = piece_selected
                            valid_moves.append(valid_move)
                        elif row[j][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[row_index][j] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

                    # Vertical down
                    for i in range(row_index + 1, len(board)):
                        if board[i][col_index] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][col_index] = piece_selected
                            valid_moves.append(valid_move)
                        elif board[i][col_index][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][col_index] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

                    # Vertical up
                    for i in range(row_index - 1, -1, -1):
                        if board[i][col_index] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][col_index] = piece_selected
                            valid_moves.append(valid_move)
                        elif board[i][col_index][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][col_index] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

        return valid_moves  # Return the valid moves

    @staticmethod
    def get_bishop_moves(piece_selected, board):
        valid_moves = []  # Empty list to store the valid moves in

        for row_index, row in enumerate(board):
            for col_index, square in enumerate(row):
                if square == piece_selected:
                    # Diagonal up-left
                    for i, j in zip(range(row_index - 1, -1, -1), range(col_index - 1, -1, -1)):
                        if board[i][j] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                        elif board[i][j][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

                    # Diagonal up-right
                    for i, j in zip(range(row_index - 1, -1, -1), range(col_index + 1, len(board))):
                        if board[i][j] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                        elif board[i][j][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

                    # Diagonal down-left
                    for i, j in zip(range(row_index + 1, len(board)), range(col_index - 1, -1, -1)):
                        if board[i][j] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                        elif board[i][j][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

                    # Diagonal down-right
                    for i, j in zip(range(row_index + 1, len(board)), range(col_index + 1, len(board))):
                        if board[i][j] == "---":  # When empty square, move gets added
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                        elif board[i][j][0] != square[0]:  # When opponents piece, move gets added but no further moves in that direction
                            valid_move = copy.deepcopy(board)
                            valid_move[row_index][row.index(piece_selected)] = "---"
                            valid_move[i][j] = piece_selected
                            valid_moves.append(valid_move)
                            break
                        else:  # When own piece, no further moves in that direction
                            break

        return valid_moves  # Return the valid moves

    @staticmethod
    def get_knight_moves(piece_selected, board):
        valid_moves = []  # Empty list to store the valid moves in

        for row_index, row in enumerate(board):
            for col_index, square in enumerate(row):
                if square == piece_selected:
                    moves = [
                        (row_index - 2, col_index - 1), (row_index - 2, col_index + 1),
                        (row_index - 1, col_index - 2), (row_index - 1, col_index + 2),
                        (row_index + 1, col_index - 2), (row_index + 1, col_index + 2),
                        (row_index + 2, col_index - 1), (row_index + 2, col_index + 1)
                    ]  # All possible knight moves

                    # Loop through the possible knight moves and add the valid moves the valid moves list
                    for move in moves:
                        new_row, new_col = move
                        if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if inside board
                            if board[new_row][new_col] == "---" or board[new_row][new_col][0] != square[0]:  # When empty square or opponents piece, move gets added
                                valid_move = copy.deepcopy(board)
                                valid_move[row_index][col_index] = "---"
                                valid_move[new_row][new_col] = piece_selected
                                valid_moves.append(valid_move)

        return valid_moves  # Return the valid moves

    def get_king_moves(self, piece_selected, board):
        valid_moves = []  # Empty list to store the valid moves in
        castling_rook1 = "None"  # Variable to store the long side castling rook
        castling_rook2 = "None"  # Variable to store the short side castling rook

        for row_index, row in enumerate(board):
            for col_index, square in enumerate(row):
                if square == piece_selected:
                    moves = [
                        (row_index - 1, col_index - 1), (row_index - 1, col_index), (row_index - 1, col_index + 1),
                        (row_index, col_index - 1), (row_index, col_index + 1), (row_index + 1, col_index - 1),
                        (row_index + 1, col_index), (row_index + 1, col_index + 1)
                    ]  # All possible king moves

                    # Loop through the possible king moves and add the valid moves the valid moves list
                    for move in moves:
                        new_row, new_col = move
                        if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if inside board
                            if board[new_row][new_col] == "---" or board[new_row][new_col][0] != square[0]:  # When empty square or opponents piece, move gets added
                                temp_board = copy.deepcopy(board)
                                temp_board[row_index][col_index] = "---"
                                temp_board[new_row][new_col] = piece_selected
                                if not self.is_in_check(temp_board, square[0]):  # Check if king can't be taken by opponents pieces
                                    valid_moves.append(temp_board)

                    long_castle, short_castle = self.check_for_castling(board, piece_selected[0])  # Check if castling is possible
                    row = 7 if piece_selected[0] == "w" else 0  # Back row
                    if long_castle:  # Add long castle move
                        temp_board = copy.deepcopy(board)
                        temp_board[row][4] = "---"
                        temp_board[row][0] = "---"
                        temp_board[row][2] = piece_selected
                        temp_board[row][3] = f"{piece_selected[0]}R1"
                        valid_moves.append(temp_board)
                        castling_rook1 = f"{piece_selected[0]}R1"
                    if short_castle:  # Add short castle move
                        temp_board = copy.deepcopy(board)
                        temp_board[row][4] = "---"
                        temp_board[row][7] = "---"
                        temp_board[row][6] = piece_selected
                        temp_board[row][5] = f"{piece_selected[0]}R2"
                        valid_moves.append(temp_board)
                        castling_rook2 = f"{piece_selected[0]}R2"

        return valid_moves, castling_rook1, castling_rook2  # Return valid moves and castling rooks

    def get_pawn_moves(self, piece_selected, board):
        valid_moves = []  # Empty list to store the valid moves in
        en_passant_target = None  # Variable to store the en passant target

        for row_index, row in enumerate(board):
            for col_index, square in enumerate(row):
                if square == piece_selected:
                    move_changer = -1 if piece_selected[0] == "w" else 1  # # The changer when moving
                    move_changer_start = -2 if piece_selected[0] == "w" else 2  # The changer when moving at the start
                    start_row = 6 if piece_selected[0] == "w" else 1  # Start row
                    opponent_color = "w" if piece_selected[0] == "b" else "b"  # Opponents color
                    back_row = 0 if piece_selected[0] == "w" else 7  # Back row

                    new_row, new_col = (row_index + move_changer, col_index)
                    if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if inside board
                        if board[new_row][new_col] == "---":  # When empty square, move gets added

                            # Promotion
                            if new_row == back_row:  # When piece gets to back row
                                pieces_to_promote_to = ["Q", "R", "B", "N"]  # Pieces player can promote to
                                for piece in pieces_to_promote_to:
                                    max_number = 0  # Reset max number
                                    for count_row in board:
                                        for count_square in count_row:
                                            if count_square.startswith(piece_selected[0] + piece):  # Check if the square starts with the piece
                                                number_str = count_square[-1]  # Get the number from that square
                                                if number_str.isdigit():
                                                    number = int(number_str)
                                                    max_number = max(max_number, number)  # Update the max number

                                    next_number = max_number + 1  # Define the next number that isn't already on the board
                                    temp_board = copy.deepcopy(board)
                                    temp_board[row_index][col_index] = "---"
                                    temp_board[new_row][new_col] = piece_selected[0] + piece + str(next_number)
                                    valid_moves.append(temp_board)

                            else:  # If piece is not at back row
                                temp_board = copy.deepcopy(board)
                                temp_board[row_index][col_index] = "---"
                                temp_board[new_row][new_col] = piece_selected
                                valid_moves.append(temp_board)

                    # Capturing
                    squares_to_check = [(row_index + move_changer, col_index + 1),
                                        (row_index + move_changer, col_index - 1)]  # Capture squares
                    for check_square in squares_to_check:  # Check if pawn can capture
                        new_row, new_col = check_square
                        if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if inside board
                            if board[new_row][new_col][0] == opponent_color:  # If opponents color, move gets added

                                # Promotion
                                if new_row == back_row:  # When piece gets to back row
                                    pieces_to_promote_to = ["Q", "R", "B", "N"]  # Pieces player can promote to
                                    for piece in pieces_to_promote_to:
                                        max_number = 0  # Reset max number
                                        for count_row in board:
                                            for count_square in count_row:
                                                if count_square.startswith(piece_selected[0] + piece):  # Check if the square starts with the piece
                                                    number_str = count_square[-1]  # Get the number from that square
                                                    if number_str.isdigit():
                                                        number = int(number_str)
                                                        max_number = max(max_number, number)  # Update the max number

                                        next_number = max_number + 1  # Define the next number that isn't already on the board
                                        temp_board = copy.deepcopy(board)
                                        temp_board[row_index][col_index] = "---"
                                        temp_board[new_row][new_col] = piece_selected[0] + piece + str(next_number)
                                        valid_moves.append(temp_board)
                                else:  # If piece is not at back row
                                    temp_board = copy.deepcopy(board)
                                    temp_board[row_index][col_index] = "---"
                                    temp_board[new_row][new_col] = piece_selected
                                    valid_moves.append(temp_board)

                    if row_index == start_row:  # If still on starting square, pawn can move two squares
                        if board[row_index + move_changer_start][col_index] == "---" and board[row_index + move_changer][col_index] == "---":  # When empty square, move gets added
                            temp_board = copy.deepcopy(board)
                            temp_board[row_index][col_index] = "---"
                            temp_board[row_index + move_changer_start][col_index] = piece_selected
                            valid_moves.append(temp_board)

                    en_passant, temp_board, en_passant_target = self.check_for_en_passant(piece_selected, board)  # Check for en passant
                    if en_passant:  # If en passant, add to the valid moves
                        valid_moves.append(temp_board)

        return valid_moves, en_passant_target  # Return valid moves and en passant target

    def get_valid_moves(self, piece_selected, board):
        valid_moves = []  # Empty list to store the valid moves in
        en_passant_target = None  # Variable to store the en passant target
        castling_rook1 = "None"  # Variable to store the long side castling rook
        castling_rook2 = "None"  # Variable to store the short side castling rook

        # Rook and queen valid moves
        if piece_selected[1] == "R" or piece_selected[1] == "Q":
            valid_moves_rook = self.get_rook_moves(piece_selected, board)
            valid_moves.extend(valid_moves_rook)

        # Bishop and queen valid moves
        if piece_selected[1] == "B" or piece_selected[1] == "Q":
            valid_moves_bishop = self.get_bishop_moves(piece_selected, board)
            valid_moves.extend(valid_moves_bishop)

        # Knight valid moves
        if piece_selected[1] == "N":
            valid_moves_knight = self.get_knight_moves(piece_selected, board)
            valid_moves.extend(valid_moves_knight)

        # King valid moves
        if piece_selected[1] == "K":
            valid_moves_king, castling_rook1, castling_rook2 = self.get_king_moves(piece_selected, board)
            valid_moves.extend(valid_moves_king)

        # Pawn valid moves
        if piece_selected[1] == "p":
            valid_moves_pawn, en_passant_target = self.get_pawn_moves(piece_selected, board)
            valid_moves.extend(valid_moves_pawn)

        return valid_moves, en_passant_target, castling_rook1, castling_rook2  # Return the valid moves

    def filter_moves_in_check(self, valid_moves, piece_selected):
        valid_moves = [move for move in valid_moves if not self.is_in_check(move, piece_selected[0])]  # Remove the moves where the king would be in check
        return valid_moves  # Return the new valid moves

    def is_in_check(self, board, color):
        king_position = None  # Set the kings position to None
        for row_index, row in enumerate(board):
            for col_index, square in enumerate(row):
                if square[0] == color and square[1] == "K":  # Find kings position
                    king_position = (row_index, col_index)

        if not king_position:  # Return false if there is no king position (to prevent bugs)
            return False

        opponent_color = "w" if color == "b" else "b"  # Define opponents color

        pieces_to_check = [piece for row in board for piece in row if piece[0] == opponent_color]  # Make list for pieces to check

        # Loop through all the pieces to check if they can capture the king
        for piece in pieces_to_check:
            if piece[1] == "K":  # If piece is king check for possible moves but don't check for checks
                valid_moves = []  # Empty list to store the valid moves in
                for row_index, row in enumerate(board):
                    for col_index, square in enumerate(row):
                        if square == piece:
                            moves = [
                                (row_index - 1, col_index - 1), (row_index - 1, col_index),
                                (row_index - 1, col_index + 1),
                                (row_index, col_index - 1), (row_index, col_index + 1), (row_index + 1, col_index - 1),
                                (row_index + 1, col_index), (row_index + 1, col_index + 1)
                            ]  # All possible king moves

                            for move in moves:
                                new_row, new_col = move
                                if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if inside board
                                    if board[new_row][new_col] == "---" or board[new_row][new_col][0] != square[0]:  # When empty square or opponents piece, move gets added
                                        temp_board = copy.deepcopy(board)
                                        temp_board[row_index][col_index] = "---"
                                        temp_board[new_row][new_col] = piece
                                        valid_moves.append(temp_board)
            else:
                valid_moves = self.get_valid_moves(piece, board)[0]  # Check valid moves for the piece

            for move in valid_moves:
                if move[king_position[0]][king_position[1]] == piece:  # When piece can take king, return True
                    return True
        return False  # When no pieces can take king, return False

    def check_for_checkmate(self, board):
        valid_moves_white = self.get_valid_moves("wK", self.board)[0]  # Check valid moves of white king
        valid_moves_black = self.get_valid_moves("bK", self.board)[0]  # Check valid moves of black king

        if not valid_moves_white and self.is_in_check(board, "w"):  # If white king has no moves and is in check, possible checkmate
            pieces_to_check = [piece for row in board for piece in row if piece[0] == "w" and piece[1] != "K"]  # White pieces without king

            # Loop through all the pieces to check and check if they have a move that avoids checkmate
            for piece in pieces_to_check:
                valid_moves_piece = self.get_valid_moves(piece, board)[0]
                for move in valid_moves_piece:
                    if not self.is_in_check(move, "w"):
                        break  # If a move avoids check, no checkmate
                else:
                    continue  # Continue to the next piece if no move found that avoids check
                break  # If a move avoids check, no checkmate

            else:
                self.checkmate = True  # No move found that avoids check, it is checkmate
                return "Black"  # Black won

        elif not valid_moves_black and self.is_in_check(board, "b"):  # If black king has no moves and is in check, possible checkmate
            pieces_to_check = [piece for row in board for piece in row if piece[0] == "b" and piece[1] != "K"]  # Black pieces without king

            # Loop through all the pieces to check and check if they have a move that avoids checkmate
            for piece in pieces_to_check:
                valid_moves_piece = self.get_valid_moves(piece, board)[0]
                for move in valid_moves_piece:
                    if not self.is_in_check(move, "b"):
                        break  # If a move avoids check, no checkmate
                else:
                    continue  # Continue to the next piece if no move found that avoids check
                break  # If a move avoids check, no checkmate

            else:
                self.checkmate = True  # No move found that avoids check, it is checkmate
                return "White"  # White won

        return None  # Noone won

    def check_for_draw(self, board, white_to_move):
        pieces_to_check_white = [piece for row in board for piece in row if piece[0] == "w"]  # White pieces
        pieces_to_check_black = [piece for row in board for piece in row if piece[0] == "b"]  # Black pieces

        pieces_to_check = pieces_to_check_white if white_to_move else pieces_to_check_black  # Define pieces to check for the color to move

        # Loop through all the pieces to check and check if they have a valid move
        for piece in pieces_to_check:
            valid_moves_piece = self.get_valid_moves(piece, board)[0]  # Get the valid moves of the pieces
            if valid_moves_piece:
                valid_moves_piece_filtered = self.filter_moves_in_check(valid_moves_piece, piece)  # Filter valid moves of the pieces
                if valid_moves_piece_filtered:  # If a valid move is found, break out of the loop
                    break
        else:  # If no move is found
            color = "w" if white_to_move else "b"  # Define the color
            if not self.is_in_check(board, color):  # If king is not in check
                self.draw = True
                return True

        # Check if there are enough pieces to checkmate
        if len(pieces_to_check_white) <= 2 and len(pieces_to_check_black) <= 2:
            # Check if white has enough pieces to checkmate
            draw_white = True if len(pieces_to_check_white) == 1 or any(piece[1] in {"N", "B"} for piece in pieces_to_check_white) else False
            # Check if black has enough pieces to checkmate
            draw_black = True if len(pieces_to_check_black) == 1 or any(piece[1] in {"N", "B"} for piece in pieces_to_check_black) else False

            if draw_white and draw_black:  # If white and black don't have enough pieces to checkmate, it is a draw
                self.draw = True
                return True

        # Check if a position has happened three times
        for move in self.moves:
            times_happened = self.moves.count(move)  # Count how much the position has happened
            if times_happened == 3:  # If it has happened three times, it is a draw
                self.draw = True
                return True

        self.draw = False
        return False

    def check_for_en_passant(self, piece_selected, board):
        move_changer = -1 if piece_selected[0] == "w" else 1  # The changer to row index for both colors
        start_row_opponent = 1 if piece_selected[0] == "w" else 6  # Start row opponent
        opponent_color = "w" if piece_selected[0] == "b" else "b"  # Opponents color
        en_passant_row = 3 if piece_selected[0] == "w" else 4  # The row where a pawn can take en passant

        if len(self.moves) > 3 and piece_selected[1] == "p":  # If more than three moves are taken and the piece selected is a pawn
            for row_index, row in enumerate(board):
                for col_index, square in enumerate(row):
                    if square == piece_selected:
                        # Check if en passant is legal
                        if row_index == en_passant_row:
                            # En passant to the right
                            if col_index < 7 and self.moves[-2][start_row_opponent][col_index + 1] == board[en_passant_row][col_index + 1] and board[en_passant_row][col_index + 1][0] == opponent_color:
                                temp_board = copy.deepcopy(board)
                                temp_board[row_index][col_index] = "---"
                                temp_board[en_passant_row][col_index + 1] = "---"
                                temp_board[row_index + move_changer][col_index + 1] = piece_selected

                                return True, temp_board, temp_board[en_passant_row][col_index + 1]  # Return the valid move and the en passant target

                            # En passant to the left
                            if col_index > 0 and self.moves[-2][start_row_opponent][col_index - 1] == board[en_passant_row][col_index - 1] and board[en_passant_row][col_index - 1][0] == opponent_color:  # Check if en passant is legal
                                temp_board = copy.deepcopy(board)
                                temp_board[row_index][col_index] = "---"
                                temp_board[en_passant_row][col_index - 1] = "---"
                                temp_board[row_index + move_changer][col_index - 1] = piece_selected

                                return True, temp_board, temp_board[en_passant_row][col_index - 1]  # Return the valid move and the en passant target

        return False, None, None  # Return no move and no en passant target

    def check_for_castling(self, board, color):
        short_castle = long_castle = True  # Default is set to True
        row = 7 if color == "w" else 0  # Defining back row

        for move in self.moves:
            if move[row][4] != f"{color}K":  # If king has moved in the game, castling is not possible
                short_castle = long_castle = False
            elif move[row][0] != f'{color}R1':  # If rook 1 has moved, castling long is not possible
                long_castle = False
            elif move[row][7] != f"{color}R2":  # If rook 2 has moved, castling short is not possible
                short_castle = False

        # Long castling
        if long_castle and not self.is_in_check(board, color):  # Check if the king is not in check
            squares_to_check = [i for i in range(2, 4)]
            for square in squares_to_check:
                if board[row][square] != "---":  # Check if pieces are in between
                    long_castle = False

                temp_board = copy.deepcopy(board)
                temp_board[row][4] = "---"
                temp_board[row][square] = f"{color}K"
                if self.is_in_check(temp_board, color):  # Check if there are no checks in between
                    long_castle = False
        else:
            long_castle = False

        # Short castling
        if short_castle and not self.is_in_check(board, color):
            squares_to_check = [i for i in range(5, 7)]
            for square in squares_to_check:
                if board[row][square] != "---":  # Check if pieces are in between
                    short_castle = False

                temp_board = copy.deepcopy(board)
                temp_board[row][square] = f"{color}K"
                if self.is_in_check(temp_board, color):  # Check if there are no checks in between
                    short_castle = False
        else:
            short_castle = False

        return long_castle, short_castle  # Return long_castle and short_castle

    def connected(self):
        return self.ready  # Check if both player are ready

    def play(self, move):
        self.board = move  # Make the board the move played
        self.moves.append(move)  # Add the move to the moves list
        self.white_to_move = not self.white_to_move  # Change the color that is playing

from enum import Enum

X_RANGE = range(8)
Y_RANGE = range(8)


class Piece(Enum):
    KING_WHITE = chr(0x2654)
    KING_BLACK = chr(0x265A)
    QUEEN_WHITE = chr(0x2655)
    QUEEN_BLACK = chr(0x265B)
    ROOK_WHITE = chr(0x2656)
    ROOK_BLACK = chr(0x265C)
    BISHOP_WHITE = chr(0x2657)
    BISHOP_BLACK = chr(0x265D)
    KNIGHT_WHITE = chr(0x2658)
    KNIGHT_BLACK = chr(0x265E)
    PAWN_WHITE = chr(0x2659)
    PAWN_BLACK = chr(0x265F)


def setup_text(x, y):
    # set up the board based on the x, y coordinates
    match y:
        # white pieces
        case 0:
            match x:
                case 0:
                    return Piece.ROOK_WHITE
                case 1:
                    return Piece.KNIGHT_WHITE
                case 2:
                    return Piece.BISHOP_WHITE
                case 3:
                    return Piece.QUEEN_WHITE
                case 4:
                    return Piece.KING_WHITE
                case 5:
                    return Piece.BISHOP_WHITE
                case 6:
                    return Piece.KNIGHT_WHITE
                case 7:
                    return Piece.ROOK_WHITE
                case _:
                    raise ValueError("Invalid x coordinate")
        # white pawns
        case 1:
            return Piece.PAWN_WHITE
        # black pawns
        case 6:
            return Piece.PAWN_BLACK
        # black pieces
        case 7:
            match x:
                case 0:
                    return Piece.ROOK_BLACK
                case 1:
                    return Piece.KNIGHT_BLACK
                case 2:
                    return Piece.BISHOP_BLACK
                case 3:
                    return Piece.QUEEN_BLACK
                case 4:
                    return Piece.KING_BLACK
                case 5:
                    return Piece.BISHOP_BLACK
                case 6:
                    return Piece.KNIGHT_BLACK
                case 7:
                    return Piece.ROOK_BLACK
                case _:
                    raise ValueError("Invalid x coordinate")
        case _:
            raise ValueError("Invalid y coordinate")


def is_same_color(piece1, piece2):
    """checks if two pieces are of the same color"""
    if piece1 in [
        Piece.KING_WHITE,
        Piece.QUEEN_WHITE,
        Piece.ROOK_WHITE,
        Piece.BISHOP_WHITE,
        Piece.KNIGHT_WHITE,
        Piece.PAWN_WHITE,
    ]:
        return piece2 in [
            Piece.KING_WHITE,
            Piece.QUEEN_WHITE,
            Piece.ROOK_WHITE,
            Piece.BISHOP_WHITE,
            Piece.KNIGHT_WHITE,
            Piece.PAWN_WHITE,
        ]
    else:
        return piece2 in [
            Piece.KING_BLACK,
            Piece.QUEEN_BLACK,
            Piece.ROOK_BLACK,
            Piece.BISHOP_BLACK,
            Piece.KNIGHT_BLACK,
            Piece.PAWN_BLACK,
        ]

def is_white(piece):
    """checks if a piece is white"""
    return piece in [
        Piece.KING_WHITE,
        Piece.QUEEN_WHITE,
        Piece.ROOK_WHITE,
        Piece.BISHOP_WHITE,
        Piece.KNIGHT_WHITE,
        Piece.PAWN_WHITE,
    ]

def king_valid_moves(x, y):
    """returns the coordinates around a piece, ignoring invalid coordinates"""
    moves = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            moves.append((x + i, y + j))
    return moves

def diagonal(x, y):
    """returns the coordinates of the diagonals of a piece"""
    # returns four diagonals, top left, top right, bottom left, bottom right
    # return the diagonals in a tuple(list, list, list, list)
    top_left = []
    top_right = []
    bottom_left = []
    bottom_right = []
    for i in range(1, 8):
        if x - i >= 0 and y - i >= 0:
            top_left.append((x - i, y - i))
        if x + i < 8 and y - i >= 0:
            top_right.append((x + i, y - i))
        if x - i >= 0 and y + i < 8:
            bottom_left.append((x - i, y + i))
        if x + i < 8 and y + i < 8:
            bottom_right.append((x + i, y + i))
    return top_left, top_right, bottom_left, bottom_right

def axes(x, y):
    """returns the coordinates of the axes of a piece"""
    # returns two axes, horizontal and vertical
    # return the axes in a tuple(list, list)
    up = []
    down = []
    left = []
    right = []
    for i in range(1, 8):
        if y - i >= 0:
            up.append((x, y - i))
        if y + i < 8:
            down.append((x, y + i))
        if x - i >= 0:
            left.append((x - i, y))
        if x + i < 8:
            right.append((x + i, y))
    return up, down, left, right

def check_valid_moves(
    piece: Piece, coor: tuple[int, int], pieces: list[list[Piece]]
) -> list[tuple[int, int]]:
    """gives out the valid moves for each piece"""
    """requires reading all pieces on a board"""
    valid_moves = []

    match piece:
        case Piece.KING_WHITE | Piece.KING_BLACK:
            for c in king_valid_moves(*coor):
                h, v = c
                if (
                    0 <= h < 8 and 0 <= v < 8
                ):  # Ensure the coordinates are within the board limits
                    if pieces[h][v] is None or not is_same_color(piece, pieces[h][v]):
                        valid_moves.append(c)
        case Piece.PAWN_WHITE:
            h, v = coor
            # check if v is at starting position
            if v == 1:
                if pieces[h][v + 1] is None and pieces[h][v + 2] is None:
                    valid_moves.append((h, v + 2))
            if v + 1 < 8 and pieces[h][v + 1] is None:
                valid_moves.append((h, v + 1))
            if (
                h - 1 >= 0
                and v + 1 < 8
                and not is_same_color(piece, pieces[h - 1][v + 1])
                and pieces[h - 1][v + 1] is not None
            ):
                valid_moves.append((h - 1, v + 1))
            if (
                h + 1 < 8
                and v + 1 < 8
                and not is_same_color(piece, pieces[h + 1][v + 1])
                and pieces[h + 1][v + 1] is not None
            ):
                valid_moves.append((h + 1, v + 1))
        case Piece.PAWN_BLACK:
            h, v = coor
            # check if v is at starting position
            if v == 6:
                if pieces[h][v - 1] is None and pieces[h][v - 2] is None:
                    valid_moves.append((h, v - 2))
            if v - 1 >= 0 and pieces[h][v - 1] is None:
                valid_moves.append((h, v - 1))
            if (
                h - 1 >= 0
                and v - 1 >= 0
                and not is_same_color(piece, pieces[h - 1][v - 1])
                and pieces[h - 1][v - 1] is not None
            ):
                valid_moves.append((h - 1, v - 1))
            if (
                h + 1 < 8
                and v - 1 >= 0
                and not is_same_color(piece, pieces[h + 1][v - 1])
                and pieces[h + 1][v - 1] is not None
            ):
                valid_moves.append((h + 1, v - 1))
        case Piece.QUEEN_WHITE | Piece.QUEEN_BLACK:
            h, v = coor
            c = diagonal(h, v) + axes(h, v)
            for li in c:
                for coor in li:
                    if pieces[coor[0]][coor[1]] is None:
                        valid_moves.append(coor)
                    elif not is_same_color(piece, pieces[coor[0]][coor[1]]):
                        valid_moves.append(coor)
                        break
                    else:
                        break
        case Piece.ROOK_WHITE | Piece.ROOK_BLACK:
            h, v = coor
            c = axes(h, v)
            for li in c:
                for coor in li:
                    if pieces[coor[0]][coor[1]] is None:
                        valid_moves.append(coor)
                    elif not is_same_color(piece, pieces[coor[0]][coor[1]]):
                        valid_moves.append(coor)
                        break
                    else:
                        break
        case Piece.BISHOP_WHITE | Piece.BISHOP_BLACK:
            h, v = coor
            c = diagonal(h, v)
            for li in c:
                for coor in li:
                    if pieces[coor[0]][coor[1]] is None:
                        valid_moves.append(coor)
                    elif not is_same_color(piece, pieces[coor[0]][coor[1]]):
                        valid_moves.append(coor)
                        break
                    else:
                        break
        case Piece.KNIGHT_WHITE | Piece.KNIGHT_BLACK:
            h, v = coor
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) == 3:
                        if 0 <= h + i < 8 and 0 <= v + j < 8:
                            if pieces[h + i][v + j] is None or not is_same_color(
                                piece, pieces[h + i][v + j]
                            ):
                                valid_moves.append((h + i, v + j))
        case _:
            pass

    sanitized_moves = set()
    for move in valid_moves:
        if move[0] not in X_RANGE or move[1] not in Y_RANGE:
            continue
        sanitized_moves |= {move}
    print(f"Cur: {coor}, valid: {sanitized_moves}")
    return sanitized_moves

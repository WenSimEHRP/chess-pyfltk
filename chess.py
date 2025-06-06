import fltk
from pieces import Piece, setup_text, check_valid_moves, is_white

CHESS_FONT = 100
fltk.Fl.set_font(CHESS_FONT, "DejaVu Sans")


class Board(fltk.Fl_Group):
    def __init__(self, x, y, w=800, h=800, label=None):
        super().__init__(x, y, w, h, label)
        self.box(fltk.FL_FLAT_BOX)
        self.sqrsiz = 100
        self.end()
        self.valid_moves = []

    def draw(self):
        super().draw()
        color = [215, 0x6D9C5200]
        highlight_color = [3, 3 + 8]
        for y in range(0, self.w(), self.sqrsiz):
            for x in range(0, self.h(), self.sqrsiz):
                c = color[(x + y) // self.sqrsiz % 2]
                fltk.fl_rectf(x, y, self.sqrsiz, self.sqrsiz, c)
        for move in self.valid_moves:
            x, y = move
            c = highlight_color[(x + y) % 2]
            fltk.fl_rectf(x * self.sqrsiz, y * self.sqrsiz, self.sqrsiz, self.sqrsiz, c)


class ChessPiece(fltk.Fl_Box):
    SIZE = 100
    pieces = [[None for _ in range(8)] for _ in range(8)]
    white_turn = True
    ended = False

    def __init__(self, h, v, window):
        self.type = setup_text(h, v)
        super().__init__(
            h * self.SIZE, v * self.SIZE, self.SIZE, self.SIZE, self.type.value
        )
        self.box(fltk.FL_NO_BOX)
        self.labelfont(CHESS_FONT)
        self.labelsize(100)
        self.dx = 0
        self.dy = 0
        self.pos = (h, v)
        ChessPiece.pieces[h][v] = self.type
        self.window = window

    def handle(self, event):
        r = super().handle(event)
        if ChessPiece.white_turn:
            if not is_white(self.type):
                return r
        else:
            if is_white(self.type):
                return r
        match event:
            case fltk.FL_PUSH:
                self.labelsize(150)
                self.dx = fltk.Fl.event_x() - self.x()
                self.dy = fltk.Fl.event_y() - self.y()
                # highlight valid moves
                self.window.refresh_board_pieces()
                self.window.board.valid_moves = check_valid_moves(
                    self.type, self.pos, ChessPiece.pieces
                )
                self.parent().redraw()
                return 1
            case fltk.FL_DRAG:
                x = fltk.Fl.event_x()
                y = fltk.Fl.event_y()
                self.position(x - self.dx, y - self.dy)
                self.parent().redraw()
                return 1
            case fltk.FL_RELEASE:
                self.labelsize(100)
                x = fltk.Fl.event_x() // 100
                y = fltk.Fl.event_y() // 100
                self.window.refresh_board_pieces()
                if (x, y) not in check_valid_moves(
                    self.type, self.pos, ChessPiece.pieces
                ):
                    self.position(self.pos[0] * 100, self.pos[1] * 100)
                else:
                    print(f"Piece released at {x}, {y}")
                    self.position(x * 100, y * 100)
                    # check if piece eats another piece
                    self.window.refresh_board_pieces()
                    if ChessPiece.pieces[x][y] is not None:
                        for piece in self.window.but:
                            if piece.pos == (x, y):
                                piece.hide()
                                print(f"Eating {piece.type}")
                        # check if piece is a king
                        if ChessPiece.pieces[x][y].value in [
                            Piece.KING_BLACK.value,
                            Piece.KING_WHITE.value,
                        ]:
                            fltk.fl_message("King is dead! Game Over!")
                            ChessPiece.ended = True
                            self.window.refresh_board_pieces()
                            return 1
                    self.pos = (x, y)

                    # promotion
                    if (self.type == Piece.PAWN_WHITE and y == 7) or (
                        self.type == Piece.PAWN_BLACK and y == 0
                    ):
                        self.parent().redraw()
                        self.promotion()

                    self.window.refresh_board_pieces()
                    ChessPiece.white_turn = not ChessPiece.white_turn
                    print(f"Is white turn: {ChessPiece.white_turn}")
                self.window.board.valid_moves = []
                self.window.refresh_board_pieces()
                self.parent().redraw()
                return 1
            case _:
                return r

    # check promotion
    def promotion(self):
        # put a fltk dialog first to ask whether to promote to a knight, bishop, rook, or queen
        match fltk.fl_choice("Promote to:", "Queen", "Knight", ""):
            case 0:
                self.type = (
                    Piece.QUEEN_WHITE if is_white(self.type) else Piece.QUEEN_BLACK
                )
            case 1:
                self.type = (
                    Piece.KNIGHT_WHITE if is_white(self.type) else Piece.KNIGHT_BLACK
                )
            case 2:
                fltk.fl_message("Invalid choice. Promoting to Queen")
                self.type = (
                    Piece.QUEEN_WHITE if is_white(self.type) else Piece.QUEEN_BLACK
                )
        self.label(self.type.value)
        self.window.refresh_board_pieces()


class ChessWindow(fltk.Fl_Double_Window):
    def __init__(self, x, y, title):
        super().__init__(x, y, title)
        self.begin()
        self.board = Board(0, 0)
        self.but = tuple(
            ChessPiece(pos_x, pos_y, self) for pos_x in range(8) for pos_y in range(2)
        ) + tuple(
            ChessPiece(pos_x, pos_y, self)
            for pos_x in range(8)
            for pos_y in range(6, 8)
        )
        self.status_bar = fltk.Fl_Box(0, 800, 800, 30, "FL Chess")
        self.end()

    def refresh_board_pieces(self):
        ChessPiece.pieces = [[None for _ in range(8)] for _ in range(8)]
        for piece in self.but:
            # check if piece is eaten
            if piece.visible():
                ChessPiece.pieces[piece.pos[0]][piece.pos[1]] = piece.type
        if not ChessPiece.ended:
            if ChessPiece.white_turn:
                self.status_bar.label("White's turn")
                return
            self.status_bar.label("Black's turn")
            return
        self.status_bar.label("Game Over!")


if __name__ == "__main__":
    w = ChessWindow(800, 830, "FL Chess")
    # w.resizable(w)
    fltk.Fl.scheme("plastic")
    w.show()
    fltk.Fl.run()

import fltk

CHESS_FONT = 100
fltk.Fl.set_font(CHESS_FONT, "DejaVu Sans")

class Pieces:
    class Knight:
        def white():
            return chr(0x2658)

class Board()

class ChessPiece(fltk.Fl_Button):
    SIZE = 100
    def __init__(self, x, y):
        super().__init__(x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE, Pieces.Knight.white())
        self.labelfont(CHESS_FONT)
        c = fltk.FL_DARK3 if ((x + y) % 2 == 1) else fltk.FL_WHITE
        self.color(c)
        self.labelsize(100)

class ChessWindow(fltk.Fl_Window):
    def __init__(self, x, y, title):
        super().__init__(x, y, title)
        self.begin()
        self.but = tuple(
            ChessPiece(i, j)
            for i in range(8)
            for j in range(8)
        )
        self.end()

if __name__ == "__main__":
    w = ChessWindow(800,800, "FL Chess")
    w.resizable(w)
    w.show()
    fltk.Fl.run()

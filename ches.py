from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PySide6.QtGui import QColor, QPalette, QFont

from PySide6.QtCore import Qt
import chess

# board = chess.Board()
# tmp = board.fen()

class ChessBoard(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("PySide6 Chess Board")
        self.setFixedSize(400, 400)
        self.pieces = [['k','♔'],['q','♕'],['r','♖'],['b','♗'],['n','♘'],['p','♙'],
                        ['K','♚'],['Q','♛'],['R','♜'],['B','♝'],['N','♞'],['P','♟']]
        self.piece_dict = dict(self.pieces)
        self.selectpos = None
        self.counter = 0
        self.board = chess.Board()
        self.board_t = None
        self.tmp = self.board.fen()
        self.s = 0
        self.orderdic = {'0':'a','1':'b','2':'c','3':'d',
                         '4':'e','5':'f','6':'g','7':'h'}
        self.num_to_col = {
                1: 'a', 2: 'b', 3: 'c', 4: 'd',
                5: 'e', 6: 'f', 7: 'g', 8: 'h'
                }
        self.create_board()
        
    # def create_board(self):
    #     layout = QGridLayout()
    #     layout.setSpacing(0)  # マスの隙間をなくす
    #     self.setLayout(layout)
    #     self.board_t = self.redesignBoard()
    #     #print(board)

    #     for row in range(8):
    #         for col in range(8):
    #             char = self.board_t[row*8 + col]
    #             label = QLabel(self.piece_dict.get(char, ""))
    #             label.setFixedSize(50, 50)
    #             label.setAlignment(Qt.AlignCenter)

    #             # 白と黒のマスを交互に塗り分ける
    #             if (row + col) % 2 == 0:
    #                 color = QColor(240, 217, 181)  # 明るい色（白マス）
    #             else:
    #                 color = QColor(181, 136, 99)   # 暗い色（黒マス）
                

    #             font = QFont()
    #             font.setPointSize(50)
    #             label.setFont(font)
    #             palette = label.palette()
    #             palette.setColor(QPalette.Window, color)
    #             label.setAutoFillBackground(True)
    #             label.setPalette(palette)

    #             layout.addWidget(label, row, col)
    def create_board(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.labels = []

        self.board_t = self.redesignBoard()

        for row in range(8):
            for col in range(8):
                char = self.board_t[row*8 + col]
                label = QLabel(self.piece_dict.get(char, ""))
                label.setFixedSize(50, 50)
                label.setAlignment(Qt.AlignCenter)

                # 背景色
                color = QColor(240, 217, 181) if (row + col) % 2 == 0 else QColor(181, 136, 99)
                palette = label.palette()
                palette.setColor(QPalette.Window, color)
                label.setAutoFillBackground(True)
                label.setPalette(palette)

                font = QFont()
                font.setPointSize(50)
                label.setFont(font)

                self.layout.addWidget(label, row, col)
                self.labels.append(label)
            
    def update_board(self):
        self.board_t = self.redesignBoard()
        for i, label in enumerate(self.labels):
            char = self.board_t[i]
            label.setText(self.piece_dict.get(char, ""))

    
    def redesignBoard(self):
        # global tmp
        # board = tmp
        board = self.board.fen()
        print(board)
        reBoard = []
        for piece in board:
            skip = 0
            if piece.isdecimal():
                skip = int(piece)
                for _ in range(int(piece)):
                    reBoard.append('*')

            elif piece not in '/':
                reBoard.append(piece)
        
        return reBoard
    
    #駒を動かす関数
    def movepices(self,event):
        self.parent().handle_click(event.x(),event.y())
    
    def handle_click(self,x,y):
        if self.selectpos == None:
            self.selectpos = (x,y)
        else:
            order = str(self.orderdic.get(x//50)) + str((y//50))
            print(order)

            self.selectpos = None
    
    def number_to_letter(self, n):
        return chr(ord('a') + n - 1) 
            
    #マウス座標取得
    def mousePressEvent(self, event):
        self.counter += 1
        x = int(event.position().x())
        y = int(event.position().y())
        #print(f"Clicked at: ({x}, {y})")
        
        # 例えばどのマスがクリックされたか
        col = (x // 50) + 1 # 1マス50pxなので列番号
        row = 9 - (y // 50)  # 行番号
        if self.counter // 2 == 0:
            self.s = self.board_t[8*row+col]
        else:
            s1 = self.number_to_letter(int(col))
            s2 = str(row)
            if self.s.isupper():
                char = str(self.s+s1+s2)
                self.board.push(self.board.parse_san(char))
                print(char)
            else:
                char = str(s1+s2)
                self.board.push(self.board.parse_san(char))
                print(char)
        
        self.update_board()
        #print(f"Grid position: row={row}, col={col}")  
    
             

if __name__ == "__main__":
    app = QApplication([])
    window = ChessBoard()
    window.show()
    app.exec()

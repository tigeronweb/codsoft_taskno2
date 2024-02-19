import tkinter as tk
from tkinter import messagebox
import math


X = 'X'
O = 'O'
EMPTY = None

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        
        self.board = [[EMPTY] * 3 for _ in range(3)]
        self.current_player = X  
        
        self.buttons = [[None] * 3 for _ in range(3)]
        
        self.create_board()
        
    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text="", font=('Comic Sans MS', 40, 'bold'), width=6, height=2,
                                               command=lambda row=i, col=j: self.button_click(row, col),
                                               bg='yellow' if (i+j)%2 == 0 else 'red', fg='black')
                self.buttons[i][j].grid(row=i, column=j)
        
        if self.current_player == O:
            row, col = self.find_best_move()
            self.button_click(row, col)
        
    def button_click(self, row, col):
        if self.board[row][col] is not EMPTY:
            return
        
        self.buttons[row][col].config(text=self.current_player)
        self.board[row][col] = self.current_player
        
        if self.check_winner(self.current_player):
            if self.current_player == O:
                messagebox.showinfo("Winner", "AI wins!")
            else:
                messagebox.showinfo("Winner", "Player wins!")
            self.reset_game()
        elif self.is_board_full():
            messagebox.showinfo("Draw", "It's a draw!")
            self.reset_game()
        else:
            self.current_player = O if self.current_player == X else X
            if self.current_player == O:
                row, col = self.find_best_move()
                self.button_click(row, col)
                
    def check_winner(self, player):
        
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False
    
    def is_board_full(self):
        return all(cell is not EMPTY for row in self.board for cell in row)
    
    def evaluate(self):
        if self.check_winner(X):
            return -1
        elif self.check_winner(O):
            return 1
        else:
            return 0
    
    def minimax(self, depth, is_maximizing):
        score = self.evaluate()
        if score != 0:
            return score

        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] is EMPTY:
                        self.board[row][col] = O
                        score = self.minimax(depth + 1, False)
                        self.board[row][col] = EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] is EMPTY:
                        self.board[row][col] = X
                        score = self.minimax(depth + 1, True)
                        self.board[row][col] = EMPTY
                        best_score = min(score, best_score)
            return best_score
    
    def find_best_move(self):
        best_move = None
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is EMPTY:
                    self.board[row][col] = O
                    score = self.minimax(0, False)
                    self.board[row][col] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move
    
    def reset_game(self):
        self.board = [[EMPTY] * 3 for _ in range(3)]
        self.current_player = X
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        
        self.create_board()

def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

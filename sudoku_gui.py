import tkinter as tk
from tkinter import messagebox
import random
import copy

# ------------------ Sudoku Generator ------------------
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku(difficulty="easy"):
    board = [[0]*9 for _ in range(9)]
    for _ in range(20):
        row, col = random.randint(0,8), random.randint(0,8)
        num = random.randint(1,9)
        if is_valid(board, row, col, num):
            board[row][col] = num

    solve(board)
    puzzle = copy.deepcopy(board)

    empty_cells = {
        "easy": 30,
        "medium": 45,
        "hard": 60
    }[difficulty]

    while empty_cells > 0:
        row, col = random.randint(0,8), random.randint(0,8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            empty_cells -= 1

    return puzzle, board

# ------------------ Main Game GUI ------------------
class SudokuGUI:
    def __init__(self, master, difficulty):
        self.master = master
        self.master.title("Sudoku Game")
        self.cells = [[None]*9 for _ in range(9)]
        self.puzzle = None
        self.solution = None
        self.difficulty = difficulty

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.pack()

        for row in range(9):
            for col in range(9):
                entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=2, pady=2)
                self.cells[row][col] = entry

        controls = tk.Frame(self.master)
        controls.pack(pady=10)

        tk.Button(controls, text="New Game", command=self.new_game).grid(row=0, column=0, padx=5)
        tk.Button(controls, text="Check", command=self.check_solution).grid(row=0, column=1, padx=5)

    def new_game(self):
        self.puzzle, self.solution = generate_sudoku(self.difficulty)
        for row in range(9):
            for col in range(9):
                entry = self.cells[row][col]
                if self.puzzle[row][col] != 0:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(self.puzzle[row][col]))
                    entry.config(state='disabled', disabledforeground='black')
                else:
                    entry.config(state='normal')
                    entry.delete(0, tk.END)

    def check_solution(self):
        for row in range(9):
            for col in range(9):
                entry = self.cells[row][col]
                val = entry.get()
                if val.isdigit():
                    if int(val) != self.solution[row][col]:
                        messagebox.showwarning("Result", "There is a mistake. Try again.")
                        return
                else:
                    messagebox.showinfo("Result", "Please fill in all cells.")
                    return

        messagebox.showinfo("Congratulations!", "Sudoku solved correctly!")

# ------------------ Start Screen ------------------
class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game - Start")
        self.root.geometry("300x200")

        self.difficulty = tk.StringVar(value="easy")

        tk.Label(root, text="Welcome to Sudoku!", font=("Arial", 16)).pack(pady=10)
        tk.Label(root, text="Select difficulty:").pack(pady=5)

        tk.OptionMenu(root, self.difficulty, "easy", "medium", "hard").pack()

        tk.Button(root, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.root.destroy()  # Close start screen
        game_window = tk.Tk()
        SudokuGUI(game_window, self.difficulty.get())
        game_window.mainloop()

# ------------------ Main ------------------
if __name__ == "__main__":
    start_root = tk.Tk()
    app = StartScreen(start_root)
    start_root.mainloop()

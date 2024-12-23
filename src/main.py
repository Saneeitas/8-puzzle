import numpy as np
import random
import tkinter as tk
from tkinter import messagebox, filedialog
import pickle

class Puzzle:
    def __init__(self, initial_state):
        self.state = np.array(initial_state).reshape(3, 3)
        self.move_count = 0  # Initialize move counter

    def display(self):
        return self.state

    def move(self, direction):
        zero_pos = np.argwhere(self.state == 0)[0]
        x, y = zero_pos

        if direction == 'up' and x < 2:
            self.state[x, y], self.state[x + 1, y] = self.state[x + 1, y], self.state[x, y]
        elif direction == 'down' and x > 0:
            self.state[x, y], self.state[x - 1, y] = self.state[x - 1, y], self.state[x, y]
        elif direction == 'left' and y < 2:
            self.state[x, y], self.state[x, y + 1] = self.state[x, y + 1], self.state[x, y]
        elif direction == 'right' and y > 0:
            self.state[x, y], self.state[x, y - 1] = self.state[x, y - 1], self.state[x, y]

        self.move_count += 1  # Increment move counter

    def is_solved(self):
        return np.array_equal(self.state, np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]).reshape(3, 3))

    def randomize(self):
        while True:
            state = np.random.permutation(9)  # Randomly permute numbers 0-8
            if self.is_solvable(state):
                self.state = state.reshape(3, 3)
                break

    def is_solvable(self, state):
        state = state[state != 0]  # Remove zero for counting inversions
        inversions = sum(
            1 for i in range(len(state)) for j in range(i + 1, len(state)) if state[i] > state[j]
        )
        return inversions % 2 == 0

    def save_game(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.state, self.move_count), f)

    def load_game(self, filename):
        with open(filename, 'rb') as f:
            self.state, self.move_count = pickle.load(f)

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Game")
        self.puzzle = Puzzle([1, 2, 3, 4, 5, 6, 0, 7, 8])
        self.puzzle.randomize()
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.master, text='', width=5, height=2,
                                command=lambda i=i, j=j: self.move_tile(i, j))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        self.reset_button = tk.Button(self.master, text='Reset', command=self.reset_game)
        self.reset_button.grid(row=3, column=0)

        self.save_button = tk.Button(self.master, text='Save', command=self.save_game)
        self.save_button.grid(row=3, column=1)

        self.load_button = tk.Button(self.master, text='Load', command=self.load_game)
        self.load_button.grid(row=3, column=2)

        self.score_label = tk.Label(self.master, text='Score: 0')
        self.score_label.grid(row=4, column=0, columnspan=3)

    def move_tile(self, i, j):
        zero_pos = np.argwhere(self.puzzle.state == 0)[0]
        x, y = zero_pos

        if (i == x and abs(j - y) == 1) or (j == y and abs(i - x) == 1):
            if i == x + 1:
                self.puzzle.move('up')
            elif i == x - 1:
                self.puzzle.move('down')
            elif j == y + 1:
                self.puzzle.move('left')
            elif j == y - 1:
                self.puzzle.move('right')

            self.update_display()
            if self.puzzle.is_solved():
                score = self.calculate_score()
                messagebox.showinfo("Congratulations!", f"You've solved the puzzle in {self.puzzle.move_count} moves!\nYour score: {score}")
                self.score_label.config(text=f'Score: {score}')

    def calculate_score(self):
        # Simple scoring: 1000 - (10 * moves)
        return max(0, 1000 - (10 * self.puzzle.move_count))

    def update_display(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=str(self.puzzle.state[i][j]) if self.puzzle.state[i][j] != 0 else '')

    def reset_game(self):
        self.puzzle.randomize()
        self.puzzle.move_count = 0
        self.update_display()
        self.score_label.config(text='Score: 0')

    def save_game(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pkl",
                                                  filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
        if filename:
            self.puzzle.save_game(filename)
            messagebox.showinfo("Game Saved", "Your game has been saved successfully!")

    def load_game(self):
        filename = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])
        if filename:
            self.puzzle.load_game(filename)
            self.update_display()
            self.score_label.config(text=f'Score: {self.calculate_score()}')
            messagebox.showinfo("Game Loaded", "Your game has been loaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
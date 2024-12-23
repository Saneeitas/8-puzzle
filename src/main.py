import numpy as np
import random
import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import time
import os

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

    def save_high_scores(self, scores, filename='high_scores.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(scores, f)

    def load_high_scores(self, filename='high_scores.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                return pickle.load(f)
        return []

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Game")
        self.puzzle = Puzzle([1, 2, 3, 4, 5, 6, 0, 7, 8])
        self.start_time = None
        self.elapsed_time = 0
        self.high_scores = self.puzzle.load_high_scores()
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

        self.timer_label = tk.Label(self.master, text='Time: 0s')
        self.timer_label.grid(row=5, column=0, columnspan=3)

        self.high_scores_button = tk.Button(self.master, text='High Scores', command=self.show_high_scores)
        self.high_scores_button.grid(row=6, column=0, columnspan=3)

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
                elapsed_time = int(time.time() - self.start_time)
                score = self.calculate_score(elapsed_time)
                messagebox.showinfo("Congratulations!", f"You've solved the puzzle in {self.puzzle.move_count} moves and {elapsed_time} seconds!\nYour score: {score}")
                self.update_high_scores(score)
                self.score_label.config(text=f'Score: {score}')
                self.reset_timer()

    def calculate_score(self, elapsed_time):
        # Simple scoring: 1000 - (10 * moves) - (2 * elapsed time)
        return max(0, 1000 - (10 * self.puzzle.move_count) - (2 * elapsed_time))

    def update_display(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=str(self.puzzle.state[i][j]) if self.puzzle.state[i][j] != 0 else '')
        
        # Update timer display
        if self.start_time is not None:
            self.elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f'Time: {self.elapsed_time}s')

    def reset_game(self):
        self.puzzle.randomize()
        self.puzzle.move_count = 0
        self.start_time = time.time()  # Start the timer
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
            self.start_time = time.time()  # Reset the timer
            messagebox.showinfo("Game Loaded", "Your game has been loaded successfully!")

    def update_high_scores(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)  # Sort scores in descending order
        self.high_scores = self.high_scores[:5]  # Keep only the top 5 scores
        self.puzzle.save_high_scores(self.high_scores)  # Save high scores to file

    def show_high_scores(self):
        if not self.high_scores:
            messagebox.showinfo("High Scores", "No high scores yet!")
        else:
            scores = "\n".join(str(s) for s in self.high_scores)
            messagebox.showinfo("High Scores", f"Top Scores:\n{scores}")

    def reset_timer(self):
        self.start_time = None
        self.elapsed_time = 0
        self.timer_label.config(text='Time: 0s')

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
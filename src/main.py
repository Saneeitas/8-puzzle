import numpy as np
import random

class Puzzle:
    def __init__(self, initial_state):
        self.state = np.array(initial_state).reshape(3, 3)
        self.move_count = 0  # Initialize move counter

    def display(self):
        print(self.state)

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
        else:
            print("Invalid move!")
            return
        
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

    def reset(self):
        self.move_count = 0  # Reset move counter
        self.randomize()  # Randomize the puzzle state

    def help(self):
        print("Welcome to the 8-Puzzle Game!")
        print("Instructions:")
        print("1. You can move the empty space (0) using the following commands:")
        print("   - 'up' to move the empty space up")
        print("   - 'down' to move the empty space down")
        print("   - 'left' to move the empty space left")
        print("   - 'right' to move the empty space right")
        print("2. Type 'reset' to restart the game with a new random state.")
        print("3. Type 'quit' to exit the game.")
        print("4. Type 'help' to see this message again.")

if __name__ == "__main__":
    puzzle = Puzzle([1, 2, 3, 4, 5, 6, 0, 7, 8])  # Initial state
    puzzle.randomize()  # Randomize the puzzle state
    puzzle.display()

    puzzle.help()  # Display help instructions

    while True:
        move = input("Enter your move (up, down, left, right), 'reset' to restart, 'help' for instructions, or 'quit' to exit: ").strip().lower()
        if move == 'quit':
            print("Thanks for playing!")
            break
        elif move == 'reset':
            puzzle.reset()  # Reset the game
            puzzle.display()
            continue
        elif move == 'help':
            puzzle.help()  # Display help instructions
            continue
        elif move in ['up', 'down', 'left', 'right']:
            puzzle.move(move)
            puzzle.display()
            if puzzle.is_solved():
                print(f"Congratulations! You've solved the puzzle in {puzzle.move_count} moves!")
                break
        else:
            print("Invalid command! Please enter a valid move or command.")
import numpy as np

class Puzzle:
    def __init__(self, initial_state):
        self.state = np.array(initial_state).reshape(3, 3)

    def display(self):
        print(self.state)

if __name__ == "__main__":
    initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]  # 0 represents the empty space
    puzzle = Puzzle(initial_state)
    puzzle.display()
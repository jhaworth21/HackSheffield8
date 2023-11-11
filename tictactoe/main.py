import enum
import typing
from random import choice

grids = set()
count = 0


class Move(enum.Enum):
    NOT_FILLED = 0
    X = 1  # Computer
    O = 2  # Player


# Always a grid where the computer has just moved, waiting for player
class Grid:
    def __init__(self, grid_values: typing.List[typing.List[Move]]):
        # Grid values is a grid, where the computer has just moved
        self.grid: typing.List[typing.List[Move]] = [row.copy() for row in grid_values]
        self.computer_move()
        print("Computer moved")

    def computer_move(self):
        # Check for winning move or block opponent
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == Move.NOT_FILLED:
                    # Check for winning move
                    self.grid[i][j] = Move.X
                    if self.is_winning_grid():
                        return
                    self.grid[i][j] = Move.NOT_FILLED

                    # Check for blocking move
                    self.grid[i][j] = Move.O
                    if self.is_winning_grid():
                        self.grid[i][j] = Move.X
                        return
                    self.grid[i][j] = Move.NOT_FILLED

        # Take center
        if self.grid[1][1] == Move.NOT_FILLED:
            self.grid[1][1] = Move.X
            return

        # Take a corner
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty_corners = [(i, j) for i, j in corners if self.grid[i][j] == Move.NOT_FILLED]
        if empty_corners:
            i, j = choice(empty_corners)
            self.grid[i][j] = Move.X
            return

        # Take any open space
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == Move.NOT_FILLED:
                    self.grid[i][j] = Move.X
                    return

    def populate_possible_grids(self):
        if self.is_winning_grid():
            return
        new_grids = set()
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == Move.NOT_FILLED:
                    new_grid = Grid(self.grid)
                    new_grid.grid[i][j] = Move.O
                    if new_grid in grids:
                        continue
                    grids.add(new_grid)
                    new_grids.add(new_grid)

        for new_grid in new_grids:
            new_grid.populate_possible_grids()

    def is_winning_grid(self):
        # Check rows
        for row in self.grid:
            if all(cell == Move.X for cell in row):
                return True

        # Check columns
        for col in range(3):
            if all(self.grid[row][col] == Move.X for row in range(3)):
                return True

        # Check diagonals
        if all(self.grid[i][i] == Move.X for i in range(3)):
            return True
        if all(self.grid[i][2 - i] == Move.X for i in range(3)):
            return True

        return False

    def __eq__(self, other):
        return self.grid == other.grid

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.grid))

    def __str__(self):
        output = ""
        for row in self.grid:
            for value in row:
                if value == Move.X:
                    output += "X"
                elif value == Move.O:
                    output += "O"
                else:
                    output += " "
            output += "\n"
        return output


if __name__ == "__main__":
    grid = Grid([[Move.NOT_FILLED for _ in range(3)] for _ in range(3)])
    grid.populate_possible_grids()
    print(len(grids))

    for grid in grids:
        print(grid)

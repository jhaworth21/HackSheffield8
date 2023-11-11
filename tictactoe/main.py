import enum
import typing

grids = []

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
        self.move_grids = []

    def computer_move(self):
        if self.is_winning_grid(Move.X) or self.is_winning_grid(Move.O):
            return
        # 1. Check for a winning move
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == Move.NOT_FILLED:
                    self.grid[i][j] = Move.X
                    if self.is_winning_grid(Move.X):
                        return
                    else:
                        self.grid[i][j] = Move.NOT_FILLED

        # 2. Block opponent if they have a winning move next
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == Move.NOT_FILLED:
                    self.grid[i][j] = Move.O
                    if self.is_winning_grid(Move.O):
                        self.grid[i][j] = Move.X
                        return
                    else:
                        self.grid[i][j] = Move.NOT_FILLED

        # 3. Take the center if it's free
        if self.grid[1][1] == Move.NOT_FILLED:
            self.grid[1][1] = Move.X
            return

        # 4. Take an opposite corner if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for i, j in corners:
            if self.grid[i][j] == Move.O and self.grid[2 - i][2 - j] == Move.NOT_FILLED:
                self.grid[2 - i][2 - j] = Move.X
                return

        # 5. Take any empty corner
        for i, j in corners:
            if self.grid[i][j] == Move.NOT_FILLED:
                self.grid[i][j] = Move.X
                return

        # 6. Take any empty side
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for i, j in sides:
            if self.grid[i][j] == Move.NOT_FILLED:
                self.grid[i][j] = Move.X
                return

    def friendly_hash(self):
        friendly = ""
        for row in self.grid:
            for value in row:
                if value == Move.X:
                    friendly += "X"
                elif value == Move.O:
                    friendly += "O"
                else:
                    friendly += "E"
        return friendly

    def populate_possible_grids(self):
        if self.is_winning_grid(Move.X) or self.is_winning_grid(Move.O):
            return
        new_grids = set()
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == Move.NOT_FILLED:
                    new_grid = Grid(self.grid)
                    new_grid.grid[i][j] = Move.O
                    new_grid.computer_move()
                    if new_grid in grids:
                        self.move_grids.append(grids[grids.index(new_grid)])
                        continue
                    grids.append(new_grid)
                    new_grids.add(new_grid)
                    self.move_grids.append(new_grid)

        for new_grid in new_grids:
            new_grid.populate_possible_grids()

    def is_winning_grid(self, player: Move):
        # Check rows
        for row in self.grid:
            if all(cell == player for cell in row):
                return True

        # Check columns
        for col in range(3):
            if all(self.grid[row][col] == player for row in range(3)):
                return True

        # Check diagonals
        if all(self.grid[i][i] == player for i in range(3)):
            return True
        if all(self.grid[i][2 - i] == player for i in range(3)):
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
                    output += "E"
            output += "\n"
        return output


if __name__ == "__main__":
    grid = Grid([[Move.NOT_FILLED for _ in range(3)] for _ in range(3)])
    grid.populate_possible_grids()
    print(len(grids))

    print(grid.move_grids[4].move_grids[1].move_grids[1].move_grids[1].move_grids[0])

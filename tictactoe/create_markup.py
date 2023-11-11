from main import Grid, Move, grids as all_grids


def run():
    starting_grid = Grid([[Move.NOT_FILLED for _ in range(3)] for _ in range(3)])
    starting_grid.populate_possible_grids()
    all_grids.append(starting_grid)

    for grid in all_grids:
        page_markdown = ""
        page_markdown += "# Tic-Tac-Toe Game Board\n"
        move_cells = 0

        is_winning_grid = False
        if grid.is_winning_grid(Move.X):
            is_winning_grid = True
            page_markdown += "## Result: Computer wins 🤖\n"

        if grid.is_winning_grid(Move.O):
            is_winning_grid = True
            page_markdown += "## Result: You win! 🎉\n"

        if len(grid.move_grids) == 0 and not is_winning_grid:
            page_markdown += "## Result: You drew 🤝\n"

        # Add a table header (assuming a 3x3 grid for tic-tac-toe)
        page_markdown += "|   |   |   |\n"
        page_markdown += "|---|---|---|\n"

        for row in grid.grid:
            page_markdown += "|"
            for cell in row:
                if cell == Move.X:
                    page_markdown += "❌ |"
                elif cell == Move.O:
                    page_markdown += "⭕ |"
                else:
                    if len(grid.move_grids) == 0:
                        # This is a leaf node, e.g. a winning grid
                        page_markdown += "  |"
                    else:
                        next_grid = grid.move_grids[move_cells]
                        page_markdown += f"[🔎]({next_grid.friendly_hash()}.md) |"
                        move_cells += 1
            page_markdown += "\n"

        if len(grid.move_grids) != 0:
            page_markdown += "\nClick on the 🔎 to make a move"

        if len(grid.move_grids) == 0:
            page_markdown += "\n🔄 [Click here](EEEEEEEEE.md) to restart"

        with open(f"grids_markdown/{grid.friendly_hash()}.md", "w", encoding="utf-8") as f:
            f.write(page_markdown)


if __name__ == "__main__":
    run()

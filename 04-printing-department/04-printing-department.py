MAX_ADJACENT_ROLLS = 3
ROLL_OF_PAPER = "@"


def main(content: str):
    grid = content.split("\n")
    row_count = len(grid)
    col_count = len(grid[0])

    def get_adjacent_rolls_count(grid: list[str], row: int, col: int) -> int:
        # If we're on coordinate (0, 0), we need (0, 1), (1, 0), (1, 1)
        # If we're on coordinate (0, 1), we need (0, 0), (0, 2), (1, 0), (1, 1), (1, 2)
        # If we're on coordinate (1, 1), we need (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)
        top_border = max(row - 1, 0)
        bottom_border = min(row + 1, row_count - 1)
        left_border = max(col - 1, 0)
        right_border = min(col + 1, col_count - 1)

        result = 0

        for x in range(left_border, right_border + 1):
            for y in range(top_border, bottom_border + 1):
                if x == col and y == row:
                    continue
                if grid[y][x] == ROLL_OF_PAPER:
                    result += 1
        return result

    total_count = 0
    for row in range(row_count):
        for col in range(col_count):
            item = grid[row][col]
            if (
                item == ROLL_OF_PAPER
                and get_adjacent_rolls_count(grid, row, col) <= MAX_ADJACENT_ROLLS
            ):
                total_count += 1
    print(f"RESULT: {total_count}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

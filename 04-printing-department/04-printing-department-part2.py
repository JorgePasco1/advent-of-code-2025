from copy import deepcopy
import time


MAX_ADJACENT_ROLLS = 3
ROLL_OF_PAPER = "@"
EMPTY_POSITION = "."


def print_grid(grid: list[list[str]]):
    print("\n".join("".join(row) for row in grid))
    print("------------------------------")


def main(content: str):
    grid = [list(row) for row in content.split("\n")]
    row_count = len(grid)
    col_count = len(grid[0])

    def get_adjacent_rolls_count(grid: list[str], row: int, col: int) -> int:
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

    result = 0
    print_grid(grid)
    while True:
        current_iter_count = 0
        new_grid = deepcopy(grid)
        for row in range(row_count):
            for col in range(col_count):
                item = grid[row][col]
                if (
                    item == ROLL_OF_PAPER
                    and get_adjacent_rolls_count(grid, row, col) <= MAX_ADJACENT_ROLLS
                ):
                    current_iter_count += 1
                    new_grid[row][col] = EMPTY_POSITION
        if current_iter_count == 0:
            break
        result += current_iter_count
        grid = new_grid
        print_grid(grid)
        # time.sleep(0.2) # cool visualization

    print(f"RESULT: {result}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

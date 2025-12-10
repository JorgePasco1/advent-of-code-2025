from typing import Literal, Tuple


UPPER_BOUND = 99
LOWER_BOUND = 0
POSITION_COUNT = UPPER_BOUND - LOWER_BOUND + 1
STARTING_POSITION = 50
RIGHT_POSITION_TO_COUNT = 0


def update_position(
    curr: int, direction: Literal["L", "R"], amount: int
) -> Tuple[int, int]:
    """
    Returns new position and how many times it passed through 0
    """
    print("curr, direction, amount", curr, direction, amount)
    result = curr  # 98
    remaining = amount  # 5
    count = 0
    if direction == "R":
        while remaining:
            result += 1
            remaining -=1
            if result > UPPER_BOUND:
                result = LOWER_BOUND
                count += 1
    if direction == "L":
        while remaining:
            result -= 1
            remaining -= 1
            if result == 0:
                count += 1
            if result < LOWER_BOUND:
                result = UPPER_BOUND
    return result, count


def main(content: str):

    instructions = content.split("\n")
    curr_pos = STARTING_POSITION
    result = 0
    for instruction in instructions:
        direction, amount = instruction[0], int(instruction[1:])
        curr_pos, zero_count = update_position(curr_pos, direction, amount)
        result += zero_count
    print("RESULT: ", result)


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    print(update_position(98, "R", 105))
    print(update_position(3, "L", 3))
    # main(raw_content.strip())

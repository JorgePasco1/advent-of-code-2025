UPPER_BOUND = 99
LOWER_BOUND = 0
POSITION_COUNT = UPPER_BOUND - LOWER_BOUND + 1
STARTING_POSITION = 50
RIGHT_POSITION_TO_COUNT = 0


def main(content: str):
    instructions = content.split("\n")
    curr_pos = STARTING_POSITION
    result = 0
    for instruction in instructions:
        direction, amount = instruction[0], int(instruction[1:])
        mult = -1 if direction == "L" else 1
        new_pos = curr_pos + amount * mult
        while new_pos > UPPER_BOUND:
            new_pos = new_pos - POSITION_COUNT
        while new_pos < LOWER_BOUND:
            new_pos = new_pos + POSITION_COUNT
        curr_pos = new_pos
        if curr_pos == RIGHT_POSITION_TO_COUNT:
            result += 1
    print("RESULT", result)


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

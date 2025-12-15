import time

START = "S"
SPLITTER = "^"
BEAM = "|"
EMPTY = "."


def print_diagram(rows: list[str]):
    print("\n".join(["".join(row) for row in rows]))
    print("---------------------")


def main(content: str):
    rows = [list(row) for row in content.split("\n")]
    split_count = 0
    for i in range(len(rows)):
        if i == 0:
            continue
        row = rows[i]
        previous_row = rows[i - 1]

        for j in range(len(row)):
            prev_item = previous_row[j]
            if row[j] == EMPTY and prev_item != SPLITTER:
                row[j] = BEAM if prev_item == START else prev_item
            if row[j] == SPLITTER and previous_row[j] == BEAM:
                row[j - 1] = BEAM
                row[j + 1] = BEAM
                split_count += 1

        # print_diagram(rows)
        # time.sleep(0.05)

    print(f"RESULT: {split_count}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

START = "S"
SPLITTER = "^"


def main(content: str):
    rows = content.split("\n")
    if not rows:
        return

    width = len(rows[0])
    height = len(rows)
    counts = [1 if cell == START else 0 for cell in rows[0]]

    for row_n in range(height):
        next_counts = [0] * width
        current_row_str = rows[row_n]

        for col_n in range(width):
            incoming = counts[col_n]
            if incoming == 0:
                continue

            cell = current_row_str[col_n]

            if cell == SPLITTER:
                next_counts[col_n - 1] += incoming
                next_counts[col_n + 1] += incoming
                continue

            next_counts[col_n] += incoming

        counts = next_counts

    print(f"RESULT: {sum(counts)}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

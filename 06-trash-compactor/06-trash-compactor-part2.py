from math import prod


MULT_OPERATOR = "*"
EMPTY_SPACE = " "


def get_groups(content: str) -> list[list[str]]:
    def get_value_for_row(row: str, idx: int) -> str:
        if idx > len(row) - 1:
            return ""
        return row[idx]

    rows = content.split("\n")
    number_rows = rows[0 : len(rows) - 1]
    operator_row = rows[-1][::-1].split()
    longest_row = max(len(row) for row in number_rows)
    # print(longest_row)
    curr_col = longest_row - 1
    groups = []
    while curr_col >= 0:
        current_group = []
        while True:
            if curr_col < 0:
                break
            row_values = [get_value_for_row(row, curr_col) for row in number_rows]
            if all([rv == EMPTY_SPACE for rv in row_values]):
                curr_col -= 1
                groups.append(current_group)
                break
            num = int("".join(row_values))
            current_group.append(num)
            curr_col -= 1
        if curr_col == -1:
            groups.append(current_group)

    for idx, operator in enumerate(operator_row):
        groups[idx].append(operator)
    print(groups)
    return groups


def main(content: str):
    total = 0
    groups = get_groups(content)
    for group in groups:
        factors = [int(factor) for factor in group[0 : len(group) - 1]]
        operation = group[-1]
        result = prod(factors) if operation == MULT_OPERATOR else sum(factors)
        total += result
    print(f"RESULT: {total}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

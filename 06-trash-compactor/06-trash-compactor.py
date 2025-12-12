from math import prod


MULT_OPERATOR = "*"


def get_groups(content: str) -> list[list[str]]:
    rows = [row.split() for row in content.split("\n")]
    group_count = len(rows[0])
    groups = [[] for _ in range(group_count)]
    for i in range(group_count):
        for row in rows:
            groups[i].append(row[i])
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

DIGITS = 12


def get_max_joltage(bank: str) -> int:
    result = []
    n = len(bank)
    for i, battery in enumerate(bank):
        battery_joltage = int(battery)
        if len(result) == 0:
            result.append(battery_joltage)
            continue

        while result and battery_joltage > result[-1]:
            current_len = len(result)  # 1
            remaining_batteries = n - i - 1  # 13
            has_margin = current_len + remaining_batteries >= DIGITS
            if has_margin:
                result.pop()
            else:
                break
        if len(result) < DIGITS:
            result.append(battery_joltage)

    return int("".join(map(str, result)))


def main(content: str):
    banks = content.split("\n")

    total = 0
    for bank in banks:
        total += get_max_joltage(bank)

    print("RESULT: ", total)


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

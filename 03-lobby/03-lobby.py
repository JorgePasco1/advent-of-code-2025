def get_max_joltage(bank: str) -> int:
    max_ = 0
    second_max = 0
    n = len(bank)

    for i, battery in enumerate(bank):
        battery_joltage = int(battery)
        if battery_joltage > max_ and i < n - 1:
            max_ = battery_joltage
            second_max = 0
            continue
        if battery_joltage > second_max:
            second_max = battery_joltage
    return max_ * 10 + second_max


def main(content: str):
    # TODO: Implement solution
    banks = content.split("\n")

    total = 0
    for bank in banks:
        total += get_max_joltage(bank)

    print("RESULT: ", total)


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

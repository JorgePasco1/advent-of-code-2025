from typing import TypedDict


class Range(TypedDict):
    l: int
    r: int

    @classmethod
    def from_str(cls, str_: str):
        l, r = str_.split("-")
        return cls(l=int(l), r=int(r))


def is_invalid(num: int) -> bool:
    num_str = str(num)
    if len(num_str) % 2 != 0:
        return False
    middle = int(len(num_str) / 2)
    return num_str[0:middle] == num_str[middle:]


def main(content: str):
    result = 0
    ranges = [Range.from_str(range) for range in content.split(",")]
    for rg in ranges:
        for num in range(rg["l"], rg["r"] + 1):
            if is_invalid(num):
                result += num
    print(result)


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

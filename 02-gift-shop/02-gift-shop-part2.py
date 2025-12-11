from typing import List, TypedDict
import textwrap


class Range(TypedDict):
    l: int
    r: int

    @classmethod
    def from_str(cls, str_: str):
        l, r = str_.split("-")
        return cls(l=int(l), r=int(r))


def split_in_n(str_: str, n: int) -> List[List[int]]:
    return textwrap.wrap(str_, n)


def is_invalid(num: int) -> bool:

    num_str = str(num)
    if len(set(num_str)) == 1:
        return True
    for parts in range(2, len(num_str) // 2 + 1):
        if len(num_str) % parts != 0:
            continue
        splitted = split_in_n(num_str, parts)
        if len(set(splitted)) == 1:
            return True
    return False


def main(content: str):
    result = 0
    ranges = [Range.from_str(range) for range in content.split(",")]
    nums = []
    for rg in ranges:
        print(f"Working on {rg["l"]}-{rg["r"]}")
        for num in range(rg["l"], rg["r"] + 1):
            if is_invalid(num):
                result += num
                nums.append(num)
    print(result)
    print(nums)


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

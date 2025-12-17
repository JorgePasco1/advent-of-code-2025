from functools import lru_cache

OUT = "out"
STARTING_POINT = "svr"


def main(content: str):
    mapper = {}
    for line in content.split("\n"):
        key, vals = line.split(":")
        vals = vals.strip().split(" ")
        mapper[key] = vals

    visiting = set()

    @lru_cache(maxsize=None)
    def move_to(key: str, seen_dac: bool = False, seen_fft: bool = False) -> int:
        if key == OUT:
            return 1 if (seen_dac and seen_fft) else 0

        seen_dac = seen_dac or key == "dac"
        seen_fft = seen_fft or key == "fft"

        visiting.add(key)
        try:
            total = 0
            for nxt in mapper[key]:
                total += move_to(nxt, seen_dac, seen_fft)
            return total
        finally:
            visiting.remove(key)

    result = move_to(STARTING_POINT)
    print(result)


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

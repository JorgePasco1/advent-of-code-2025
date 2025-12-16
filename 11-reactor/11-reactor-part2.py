OUT = "out"
STARTING_POINT = "svr"


def move_to(mapper: dict, key: str, path: set[str] | None = None) -> int:
    if path is None:
        path = set()

    if mapper[key][0] == OUT:
        return 1

    if key in path:
        return 0
    path.add(key)

    count = 0
    for next_ in mapper[key]:
        count += move_to(mapper, next_, path)
    return count


def main(content: str):
    mapper = {}
    for line in content.split("\n"):
        key, vals = line.split(":")
        vals = vals.strip().split(" ")
        mapper[key] = vals
    result = move_to(mapper, STARTING_POINT)
    print(f"RESULT: {result}")


if __name__ == "__main__":
    with open("./example-input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

def get_interval_from_str(raw_range: str) -> list[int]:
    left, right = raw_range.split("-")
    return [int(left), int(right)]


def merge(intervals: list[list[int]]) -> list[list[int]]:
    if len(intervals) == 1:
        return intervals

    def _are_overlapping(a: list[int], b: list[int]) -> bool:
        return a[1] >= b[0]

    def _merge(a: list[int], b: list[int]) -> list[int]:
        return [a[0], max(a[1], b[1])]

    intervals.sort()
    merged = []

    for interval in intervals:
        if not merged or not _are_overlapping(merged[-1], interval):
            merged.append(interval)
            continue

        merged[-1] = _merge(merged[-1], interval)
    return merged


def main(content: str):
    raw_intervals, raw_ingredient_ids = content.split("\n\n")
    fresh_intervals = [
        get_interval_from_str(interval) for interval in raw_intervals.split("\n")
    ]
    fresh_intervals = merge(fresh_intervals)
    count = 0
    for interval in fresh_intervals:
        count += interval[1] - interval[0] + 1
    print(f"RESULT: {count}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

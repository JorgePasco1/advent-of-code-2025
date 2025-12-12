import bisect


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
    ingredient_ids = map(int, raw_ingredient_ids.split("\n"))
    count = 0
    for id_ in ingredient_ids:
        range_idx = max(bisect.bisect(fresh_intervals, id_, key=lambda x: x[0]) - 1, 0)
        interval_to_check = fresh_intervals[range_idx]
        if interval_to_check[0] <= id_ <= interval_to_check[1]:
            count += 1
    print(f"RESULT: {count}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

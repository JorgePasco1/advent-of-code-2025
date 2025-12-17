# CAN'T BELIEVE THIS ACTUALLY WORKED LOL https://old.reddit.com/r/adventofcode/comments/1pkje0o/2025_day_12_solutions/nu2eq1c/


def part1(lines):
    shape_areas = {}
    current_shape_idx = 0
    valid_regions = 0

    for line in lines:
        if line.strip().endswith(":"):
            current_shape_idx = int(line[:-1])
            shape_areas[current_shape_idx] = 0

        elif "#" in line:
            shape_areas[current_shape_idx] += line.count("#")

        elif "x" in line:
            raw_dims, raw_counts = line.split(":")
            width, height = map(int, raw_dims.split("x"))
            counts = map(int, raw_counts.split())

            presents_area = sum(
                count * shape_areas[i] for i, count in enumerate(counts)
            )

            if presents_area <= width * height:
                valid_regions += 1

    return valid_regions


print(part1(open("input.txt").read().splitlines()))

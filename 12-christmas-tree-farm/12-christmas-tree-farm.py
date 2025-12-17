from typing import TypedDict
import logging
from ortools.sat.python import cp_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PART_OF_THE_SHAPE = "#"


class Region(TypedDict):
    width: int
    height: int
    present_requirements: list[int]

    @classmethod
    def from_string(cls, string: str):
        dimensions, raw_requirements = string.split(":")
        width, height = [int(num) for num in dimensions.split("x")]
        requirements = [int(num) for num in raw_requirements.strip().split(" ")]
        return cls(width=width, height=height, present_requirements=requirements)


class Shape(TypedDict):
    shape: list[list[str]]
    total_area: int
    id_: int

    @classmethod
    def from_string(cls, string: str, id_: int):
        lines = string.strip().split("\n")
        # Remove the ID line "N:"
        if ":" in lines[0]:
            lines = lines[1:]
        shape = [list(row) for row in lines]
        total_area = sum(
            len([item for item in row if item == PART_OF_THE_SHAPE]) for row in shape
        )
        return cls(shape=shape, total_area=total_area, id_=id_)


def get_orientations(
    base_shape: list[list[str]],
) -> list[tuple[int, int, list[list[str]]]]:
    """
    Generates all unique orientations for a shape.
    Returns list of (width, height, grid).
    """
    forms = []

    def rotate(g):
        return [list(row) for row in zip(*g[::-1])]

    def to_tuple(g):
        return tuple("".join(row) for row in g)

    seen = set()
    current = base_shape

    # Generate 4 rotations
    for _ in range(4):
        t = to_tuple(current)
        if t not in seen:
            seen.add(t)
            forms.append((len(current[0]), len(current), current))
        current = rotate(current)

    # Flip and generate 4 rotations
    current = [row[::-1] for row in base_shape]
    for _ in range(4):
        t = to_tuple(current)
        if t not in seen:
            seen.add(t)
            forms.append((len(current[0]), len(current), current))
        current = rotate(current)

    return forms


def solve_region(region: Region, all_shapes: list[Shape]) -> bool:
    needed_shapes = []
    for idx, count in enumerate(region["present_requirements"]):
        if count > 0:
            needed_shapes.extend([all_shapes[idx]] * count)

    total_area_needed = sum(s["total_area"] for s in needed_shapes)
    region_area = region["width"] * region["height"]

    if total_area_needed > region_area:
        logger.info(
            f"Region {region['width']}x{region['height']}: Area {region_area} < Needed {total_area_needed} -> False"
        )
        return False

    # Precompute orientations for each shape type
    # shape_orientations[shape_id] = list of (w, h, grid)
    shape_orientations = {}
    unique_shape_ids = set(s["id_"] for s in needed_shapes)
    for sid in unique_shape_ids:
        # Find the shape object
        shape_obj = next(s for s in all_shapes if s["id_"] == sid)
        shape_orientations[sid] = get_orientations(shape_obj["shape"])

    # Implement Grid Model for exact covering
    model = cp_model.CpModel()

    # item_vars[(i, r, x, y)] -> bool
    item_vars = {}

    for i, shape in enumerate(needed_shapes):
        sid = shape["id_"]

        # Symmetries pre-calc
        valid_orientations = []
        for r_idx, (w, h, grid) in enumerate(shape_orientations[sid]):
            valid_orientations.append((r_idx, w, h, grid))

        # Create vars
        added_vars = []
        for r_idx, w, h, grid in valid_orientations:
            # Valid positions
            for r in range(region["height"] - h + 1):
                for c in range(region["width"] - w + 1):
                    # Check if fits (always does by range)
                    var = model.NewBoolVar(f"p_{i}_{r_idx}_{r}_{c}")
                    item_vars[(i, r_idx, r, c)] = var
                    added_vars.append(var)

        # Exactly one placement
        model.Add(sum(added_vars) == 1)

    # Disjoint constraints per cell
    # For each cell (r, c), sum of markers <= 1
    # marker(i, r, c) is true if item i covers r,c
    # item i covers r,c if placed at (pr, pc) with rot rn, such that grid[r-pr][c-pc] is '#'

    S_H, S_W = region["height"], region["width"]
    for r in range(S_H):
        for c in range(S_W):
            covered_by = []
            for i, shape in enumerate(needed_shapes):
                sid = shape["id_"]
                for r_idx, (w, h, grid) in enumerate(shape_orientations[sid]):
                    # Check which placements cover (r, c)
                    # Placed at (pr, pc).
                    # Covers if pr <= r < pr+h AND pc <= c < pc+w AND grid[r-pr][c-pc] == '#'
                    # Range of pr: max(0, r - h + 1) to min(r, S_H - h) -> Actually pr is just loop over valid.

                    # Inverse: iterate valid PR, PC for this shape/rot
                    # If it covers r,c add to list

                    # Optimization: Iterate pr, pc relative to r, c
                    # r - h < pr <= r
                    min_pr = max(0, r - h + 1)
                    max_pr = min(
                        r, S_H - h
                    )  # Wait, placement range is bounded by board
                    # Placement (pr, pc) is valid if valid in vars

                    for pr in range(max(0, r - h + 1), r + 1):
                        if pr > S_H - h:
                            continue  # placement out of bounds
                        for pc in range(max(0, c - w + 1), c + 1):
                            if pc > S_W - w:
                                continue

                            if grid[r - pr][c - pc] == PART_OF_THE_SHAPE:
                                if (i, r_idx, pr, pc) in item_vars:
                                    covered_by.append(item_vars[(i, r_idx, pr, pc)])

            if covered_by:
                model.Add(sum(covered_by) <= 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    status = solver.Solve(model)
    return status == cp_model.OPTIMAL or status == cp_model.FEASIBLE


def main(content: str):
    parts = content.split("\n\n")
    shapes, regions = parts[0:-1], parts[-1]
    shapes = [Shape.from_string(shape, idx) for idx, shape in enumerate(shapes)]
    regions = regions.split("\n")
    regions = [Region.from_string(region) for region in regions]

    count = 0
    for i, region in enumerate(regions):
        print(f"Solving region {i} ({region['width']}x{region['height']})...")
        if solve_region(region, shapes):
            print(f"Region {i}: FITS")
            count += 1
        else:
            print(f"Region {i}: DOES NOT FIT")

    print(f"Total fitting regions: {count}")


if __name__ == "__main__":
    import sys

    # Default to example if no arg
    filename = "./input.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename, "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

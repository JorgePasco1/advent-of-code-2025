import sys

# Increase recursion depth for deep flood fills if necessary
sys.setrecursionlimit(200000)


def main(content: str):
    coordinates = [
        tuple(int(num) for num in row.split(",")) for row in content.split("\n")
    ]

    # 1. Coordinate Compression setup
    unique_xs = set()
    unique_ys = set()

    for x, y in coordinates:
        unique_xs.add(x)
        unique_ys.add(y)

    # Add padding to ensure we can surround the shape
    min_x, max_x = min(unique_xs), max(unique_xs)
    min_y, max_y = min(unique_ys), max(unique_ys)

    unique_xs.add(min_x - 1)
    unique_xs.add(max_x + 1)
    unique_ys.add(min_y - 1)
    unique_ys.add(max_y + 1)

    sorted_xs = sorted(list(unique_xs))
    sorted_ys = sorted(list(unique_ys))

    x_map = {val: i for i, val in enumerate(sorted_xs)}
    y_map = {val: i for i, val in enumerate(sorted_ys)}

    # Build compressed grid mapping
    # logical_cols[i] represents x=sorted_xs[i]
    # We also need to represent gaps between sorted_xs[i] and sorted_xs[i+1]

    # We will build a grid where indices map to:
    # Even indices 2*i -> The coordinate sorted_xs[i] itself (width 1)
    # Odd indices 2*i+1 -> The interval (sorted_xs[i]+1, sorted_xs[i+1]-1)

    # Mapping from coordinate to grid column index:
    # coord x (which is in sorted_xs) -> 2 * x_map[x]

    grid_width = 2 * len(sorted_xs) - 1
    grid_height = 2 * len(sorted_ys) - 1

    # Grid values: 0 = Unknown, 1 = Boundary, 2 = Outside
    grid = [[0] * grid_width for _ in range(grid_height)]

    # 2. Draw Boundary
    num_coords = len(coordinates)
    for i in range(num_coords):
        p1 = coordinates[i]
        p2 = coordinates[(i + 1) % num_coords]

        c1 = 2 * x_map[p1[0]]
        r1 = 2 * y_map[p1[1]]
        c2 = 2 * x_map[p2[0]]
        r2 = 2 * y_map[p2[1]]

        # Draw line from (c1, r1) to (c2, r2)
        if c1 == c2:  # Vertical
            start, end = min(r1, r2), max(r1, r2)
            for r in range(start, end + 1):
                grid[r][c1] = 1
        else:  # Horizontal
            start, end = min(c1, c2), max(c1, c2)
            for c in range(start, end + 1):
                grid[r1][c] = 1

    # 3. Flood Fill from Outside
    # We know (min_x-1, min_y-1) is at grid index (0,0) and is definitely outside
    queue = [(0, 0)]
    grid[0][0] = 2

    w, h = grid_width, grid_height

    while queue:
        cx, cy = queue.pop()  # DFS is fine, or change to deque for BFS

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                if grid[ny][nx] == 0:
                    grid[ny][nx] = 2
                    queue.append((nx, ny))

    # 4. Build 2D Prefix Sum of INVALID (Outside) cells
    # We want to know if a rectangle contains ANY Outside(2) cells.
    # So let's make a grid where 1 = Invalid, 0 = Valid (Inside or Boundary)
    invalid_grid = [[0] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 2:
                invalid_grid[r][c] = 1
            else:
                invalid_grid[r][c] = 0

    # Prefix sum
    # P[r][c] = sum(invalid_grid[0..r][0..c])
    P = [[0] * (w + 1) for _ in range(h + 1)]
    for r in range(h):
        for c in range(w):
            P[r + 1][c + 1] = P[r][c + 1] + P[r + 1][c] - P[r][c] + invalid_grid[r][c]

    def count_invalid(r1, c1, r2, c2):
        # r1, c1, r2, c2 are inclusive grid indices
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]

    # 5. Check all pairs
    max_area = 0

    # Pre-calculate grid indices for all coordinates
    mapped_coords = []
    for x, y in coordinates:
        mapped_coords.append((2 * x_map[x], 2 * y_map[y]))

    for i in range(num_coords):
        r1, c1 = mapped_coords[i][1], mapped_coords[i][0]
        x1, y1 = coordinates[i]

        for j in range(i + 1, num_coords):
            r2, c2 = mapped_coords[j][1], mapped_coords[j][0]
            x2, y2 = coordinates[j]

            # Determine rectangle bounds in grid
            rr_min, rr_max = min(r1, r2), max(r1, r2)
            cc_min, cc_max = min(c1, c2), max(c1, c2)

            # Check if this rectangle contains any invalid cells
            invalids = count_invalid(rr_min, cc_min, rr_max, cc_max)

            if invalids == 0:
                # Valid rectangle
                width = abs(x1 - x2) + 1
                height = abs(y1 - y2) + 1
                area = width * height
                if area > max_area:
                    max_area = area

    print(f"Max Area: {max_area}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

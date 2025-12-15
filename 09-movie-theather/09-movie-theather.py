def main(content: str):
    coordinates = [
        tuple(int(num) for num in row.split(",")) for row in content.split("\n")
    ]
    n = len(coordinates)

    max_ = 0
    for i in range(n):
        for j in range(i, n):
            c1, c2 = coordinates[i], coordinates[j]
            area = (abs(c1[0] - c2[0]) + 1) * (abs(c1[1] - c2[1]) + 1)
            if area > max_:
                max_ = area
    print(f"RESULT: {max_}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

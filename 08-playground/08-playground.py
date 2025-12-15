import bisect
from math import sqrt, prod
from typing import TypedDict


CONNECTION_COUNT = 1000


class Coordinate(TypedDict):
    id_: int
    x: int
    y: int
    z: int

    @classmethod
    def from_str(cls, str_: str, idx: int):
        x, y, z = str_.split(",")
        return cls(id_=idx, x=int(x), y=int(y), z=int(z))


def get_distance_tuple(c1: Coordinate, c2: Coordinate) -> tuple[int, str, str]:
    return (
        sqrt(
            (c1["x"] - c2["x"]) ** 2
            + (c1["y"] - c2["y"]) ** 2
            + (c1["z"] - c2["z"]) ** 2
        ),
        c1["id_"],
        c2["id_"],
    )


def update_circuits(circuits: list[set[int]], c1: int, c2: int):
    contained = []
    not_contained = []
    for circuit in circuits:
        if c1 in circuit or c2 in circuit:
            contained.append(circuit)
        else:
            not_contained.append(circuit)
    contained = set().union(*[*contained, {c1, c2}])
    return [contained] + not_contained


def main(content: str):
    coordinates = [
        Coordinate.from_str(row, idx) for idx, row in enumerate(content.split("\n"))
    ]

    distances: list[tuple[int, int, int]] = []  # (distance, coordinate1, coordinate2)
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            distance_tuple = get_distance_tuple(coordinates[i], coordinates[j])
            if len(distances) < CONNECTION_COUNT:
                bisect.insort(distances, distance_tuple)
            else:
                if distance_tuple[0] >= distances[-1][0]:
                    continue

                bisect.insort(distances, distance_tuple)
                distances.pop()

    circuits: list[set[int]] = []
    for distance in distances:
        c1, c2 = distance[1], distance[2]
        circuits = update_circuits(circuits, c1, c2)

    result = prod(sorted(map(len, circuits), reverse=True)[0:3])
    print(f"RESULT: {result}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

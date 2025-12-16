from typing import TypedDict
from itertools import combinations
from collections import Counter


LIGHT_ON = "#"
LIGHT_OFF = "."


class Machine(TypedDict):
    light_count: int
    light_diagram: dict[int, int]
    turned_on: set[int]
    wiring_schematics: list[tuple[int]]
    joltage_requirements: set[int]

    @classmethod
    def from_str(cls, string: str):
        all_items = string.split(" ")
        raw_diagram, raw_schematics, raw_jr = (
            all_items[0],
            all_items[1:-1],
            all_items[-1],
        )
        diagram = {
            i: 1 if item == LIGHT_ON else 0
            for i, item in enumerate(list(raw_diagram[1:-1]))
        }
        light_count = len(diagram)
        turned_on = {k for k, v in diagram.items() if v == 1}
        schematics = [
            tuple([int(num) for num in rs[1:-1].split(",")]) for rs in raw_schematics
        ]
        requirements = eval(raw_jr)
        return cls(
            light_diagram=diagram,
            turned_on=turned_on,
            light_count=light_count,
            wiring_schematics=schematics,
            joltage_requirements=requirements,
        )


def solve(machine: Machine) -> int:
    def get_updated(state: dict, schematics: tuple[int]):
        counts = Counter(x for sch in schematics for x in sch)
        turned_on = {k for k, v in counts.items() if v % 2 != 0}
        return turned_on

    n = len(machine["wiring_schematics"])
    initial_state = {i: 0 for i in range(machine["light_count"])}

    for r in range(1, n + 1):
        for combo in combinations(machine["wiring_schematics"], r):
            if get_updated(initial_state, combo) == machine["turned_on"]:
                return len(combo)


def main(content: str):
    raw_machines = content.split("\n")
    machines = [Machine.from_str(rm) for rm in raw_machines]

    count = 0
    for machine in machines:
        count += solve(machine)
    print(f"RESULT: {count}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

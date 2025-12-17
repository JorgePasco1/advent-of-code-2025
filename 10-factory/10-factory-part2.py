from typing import TypedDict
from ortools.sat.python import cp_model


LIGHT_ON = "#"


class Machine(TypedDict):
    light_count: int
    light_diagram: dict[int, int]
    turned_on: set[int]
    wiring_schematics: list[tuple[int]]
    joltage_requirements: list[int]

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
        requirements = eval(raw_jr.replace("{", "[").replace("}", "]"))
        return cls(
            light_diagram=diagram,
            turned_on=turned_on,
            light_count=light_count,
            wiring_schematics=schematics,
            joltage_requirements=requirements,
        )


def solve(machine: Machine) -> int:
    targets = machine["joltage_requirements"]

    n = len(targets)

    buttons = machine["wiring_schematics"]
    affects_slot = [
        [] for _ in range(n)
    ]  # affects_slot[s] = list of button indices that increment slot s

    for idx, schematic in enumerate(machine["wiring_schematics"]):
        slots_it_affects = tuple(sorted({int(s) for s in schematic}))  # unique + sorted
        for slot in slots_it_affects:
            affects_slot[slot].append(idx)
    print("buttons", buttons)
    print("affects_slot", affects_slot)

    # --- CP-SAT model: minimize sum(x[i]) subject to Ax = targets ---
    model = cp_model.CpModel()

    x = []
    for idx, slots in enumerate(buttons):
        # Tight upper bound: cannot exceed smallest target among affected slots (exact equality constraints)
        print("slots", slots)
        ub = min(targets[s] for s in slots)
        x.append(model.NewIntVar(0, ub, f"x_{idx}"))

    # Constraints per slot
    for s in range(n):
        model.Add(sum(x[i] for i in affects_slot[s]) == targets[s])

    # Objective: minimum total presses
    model.Minimize(sum(x))

    solver = cp_model.CpSolver()
    solver.Solve(model)
    print("================================")

    return int(solver.ObjectiveValue())


def main(content: str):
    raw_machines = content.split("\n")
    machines = [Machine.from_str(rm) for rm in raw_machines]

    count = 0
    for machine in machines[0:]:
        count += solve(machine)
    print(f"RESULT: {count}")


if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())

from collections import deque
from itertools import combinations
from pyrsistent import pvector, pset
import argparse


def solve(target, *numbers):
    # Breadth first search to guarantee minimum operations
    searched = pset(pset(numbers))
    search = deque([(pset(numbers), pvector())])

    while search:
        xs, commands = search.popleft()
        for x, y in combinations(xs, 2):
            if x > y:
                x, y = y, x
            new_ops = []
            if x != y:
                new_ops.append(
                    (
                        xs.remove(x).remove(y).add(y - x),
                        commands.append(f"{y} - {x} = {y - x}"),
                    )
                )
            new_ops.append(
                (
                    xs.remove(x).remove(y).add(x + y),
                    commands.append(f"{x} + {y} = {x + y}"),
                )
            )
            new_ops.append(
                (
                    xs.remove(x).remove(y).add(x * y),
                    commands.append(f"{x} * {y} = {x * y}"),
                )
            )
            if y % x == 0:
                new_ops.append(
                    (
                        xs.remove(x).remove(y).add(y // x),
                        commands.append(f"{y} / {x} = {y // x}"),
                    )
                )

            for ns, cs in new_ops:
                if target in ns:
                    yield cs
                elif ns not in searched:
                    searched.add(ns)
                    search.append((ns, cs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="The target value")
    parser.add_argument("numbers", help="Numbers to be combined", nargs="+")
    parser.add_argument("-a", "--all", help="Show all solutions", action="store_true")
    args = parser.parse_args()

    solutions = solve(int(args.target), *[int(x) for x in args.numbers])
    print("\n".join(next(solutions)))

    if args.all:
        for s in solutions:
            print("\n")
            print("\n".join(s))

import random


survival_friendly = True


def valid(item):
    if survival_friendly:
        if item.endswith("Spawn Egg"):
            return False

        # These used to be legitimately obtainable in survival
        if item.startswith("Infested"):
            return False

    return True


with open("items.txt") as file:
    coverings = {frozenset(item.lower()): item for item in file.read().strip("\"").split("\\n") if valid(item)}


solutions = set()
for _ in range(20000):  # Seems to be enough to find every four item solution
    to_cover = set("abcdefghijklmnopqrstuvwxyz")
    solution = ()

    # Shuffle the list so the greedy alg is a bit different each time
    shuffle = [*coverings.keys()]
    random.shuffle(shuffle)

    while to_cover:
        best = max(shuffle, key=lambda s: len(s & to_cover))
        solution += coverings[best],
        shuffle.remove(best)
        to_cover -= best

    # And sometimes, the greedy alg is dumb
    # Length 4 is proven optimal in the other file
    if len(solution) < 5:
        solutions.add(frozenset(solution))


print(len(solutions))
for solution in sorted(solutions, key=lambda s: len("".join(s)), reverse=False):
    print(", ".join(solution))

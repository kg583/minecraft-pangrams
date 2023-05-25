import itertools


survival_friendly = True
with open("items.txt") as file:
    coverings = {frozenset(item.lower()): item for item in file.read().strip("\"").split("\\n") if not survival_friendly
                 or not item.endswith("Spawn Egg")}

# Remove items which are subsets of other items
filtered = {}
for covering in coverings:
    if not any(covering.issubset(other) for other in coverings if other != covering):
        filtered[covering] = coverings[covering]


i = 0
for one, two, three in itertools.combinations(filtered, r=4):
    if one | two | three == set("abcdefghijklmnopqrstuvwxyz"):
        print(filtered[one], filtered[two], filtered[three])
        quit()

    i += 1
    if not i % 100000:
        print(i)  # In 1.19, there are 243 maximal items, and ~2.1 million ways to choose 3 of them

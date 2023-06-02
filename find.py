import random


ALPHABET = set("abcdefghijklmnopqrstuvwxyz")


# Config options
survival_friendly = True
nether = True
end = False

num_shuffles = 9000
max_len = 7

custom_keywords = ["Amethyst", "Azalea", "Diamond", "Exposed", "Head", "Jungle", "Mangrove", "Oxidized", "Warped",
                   "Weathered"]
custom_deny_list = ["Frogspawn", "Jukebox", "Mycelium", "Podzol", "Recovery Compass", "Totem of Undying",
                    "Twisting Vines", "Weeping Vines"]


# Not actually used by the general searcher
def is_pangram(words):
    return ALPHABET <= set("".join(words).lower())


def is_valid(item):
    keywords, denied = custom_keywords.copy(), custom_deny_list.copy()

    if survival_friendly:
        keywords += ["Command", "Infested", "Portal", "Spawn Egg"]
        denied += ["Barrier", "Bedrock", "Debug Stick", "Jigsaw Block", "Knowledge Book", "Player Head",
                   "Reinforced Deepslate", "Spawner", "Structure Void"]

    # Some of these items can be obtained without entering the Nether
    # but are extremely challenging and/or unlikely on a random seed
    if not nether:
        keywords += ["Basalt", "Blackstone", "Blaze", "Crimson", "Nether", "Potion", "Quartz", "Soul", "Warped"]
        denied += ["Ancient Debris", "Eye of Ender", "Ghast Tear", "Magma Cream"]

    if not end:
        keywords += ["Chorus", "End ", "Purpur", "Shulker"]
        denied += ["Dragon Egg", "Elytra"]

    if item in denied:
        return False

    if any(keyword in item for keyword in keywords):
        return False

    return True


with open("items.txt") as file:
    coverings = {frozenset(item.lower()): item for item in file.read().strip("\"").split("\\n") if is_valid(item)}


solutions = set()
for _ in range(num_shuffles):  # Seems to be enough to find every four item solution
    to_cover = ALPHABET.copy()
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
    if len(solution) <= max_len:
        solutions.add(frozenset(solution))


print(len(solutions))
for solution in sorted(solutions, key=lambda s: len("".join(s)), reverse=False)[:300]:
    print(", ".join(solution))

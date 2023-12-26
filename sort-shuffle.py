import json
import random

def main(filename):
    all = json.load(open(filename, "r"))
    
    basic = [x for x in all if x["level"] == "basic"]
    intermediate = [x for x in all if x["level"] == "intermediate"]
    advanced = [x for x in all if x["level"] == "advanced"]

    random.shuffle(basic)
    random.shuffle(intermediate)
    random.shuffle(advanced)

    recombined = basic + intermediate + advanced
    json.dump(recombined, open(filename[:-5] + "-shuffled.json", "w"), indent=4)

if __name__ == "__main__":
    main("merged.json")
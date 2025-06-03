import matplotlib.pyplot as plt
from random import choices, choice
from typing import Dict, List


class Shard:

    def __init__(self, r, e, l, m) -> None:
        self.r = r
        self.e = e
        self.l = l
        self.m = m


tests: int = 1000
shards: Dict[str, Shard] = {
    "ancient": Shard(0.915, 0.08, 0.005, 0),
    "void": Shard(0.915, 0.08, 0.005, 0),
    "sacred": Shard(0, 0.94, 0.06, 0),
    "primal": Shard(0.825, 0.16, 0.01, 0.005),
    "prism": Shard(0, 0.94, 0.06, 0)
}

prices = {
    "ancient": 1.20,
    "void": 4.24,
    "primal": 5.0,
    "sacred": 17.38,
    "prism": 10.0
}

rarities = ["epic", "legendary", "mythical"]

void_l = [i[:len(i) - 1:] for i in open("void_legendary").readlines()]


def form(value: int) -> str:
    temp = str(value)

    if 11 <= value <= 13:
        return 'th'

    if temp[~0] == '1':
        return 'st'
    elif temp[~0] == '2':
        return 'nd'
    elif temp[~0] == '3':
        return 'rd'
    else:
        return 'th'


def calculate(name: str, amount: int, rarity: str = "legendary", price: float = 0.8, x2: bool = False,
              iterations: int = 500) -> None:
    crystal = shards[name]
    mean = []

    if x2:
        if name in ["ancient", "void"]:
            crystal.r = 0.83
            crystal.e = 0.16
            crystal.l = 0.01
        elif name == "sacred":
            crystal.e = 0.88
            crystal.l = 0.12
        elif name == "primal":
            crystal.r = 0.82
            crystal.m = 0.01

    fr, fe, fl, fm = crystal.r, crystal.e, crystal.l, crystal.m
    costs = []
    ten, fifty, hundred, two_hundred = 0, 0, 0, 0
    great, good, meh = 0, 0, 0

    bottom = list(range(iterations))
    results = []
    color = ""

    if rarity == "mythical" and name != "primal":
        return

    for _ in range(iterations):

        cost = price

        total = choices(population=["rare", "epic", "legendary", "mythical"],
                        weights=[crystal.r, crystal.e, crystal.l, crystal.m],
                        k=amount)

        for i in range(1, amount):

            if total[i] == rarity:

                champion = ""

                temp = crystal.l
                if rarity == "epic":
                    temp = crystal.e
                    color = "purple"

                    if name == "void":
                        quality = choices(["Great", "Good", "Meh"], weights=[0.10714285714285714,
                                                                             0.21428571428571427,
                                                                             0.6785714285714286], k=1)
                    else:
                        quality = choices(["Great", "Good", "Meh"], weights=[0.020833333333333332,
                                                                             0.125,
                                                                             0.8541666666666666], k=1)

                elif rarity == "mythical":
                    temp = crystal.m
                    color = "red"

                    quality = choices(["Great", "Good", "Meh"], weights=[0.38636363636363635,
                                                                         0.45454545454545453,
                                                                         0.1590909090909091], k=1)
                else:
                    color = "orange"
                    if name == "void":
                        quality = choices(["Great", "Good", "Meh"], weights=[0.40540540540540543,
                                                                             0.43243243243243246,
                                                                             0.16216216216216217], k=1)
                    else:
                        quality = choices(["Great", "Good", "Meh"], weights=[0.24666666666666667,
                                                                             0.39666666666666667,
                                                                             0.3566666666666667], k=1)

                if quality[0] == "Great":
                    great += 1
                elif quality[0] == "Good":
                    good += 1
                else:
                    meh += 1

                results.append(i)

                # print(f"{rarity.capitalize()} found at {round(temp, 4)} probability on the {i}{form(i)} shard!")

                crystal.r = fr
                crystal.e = fe
                crystal.l = fl
                crystal.m = fm
                break

            if rarity == "legendary":
                if name in ["ancient", "void"] and i >= 200:
                    crystal.r -= 0.05
                    crystal.l += 0.05
                elif name == "sacred" and i >= 12:
                    crystal.e -= 0.02
                    crystal.l += 0.02
                elif name == "prism" and i >= 20:
                    crystal.e -= 0.04
                    crystal.l += 0.04
                elif name == "primal" and i >= 75:
                    crystal.r -= 0.01
                    crystal.l += 0.01

            if rarity == "epic":
                if name in ["ancient", "void"] and i >= 20:
                    crystal.r -= 0.02
                    crystal.e += 0.02

            if rarity == "mythical":
                if name == "primal" and i >= 200:
                    crystal.r -= 0.1
                    crystal.m += 0.1

            total = choices(population=["rare", "epic", "legendary", "mythical"],
                            weights=[crystal.r, crystal.e, crystal.l, crystal.m],
                            k=amount)

            cost += price

        if i <= 10:
            ten += 1
        elif i <= 50:
            fifty += 1
        elif i <= 100:
            hundred += 1
        elif i <= 200:
            two_hundred += 1

        costs.append(cost)
        mean.append(i)

    print(f"Average cost of a {rarity}: ${round(sum(costs) / len(costs), 2)}")
    print(f"Highest cost of a {rarity}: ${round(max(costs), 2)}")
    print(f"Average {name} shards required: {round(sum(mean) / len(mean), 2)}")
    print(f"Great {rarity}(s): {round(great / iterations * 100, 4)}%, "
          f"Good {rarity}(s): {round(good / iterations * 100, 4)}%, "
          f"Meh / Niche {rarity}(s): {round(meh / iterations * 100, 4)}%, ")
    print(f"Within 10 shards: {round(ten / iterations * 100, 4)}%, "
          f"Within 50 shards: {round(fifty / iterations * 100, 4)}%, "
          f"Within 100 shards: {round(hundred / iterations * 100, 4)}%, "
          f"Within 200 shards: {round(two_hundred / iterations * 100, 4)}%, "
          f"Over 200 shards: {round((iterations - (ten + fifty + hundred + two_hundred)) / iterations * 100, 4)}%")

    plt.scatter(bottom, results, marker='.', color=color, label=f"Average cost of a {rarity}: ${round(sum(costs) / len(costs), 2)}\nHighest cost of a {rarity}: ${round(max(costs), 2)}")
    plt.xlabel("Iterations of simulation")
    plt.ylabel(f"Amount of {name} shards used")
    plt.title(f"Raid analytics for {rarity}s {'X2' if x2 else ''}")
    plt.legend()
    plt.show()


calculate((x := input("Enter shard: ").lower()), int(input("Enter amount of shards: ")),
          rarity=input("Enter rarity: "), price=prices[x],
          x2=True if input("X2 Drops (y/n): ").lower() == 'y' else False)


for i in shards.keys():
    for v in rarities:
        calculate(i, 220, v, price=prices[i], x2=True)

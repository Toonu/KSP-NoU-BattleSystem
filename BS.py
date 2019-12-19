import os
import random
import time


class Message:
    @staticmethod
    def start():
        start = {1: "The battle is about to start.",
                 2: "The battle is commencing.",
                 3: "Both forces deployed and started advancing towards each other",
                 4: "After long wait, the order to attack finally came...",
                 }
        Message.header("Unknown")
        Message.wait(start[random.randint(1, len(start))])
        pass

    @staticmethod
    def kill(vehicle, battle):
        if battle == 1:
            kill = {1: f"“Nailed em! He’s finished.”",
                    2: f"Lad’s a fireball now.",
                    3: f"Scratch one!",
                    }
        elif battle == 2:
            kill = {1: f"“Nailed em! He’s finished.”",
                    2: f"Lad’s a fireball now.",
                    3: f"Pilot knocked out.",
                    4: f"Plane burnt down.",
                    5: f"Engine Died: Fuel Starvation",
                    6: f"Bandit down, no chute."
                    }
        else:
            kill = {1: f"“Nailed em! He’s finished.”",
                    2: f"",
                    3: f"Scratch one!",
                    }
        Message.wait(kill[random.randint(1, len(kill))])

    @staticmethod
    def hit():
        hit = {1: f"Target hit.",
               2: f"Target damaged.",
               }
        Message.wait(hit[random.randint(1, len(hit))])
        pass

    @staticmethod
    def malfunction(vehicle, eq_system):
        malfunction = {1: f"Your {vehicle.define_system(eq_system)} has failed to lock on target after launch.",
                       2: f"{vehicle.define_system(eq_system)} has run out of fuel and auto destructed itself.",
                       3: f"{vehicle.define_system(eq_system)} missed the target",
                       4: f"{vehicle.define_system(eq_system)} failed to lit its engine",
                       5: f"{vehicle.define_system(eq_system)} failed to connect.",
                       6: f"{vehicle.define_system(eq_system)} is heading towards the sun now",
                       7: f"Enemy countermeasures were too much effective.",
                       8: f"{vehicle.define_system(eq_system)} went and whiffed em’.",
                       9: f"Failure to decouple."
                       }
        Message.wait(malfunction[random.randint(1, len(malfunction))])
        pass

    @staticmethod
    def gun_malfunction(vehicle, eq_system):
        malfunction = {1: f"Contact was too slippery.",
                       2: f"Must have been poor luck.",
                       3: f"Shot lost the mark.",
                       4: f"{vehicle.define_system(eq_system)} failed to connect."
                       }
        Message.wait(malfunction[random.randint(1, len(malfunction))])
        pass

    @staticmethod
    def death(vehicle):  # Reply with death message of vehicle = Asset object on Message self
        death = {1: f"Your {vehicle.typename.lower()} has been utterly crushed by your foes.",
                 2: f"{vehicle.typename.capitalize()} status: Presumed KIA.",
                 3: f"{vehicle.typename.capitalize()} killed in action.",
                 4: f"{vehicle.typename.capitalize()} disappeared from your battle control screen.",
                 5: f"{vehicle.typename.capitalize()} couldn't stood against such strong enemy."
                 }
        Message.header(vehicle.side)
        Message.wait(death[random.randint(1, len(death))])
        pass

    @staticmethod
    def header(craft):
        if isinstance(craft, str):
            print("Side:   ", craft)
        else:
            print("Side:   ", craft.name)
        print("Report:", random.randint(25000, 300000), time.strftime("       %D-%H:%M:%S", time.localtime()))
        print("        Confidental eyes only\n         Classified Document\n   To OPFOR, MoD, AFHC, TLBC, BCTC")
        pass

    @staticmethod
    def wait(message, i=3):  # Reply with random dots and message
        dot = "."
        for repeat in range(6):
            print(dot * random.randint(2, 4), end="")
            time.sleep(0.5)
        print("\n" + dot * i, end="")
        time.sleep(1)
        print(str(message))
        pass


class Asset:
    def __init__(self, name, asset_type, state, side, year, battle):
        self.name = name
        self.type = asset_type
        self.typename = vehicles[battle][asset_type]
        self.state = state
        self.side = side
        self.year = year
        self.reliability = year / 4000
        self.battle = battle
        self.systemtype = self.system_type()
        self.systems = {}

    def __str__(self):
        return str(self.name + "_" + self.typename + " - STATE-" + str(self.state))

    def add_system(self, system, amount):
        if amount == 0 and system in self.systems:
            del self.systems[system]
        elif amount == 0 and system not in self.systems or amount == system == "x":
            pass
        else:
            self.systems[system] = amount
        clear()
        print(self.name + "_" + self.typename + " - STATE-" + str(self.state), "\nSystems Equipped:")
        for thing, amount in self.systems.items():
            print(eq_systems[self.systemtype][int(thing)], amount, end=", ")
        print()
        pass

    def define_system(self, eq_system):  # Returns system number of eq_system to its name.
        return eq_systems[self.systemtype][self.systems[eq_system]]

    def system_type(self):
        if self.type <= 4 and self.battle == 1:
            return 1
        elif self.type >= 5 and self.battle == 1:
            return 2
        elif self.battle == 2:
            return 3
        elif self.battle == 3:
            return 4

    def attack(self, system, target):
        self.systems[system] -= 1
        target.defense(system)
        pass  # TODO

    def defense(self, system):

        pass

def welcome():
    version = "Welcome to Battle System Manager v0.5 (ALPHA)"
    print("=" * len(version), "\n", version, "\n", " " * ((len(version) - 13) // 2), "Made by Toonu\n",
          " " * ((len(version) - 21) // 2), "The Emperor of Iconia\n", " " * (len(version) // 2), "☩\n",
          " " * ((len(version) - 5) // 2), "☩☩☩☩☩\n", " " * (len(version) // 2), "☩\n", "≋" * len(version), "\n",
          sep="")
    pass


def oob_main():
    first = []
    second = []
    battle = oob_battle_type()
    year = oob_year()
    sides = oob_sides()
    for side in range(1, 3):
        for i in range(sides[side]):
            if side == 1:
                first.append("asset{0}_{1}".format(side, i))
                first[i] = Asset("asset{0}_{1}".format(side, i), oob_add_asset(battle, i, side), 3, side, year, battle)
            else:
                second.append("asset{0}_{1}".format(side, i))
                second[i] = Asset("asset{0}_{1}".format(side, i), oob_add_asset(battle, i, side), 3, side, year, battle)
    a = first + second
    for unit in a:
        oob_equipment(unit, a)
    oob_final(a)
    input("\n\nBattle will commence after pressing enter.")
    Message.wait("", 9)
    print('Program ends here for now...')
    input()
    battle_core(a, first, second, battle, year)


def oob_final(d):
    print("Final Order of Battle:\n======================")
    for unit in d:
        print(f"Side {unit.side} | {unit.typename}, equipped with", end=" ")
        if not unit.systems == {}:
            for thing, amount in unit.systems.items():
                print(eq_systems[unit.systemtype][int(thing)], amount, end=", ")
            print()
        else:
            print("its own weapon system only.")
    print()


def oob_battle_type():
    user_choice = 0
    print("Please choose the type of battle you want to simulate by typing it number:\nGround battle: "
          "| 1 |\nAir Battle:    | 2 |\nNaval Battle   | 3 |\nPlease choose battle type by typing its number:")
    while not user_choice:
        user_choice = user_input(0, 4)
    clear()
    return user_choice


def oob_year():
    user_choice = 0
    print("Write what year the battle is in. (1946 - 2019)")
    while not user_choice:
        user_choice = user_input(1945, 2020)
    clear()
    return user_choice


def oob_equipment(unit, a):
    clear()
    while True:
        print(unit)
        for i in range(len(eq_systems[unit.systemtype])):
            print(i, "=", eq_systems[unit.systemtype][i], end=" | ")
        print("Choose system the vehicle has equipped:\nTo exit equipping mode, select None. "
              "To remove item, set type normally and amount to 0.\nTo duplicate last vehicle done, type "
              f"{len(eq_systems[unit.systemtype])}")
        system = user_input(-1, len(eq_systems[unit.systemtype]) + 1)
        if not system:
            return
        elif system == len(eq_systems[unit.systemtype]):
            splitter = str(unit.name).split("_")
            merger = splitter[0] + "_" + str(int(splitter[1]) - 1)
            for asset in a:
                if asset.name == merger:
                    unit.systems = asset.systems
                    unit.add_system("x", "x")
        else:
            print("Specify how many:")
            amount = user_input(-1)
            unit.add_system(system, amount)


def oob_add_asset(battle, number, side):
    user_choice = 0
    clear()
    print(f"Asset #{number} of {side} side.\nType number of asset you want to add to the order of battle:")
    for i in range(1, len(vehicles[battle]) + 1):
        print(i, "=", vehicles[battle][i], end=" | ")
    print()
    if battle == 1:  # Ground
        user_choice = user_input(0, 7)
    elif battle == 2:  # Air
        user_choice = user_input(0, 6)
    elif battle == 3:  # Naval
        user_choice = user_input(0, 9)
    return user_choice


def oob_sides():
    sides = {}
    for side in range(1, 3):
        print(f"Specify how many assets side {side} has:")
        sides[side] = user_input()
    while True:
        clear()
        print(f"Side 1:", sides[1], "units\nSide 2:", sides[2], "units\nIs the numbers right? (1 Yes/0 = No)")
        response = user_input(-1, 2)
        if response == 1:
            return sides
        elif not response:
            while True:
                print("What side is wrong? (1/2)")
                response = user_input(0, 3)
                print("How many assets it has?")
                sides[response] = user_input()
                break


def user_input(minimum=0, maximum=200):
    while True:
        user_choice = input()
        try:
            if type(user_choice) == str and minimum < int(user_choice) < maximum:
                return int(user_choice)
            else:
                print("Your input is out of specified range!\nPlease retry: ")
        except ValueError:
            print("Your input isn't a number!\nPlease retry: ")
            continue


def clear():
    import platform
    if platform.system() == "Windows" or platform.system() == "Linux":
        clear = lambda: os.system("cls")
    elif platform.system() == "Darwin":
        clear = lambda: os.system("clear")
    clear()


def battle_core(a, side_a, side_b, battle_type, year):
    Message.start()
    won = False
    while not won:
        pass
    pass


"""
vehicles
1 - Ground battle, 2 - Air battle, 3 - naval battle
systems
1 - tank, afv, ifv, apc
2 - sam, mlb
3 - air
4 - naval
"""

vehicles = {
    1: {1: "MBT", 2: "AFV", 3: "IFV", 4: "APC", 5: "SAM", 6: "MLB"},
    2: {1: "Small Multirole Aircraft", 2: "Medium Multirole Aircraft", 3: "Large Multirole Aircraft",
        4: "Large Heavy Aircraft", 5: "Very Large Heavy Aircraft"},
    3: {1: "Corvette", 2: "Frigate", 3: "Destroyer", 4: "Cruiser", 5: "Battlecruiser", 6: "Battleship",
        7: "Light Carrier", 8: "Aircraft Carrier"}}
eq_systems = {
    1: {0: "None", 1: "Smoke", 2: "HK-APS", 3: "SK-APS", 4: "ATGM"},
    2: {0: "None", 1: "Smoke", 2: "HK-APS", 3: "SK-APS", 4: "SR-SAM", 5: "MR-SAM", 6: "LR-SAM"},
    3: {0: "None", 1: "Flares", 2: "Chaff", 3: "ECM", 4: "EWS", 5: "SRAAM", 6: "MRAAM", 7: "LRAAM", 8: "AGM", 9: "AShM",
        10: "SEAD", 11: "Cruise Missile", 12: "Bomb", 13: "GBU"},
    4: {0: "None", 1: "CIWS", 2: "DEW", 3: "ECM", 4: "Smoke", 5: "Chaff", 6: "AShM", 7: "SR-SAM", 8: "MR-SAM",
        9: "LR-SAM"}
}

# welcome()
oob_main()

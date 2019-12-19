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
    def __init__(self, name, asset_type, state, side):
        self.name = name
        self.type = self.asset_assign(asset_type)
        self.typename = vehicles[asset_type[0]][asset_type[1]]
        self.state = state
        self.statename = self.define_state()
        self.side = side
        self.year = asset_type[2]
        self.battle = asset_type[0]
        self.reliability = self.year / 3000
        self.systemtype = self.system_type()
        self.systems = {}

    def __str__(self):
        return str(self.name + "_" + self.typename + " - STATE-" + str(self.state))

    def add_system(self, system, amount):  # Adds equipment to the systems dict of object.
        if amount == 0 and system in self.systems:
            del self.systems[system]
        elif amount == 0 and system not in self.systems:
            pass
        else:
            self.systems[system] = amount

    def equipped_systems(self):
        clear()
        print("\nSystems Equipped:")
        for thing, amount in self.systems.items():
            print(eq_systems[self.systemtype][int(thing)], amount, end=", ")
        print()

    def define_system(self, system):  # Returns system name of the obj.
        return eq_systems[self.systemtype][self.systems[system]]

    def define_state(self):  # Returns name of the obj state.
        return state[self.state]

    def system_type(self):  # Assigns system per obj type
        if self.type <= 4 and self.battle == 1:
            return 1
        elif self.type >= 5 and self.battle == 1:
            return 2
        elif self.battle == 2:
            return 3
        elif self.battle == 3:
            return 4

    @staticmethod
    def asset_assign(asset_type):
        if asset_type[0] == 1:
            result = asset_type[1]
        if asset_type[0] == 2:
            result = asset_type[1] + len(vehicles[asset_type[0]])
        elif asset_type[0] == 3:
            result = asset_type[1] + len(vehicles[asset_type[0] - 1]) + len(vehicles[asset_type[0]])
        return result

    def attack(self, system, target):
        self.systems[system] -= 1
        target.defense(system)
        pass  # TODO

    def defense(self, system):

        pass


def welcome():
    version = "Welcome to Battle System Manager v0.6 (ALPHA)"
    print("=" * len(version), "\n", version, "\n", " " * ((len(version) - 13) // 2), "Made by Toonu\n",
          " " * ((len(version) - 21) // 2), "The Emperor of Iconia\n", " " * (len(version) // 2), "☩\n",
          " " * ((len(version) - 5) // 2), "☩☩☩☩☩\n", " " * (len(version) // 2), "☩\n", "≋" * len(version), "\n",
          sep="")
    pass


def oob_main():  # Main Body of assigning assets.
    first = []
    second = []
    battle_info = oob_battle_info()
    print("Stage III: Adding Vehicles\n")
    for side in range(1, 3):  # Creates the assets (vehicles) with numbered names and their specifications.
        for i in range(battle_info[0][side]):
            if side == 1:
                first.append("asset{0}_{1}".format(side, i))
                first[i] = Asset("asset{0}_{1}".format(side, i), oob_add_asset(i, side, battle_info[1]), 5, side)
            else:
                second.append("asset{0}_{1}".format(side, i))
                second[i] = Asset("asset{0}_{1}".format(side, i), oob_add_asset(i, side, battle_info[1]), 5, side)
    a = first + second
    for unit in a:  # Equips created assets with weapon systems.
        oob_equipment(unit, a)
    oob_final(a)  # Finalizes and prints the OOB.
    input("\n\nBattle will commence after pressing enter.")  # Starting next phase and battle functions itself.
    Message.wait("", 9)
    print('Program ends here for now...')
    input()
    print("Or does it?...")
    battle_core(a, first, second)


def oob_equipment(unit, a):
    clear()
    while True:
        print(unit)
        for i in range(len(eq_systems[unit.systemtype])):
            print(i, "=", eq_systems[unit.systemtype][i], end=" | ")
        print()
        system = user_input(-1, len(eq_systems[unit.systemtype]) + 1, f"\nTo exit equipping mode, select None. "
                                                                      f"To remove item, set system type and amount to "
                                                                      f"0.\nTo duplicate last vehicle done, type "
                                                                      f"{len(eq_systems[unit.systemtype])}.\nChoose "
                                                                      f"system the vehicle has equipped: ")
        if not system:
            return
        elif system == len(eq_systems[unit.systemtype]):
            splitter = str(unit.name).split("_")
            merger = splitter[0] + "_" + str(int(splitter[1]) - 1)
            for asset in a:
                while asset.name == merger:
                    if asset.systemtype == unit.systemtype:
                        unit.systems = asset.systems
                        unit.equipped_systems()
                        break
                    else:
                        clear()
                        print("The vehicles aren't of same type. Cannot duplicate equipment.")
                        break
        else:
            amount = user_input(-1, 200, "Specify how many: ")
            unit.add_system(system, amount)
            unit.equipped_systems()


def oob_add_asset(number, side, year):  # Specify each asset category, year and its type
    clear()
    category = user_input(0, 4, f"asset{side}_{number}\nAsset #{number} of {side} side.\nWhat category of vehicles you "
                                f"want to add?\n1 | Ground\n2 | Air\n3 | Naval\nInput: ")
    clear()
    print(f"asset{side}_{number}\nAsset #{number} of {side} side.\nType number of asset you want to add to the order "
          f"of battle: ")
    for i in range(1, len(vehicles[category]) + 1):  # Prints out all unit types of unit category.
        print(i, "=", vehicles[category][i], end=" | ")
    unit_type = user_input(0, len(vehicles[category]) + 1, "\nInput: ")
    clear()
    print(f"asset{side}_{number}\nAsset #{number} of {side} side.\nWhat year is the vehicle from. (1946 - 2019)\n"
          f"In case the vehicle is from {year},press enter.\nInput: ")
    new_year = user_input(1945, 2020, "", True)
    if new_year != "":
        year = new_year
    return category, unit_type, int(year)


def oob_battle_info():  # Specify how many units each side have and let the user change the values.
    sides = {}
    print("Stage I: Assigning year of battle.")
    year = user_input(1945, 2020, "Specify year: ")
    print("Stage II: Assigning vehicles to their respective sides.")
    for side in range(1, 3):
        sides[side] = user_input(0, 200, f"Specify how many assets side {side} has: ")
    while True:
        clear()
        print(f"Side 1:", sides[1], "units\nSide 2:", sides[2], "units")
        response = user_input(-1, 2, "Are the numbers right? (1 Yes/0 = No)\nInput: ")
        if response == 1:
            return sides, year
        elif not response:
            while True:
                response = user_input(0, 3, "What side is wrong? (1/2)")
                sides[response] = user_input(0, 200, "How many assets it has?")
                break


def user_input(minimum=0, maximum=200, message="", test=False):  # Limited number user input.
    while True:
        user_choice = input(message)
        try:
            if user_choice == "" and test:
                return user_choice
            if type(user_choice) == str and minimum < int(user_choice) < maximum:
                return int(user_choice)
            else:
                print("Your input is out of specified range!\nPlease retry: ")
        except ValueError:
            print("Your input isn't a number!\nPlease retry: ")
            continue


def clear():  # Clears the terminal
    import platform
    if platform.system() == "Windows" or platform.system() == "Linux":
        clear = lambda: os.system("cls")
    elif platform.system() == "Darwin":
        clear = lambda: os.system("clear")
    clear()


def oob_final(d):  # Prints units of both sides with their type and year.
    print("Final Order of Battle:\n======================")
    for unit in d:
        print(f"Side {unit.side} | {unit.year} | {unit.typename}, equipped with", end=" ")
        if not unit.systems == {}:
            for thing, amount in unit.systems.items():
                print(eq_systems[unit.systemtype][int(thing)], amount, end=", ")
            print()
        else:  # In case no weapons at specific unit.
            print("only its own weapon system.")
    print()


def battle_core(a, side_a, side_b):  # Core of the battle algorithm.
    Message.start()
    won = False
    while not won:
        for a, b in zip(side_a, side_b):
            a.attack(1, b)
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
vehicles_internal = {1: "MBT", 2: "AFV", 3: "IFV", 4: "APC", 5: "SAM", 6: "MLB", 7: "Small Multirole Aircraft",
                     8: "Medium Multirole Aircraft", 9: "Large Multirole Aircraft", 10: "Large Heavy Aircraft",
                     11: "Very Large Heavy Aircraft", 12: "Corvette", 13: "Frigate", 14: "Destroyer", 15: "Cruiser",
                     16: "Battlecruiser", 17: "Battleship", 18: "Light Carrier", 19: "Aircraft Carrier"}
eq_systems = {
    1: {0: "None", 1: "Smoke", 2: "HK-APS", 3: "SK-APS", 4: "ATGM"},
    2: {0: "None", 1: "Smoke", 2: "HK-APS", 3: "SK-APS", 4: "SR-SAM", 5: "MR-SAM", 6: "LR-SAM"},
    3: {0: "None", 1: "Flares", 2: "Chaff", 3: "ECM", 4: "EWS", 5: "SRAAM", 6: "MRAAM", 7: "LRAAM", 8: "AGM", 9: "AShM",
        10: "SEAD", 11: "Cruise Missile", 12: "Bomb", 13: "GBU"},
    4: {0: "None", 1: "CIWS", 2: "DEW", 3: "ECM", 4: "Smoke", 5: "Chaff", 6: "AShM", 7: "SR-SAM", 8: "MR-SAM",
        9: "LR-SAM"}
}
state = {0: "KIA", 1: "Heavily Damaged", 2: "Major Damage taken", 3: "Light Damage", 4: "Scratched", 5: "Normal",
         6: "RTB", 7: "MIA", 8: "Disappeared"}

try:
    welcome()
    oob_main()
except Exception as e:
    print(e)
    print(type(e))

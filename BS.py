"""
Battle system for NoU.
by Toonu
"""

import random
import time


class Message:
    """
    Message is printing messages
    """

    @staticmethod
    def message(msg_type, unit, target, system=1, headline="", dot=True, dots=True, repeat=0, header=True, wait=True):
        """
        Prints various random messages from the message dict.
        :param target: Second obj
        :param headline: Header subject message.
        :param wait: Disable wait message.
        :param msg_type: Type of message from the dict.
        :param unit: Vehicle obj affected.
        :param header: Disable header message.
        :param system: Vehicle obj weapon system.
        :param dot: Triple dots in wait message.
        :param dots: Dots in wait message.
        :param repeat: How many triple dots are repeated in wait message.

         #  0 | Battle start, 1 | Death, 2 | Gun malfunctions, 3 | Missile failure, 4 | Hit, 5 | End of report
        """
        messages = {0: ["The battle is about to start.", "The battle is commencing.",
                        "Both forces deployed and started advancing towards each other",
                        "After long waiting, the order to attack has finally came..."],
                    1: [],
                    2: ["Contact was too slippery and the rounds bounced.", "Must have been poor luck, rounds haven't"
                                                                            "penetrated.", "Shots lost the mark.",
                        "No penetration", "No good hits on the target.",
                        "Rounds haven't even scratched the enemy plates.", "Shot missed by a country mile.",
                        f"{unit.define_system(system)} failed to connect and couldn't have been fired.",
                        f"{unit.define_system(system)} malfunctioned.", "Missed the mark, try again."],
                    3: [f"The {unit.define_system(system)} has failed to lock onto the target after launch.",
                        f"{unit.define_system(system)} has run out of fuel and auto destructed itself.",
                        f"{unit.define_system(system)} failed to lit its engine.",
                        f"{unit.define_system(system)} failed to connect and malfunctioned.",
                        f"Enemy countermeasures were too much effective and misguided the {unit.define_system(system)} "
                        f"into the surface.", f"{unit.define_system(system)} went and whiffed em’.",
                        f"Failure to decouple.", f"Failure to launch.."],
                    4: [f"{target.typename.lower()} {target.name} was hit with {unit.define_system(system)} fired from "
                        f"{unit.typename.lower()} {unit.name} with {headline} dmg.",
                        f"{target.typename.lower()} {target.name} was damaged by {unit.define_system(system)} fired "
                        f"from {unit.typename.lower()} {unit.name} with {headline} dmg."],
                    5: ["End of report.\nSigned Electronically", "End of report.\nProceed with your operation."],
                    6: [f"{unit.define_system(system)} missed the target.",
                        f"{unit.define_system(system)} is heading towards the sun now."]
                    }

        if header:
            Message.header(headline)
        if wait:
            Message.wait(messages[msg_type][random.randint(0, len(messages[msg_type]) - 1)], i=repeat, dot=dot,
                         dots=dots)
        if not header and not wait:
            Message.wait(messages[msg_type][random.randint(0, len(messages[msg_type]) - 1)], i=0, dot=False, dots=False)

    @staticmethod
    def kill(unit):
        """
        Prints killing message.
        :param unit: Unit obj that was killed.
        """
        kill = {1: [f"“Nailed em! He’s finished.”", f"Lad’s a fireball now.", f"Scratch one, he's finished!",
                    f"Target crew bailed out", f"Our shot penetrated the enemy and destroyed everything inside.",
                    "The enemy has been utterly crushed by his foes.",
                    f",{unit.typename.capitalize()} {unit.name} status: Presumed KIA.",
                    f"{unit.typename.capitalize()} {unit.name} killed in action.",
                    f"{unit.typename.capitalize()} {unit.name} disappeared from battle control screen.",
                    f"{unit.typename.capitalize()} {unit.name} couldn't stood against such strong enemy."],
                2: [f"“Nailed em! He’s finished.”", f"Lad’s a fireball now.", f"Pilot knocked out.",
                    f"Plane burnt down.", f"Engine Died: Fuel Starvation", f"Bandit down, no chute to be seen.",
                    f",{unit.typename.capitalize()} {unit.name} status: Presumed KIA.",
                    f"{unit.typename.capitalize()} {unit.name} disappeared from battle control screen.",
                    f"{unit.typename.capitalize()} {unit.name} killed in action.",
                    f"{unit.typename.capitalize()} {unit.name} couldn't stood against such strong enemy."],
                3: [f"“Nailed em! He’s finished.”", f"Enemy is sinking.", f"Scratch one!",
                    f"Enemy has huge hole in his hull", f"Target is taking water and abandoning the ship was ordered.",
                    "They’ve gone to the Krusty Krab and never returned.", "They’re going under, we got em!",
                    "The target has achieved Salvation, by force.", "May Neptune have mercy on them.",
                    "She got shoved into Davy Jones’ locker by the Sea Chad.",
                    "“Something something crisp white sheets.”",
                    f",{unit.typename.capitalize()} {unit.name} status: Presumed KIA.",
                    f"{unit.typename.capitalize()} {unit.name} killed in action.",
                    f"{unit.typename.capitalize()} {unit.name} disappeared from battle control screen.",
                    f"{unit.typename.capitalize()} {unit.name} couldn't stood against such strong enemy."]}
        print(kill[unit.type][random.randint(1, len(kill))])

    @staticmethod
    def header(craft):
        """
        Prints header message.
        :param craft: Headline of header message.
        """
        print(craft)
        print("Report:", random.randint(25000, 300000), time.strftime("       %D-%H:%M:%S", time.localtime()))
        print("        Confidental eyes only\n         Classified Document\n   To OPFOR, MoD, AFHC, TLBC, BCTC")

    @staticmethod
    def wait(message, i=3, dots=True, dot=True):
        """
        Reply with random dots and message
        :param message: Message to be printed after dots.
        :param i: How many triple-dots are printed before the main message.
        :param dots: If random dots are printed before the triple dots.
        :param dot: If the triple dots are printed.
        """
        if dots:
            symbol = "."
            for repeat in range(6):
                print(symbol * random.randint(2, 4), end="")
                time.sleep(1)
            if dot:
                print("\n" + symbol * i, end="")
            time.sleep(1.5)
        print(str(message))


class Asset:
    """
    Asset objects are the units itself.
    """

    def __init__(self, name, batch, side):
        self.name = name
        self.type = batch[0]  # External unit type Eg 1 veh 2 air 3 sea
        self.external = batch[1]  # Unit specific type Eg. 1 for MBT or Small Multirole
        self.internal = self.asset_assign(batch)  # Internal unit type
        self.typename = vehicles[batch[0]][batch[1]][0]  # Asset name Eg. MBT
        self.state = 8  # How much alive asset is
        self.statename = state[self.state]  # How much alive asset is in normal name
        self.side = side  # Fighting side
        self.year = batch[2]  # Year of origin
        self.reliability = (self.year - 1945) // 2  # Reliability of its WS
        self.systems = {89 + self.external: 1}
        self.distance = 11
        self.turn = 1
        self.has_radar = self.has_radar_fn()

    def __str__(self):
        return str(self.name + "_" + self.typename + " - State: " + str(self.statename))

    def add_system(self, system, amount):
        """
        Adds equipment to the systems dict of object.
        :param system: System to be added.
        :param amount: How much of them should be added.
        """
        if amount == 0 and system in self.systems:
            del self.systems[system]
        elif amount == 0 and system not in self.systems:
            pass
        else:
            self.systems[system] = amount

    def define_system(self, system):
        """
        Defines system str name.
        :param system:  System int defining system name string.
        :return:        Returns str of the obj name.
        """
        try:
            return eq_systems[self.type][system][0]
        except KeyError:
            return "weapon system"

    def has_radar_fn(self):
        """
        Assigns radar to SAM.
        :return: Returns radar true for SAM.
        """
        if self.internal == 5:
            return True
        else:
            return False

    @staticmethod
    def asset_assign(asset_type):
        """
        Assign internal type of the unit.
        :param asset_type: Unit batch list.
        :return: Returns unit internal type also specified in global vehicle_internals.
        """
        if asset_type[0] == 1:
            result = asset_type[1]
        elif asset_type[0] == 2:
            result = asset_type[1] + len(vehicles[1])
        else:
            result = asset_type[1] + len(vehicles[1]) + len(vehicles[2])
        return result

    def attack(self, system, target):
        """
        Function for reducing asset weapon fired last turn and starting its target defensive method.
        :param system: Weapon system used.
        :param target: Target of the fired weapon system.
        :return: Returns nothing. yet...
        """
        if not target:
            global notfound
            print(f"{self} has no target to attack.")
            notfound += 1
            return
        if not system >= 90:
            self.systems[system] -= 1
            if self.systems[system] == 0:
                self.systems.pop(system)

        if target.defense(self, system) is None:
            return None
        else:
            return 1

    def defense(self, unit, system):
        """
        Function of hitting probability and decreasing unit status after hit.
        :param unit: Attacking vehicle.
        :param system: Attacking weapon system.
        """
        global state
        critical = 1
        if self.state > 0:
            reliability = unit.reliability + random.randint(0, 30)
            if reliability > 30:
                probability = random.randint(0, 100)
                for defensive in self.systems.copy():
                    if eq_systems[self.type][defensive][1] < 0:
                        if unit.type == 1 and defensive == 2:
                            pass
                        elif unit.type == 2 and defensive in (3, 4):
                            pass
                        elif unit.type == 3 and defensive in (2, 3):
                            pass
                        else:
                            self.systems[defensive] -= 1
                        probability -= 10 * -eq_systems[self.type][self.external][1]
                        if self.systems[defensive] == 0:
                            self.systems.pop(defensive)
                if probability <= 30:
                    if system > 89 or unit.type == 3 and system == 1:
                        Message.message(2, unit, self, system, header=False)
                    else:
                        Message.message(3, unit, self, system, header=False)
                    return 1
                elif 31 <= probability <= 89:
                    Message.message(4, unit, self, system, headline=eq_systems[unit.type][system][1], header=False)
                    self.state -= eq_systems[unit.type][system][1]
                elif 90 <= probability:
                    critical = 2
                    Message.message(4, unit, self, system, headline=eq_systems[unit.type][system][1] * critical,
                                    header=False)
                    self.state -= eq_systems[unit.type][system][1] * critical
            else:
                if system > 89 or unit.type == 3 and system == 1:
                    Message.message(2, unit, self, system, header=False)
                else:
                    Message.message(3, unit, self, system, header=False)
                return 1

        try:
            self.statename = state[self.state]
        except IndexError:
            self.state = 0
            self.statename = state[0]
        if self.state <= 0:
            Message.kill(self)
            return None
        else:
            return 1


def battle_core(side_a, side_b):
    """
    Core of the battle algorithm.
    :param side_a: Objects of side a.
    :param side_b: Objects of side b.
    """
    turn = 0
    # Message.message(0, default, headline="unknown")
    while len(side_b) > 0 and len(side_a) > 0:
        turn += 1
        clear()
        Message.header(f"Turn: {turn}")
        result = battle_ws_by_distance(side_a, side_b)
        if result:
            print("Nothing happened this in turn.")
        input("\nPress Enter to continue.")
        if notfound > 99:
            break

    clear()
    if notfound > 99:
        print("Draw! Nothing to attack with units on both sides!")
        input()
        return
    if len(side_a):
        print(f"Side 1 has won!\n{oob_listing(side_a, True, status=True)}")
    elif len(side_b):
        print(f"Side 2 has won!\n{oob_listing(side_b, True, status=True)}")
    else:
        print("Draw!")
    input()


def battle_ws_by_distance(side_a, side_b):
    """
    Function launches attacks depending on distance between the groups.
    :param side_a: Objects of side a.
    :param side_b: Objects of side b.
    :return: Returns nothing.
    """
    weapon_choice = 0
    side_both = side_a + side_b
    print(f"\n{oob_listing(side_a + side_b, name=True, distance=True, status=True)}\n")
    for unit in side_both:
        weapon_choice = 0
        for weapon in unit.systems.copy():
            if eq_systems[unit.type][weapon][4] <= unit.distance <= eq_systems[unit.type][weapon][3]:
                if not eq_systems[unit.type][weapon][4] < 0:
                    weapon_choice = weapon

        if weapon_choice and unit.side == 1:
            battle_target_acquisition(side_b, unit, weapon_choice)
        elif weapon_choice and unit.side == 2:
            battle_target_acquisition(side_a, unit, weapon_choice)
        if unit.distance > 1:
            unit.distance -= 1
        unit.turn += 1
    if not weapon_choice:
        return 1
    return 0


def battle_target_acquisition(unit_list, unit, weapon):
    """
    Picks primary target depending on the vehicle type.
    :param unit_list: Objects of side b.
    :param unit: Object of side a attacking with weapon.
    :param weapon: Object of side a weapon.
    """

    # TODO Add also targeting by distance
    maximum = 0
    distance = 10
    target = False
    acquisition = eq_systems[unit.type][weapon][2]

    for enemy in unit_list:
        try:
            if acquisition == 4 and enemy.has_radar:
                maximum = enemy.type
                distance = enemy.distance
                target = enemy
            elif enemy.type in acquisition and enemy.type > maximum:
                maximum = enemy.type
                distance = enemy.distance
                target = enemy
        except TypeError:
            if enemy.type == acquisition and enemy.type > maximum:
                maximum = enemy.type
                distance = enemy.distance

                target = enemy

    if unit.attack(weapon, target) is None:
        for units in range(len(unit_list)):
            if unit_list[units] == target:
                unit_list.pop(units)
                return
    else:
        pass


# Eq System Category: {System: {Name str, dmg int, target int/tuple, range int, min range int}}
vehicles = {
    1: {1: ("MBT", (90, 1, 2, 3, 4)), 2: ("AFV", (91, 1, 2, 3, 4)), 3: ("IFV", (92, 1, 2, 3)),
        4: ("APC", (93, 1, 2, 3)),
        5: ("SAM", (94, 1, 2, 3, 5, 6, 7)), 6: ("MLB", (95, 1, 2, 3, 8, 9))},
    2: {1: ("Small Multirole Aircraft", (90, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
        2: ("Medium Multirole Aircraft", (91, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
        3: ("Large Multirole Aircraft", (92, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
        4: ("Large Heavy Aircraft", (93, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
        5: ("Very Large Heavy Aircraft", (94, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))},
    3: {1: ("Corvette", (90, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
        2: ("Frigate", (91, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
        3: ("Destroyer", (92, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
        4: ("Cruiser", (93, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
        5: ("Battlecruiser", (94, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
        6: ("Battleship", (95, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
        7: ("Light Carrier", (96, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
        8: ("Aircraft Carrier", (97, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))}
}
vehicles_internal = {1: "MBT", 2: "AFV", 3: "IFV", 4: "APC", 5: "SAM", 6: "MLB", 7: "Small Multirole Aircraft",
                     8: "Medium Multirole Aircraft", 9: "Large Multirole Aircraft", 10: "Large Heavy Aircraft",
                     11: "Very Large Heavy Aircraft", 12: "Corvette", 13: "Frigate", 14: "Destroyer", 15: "Cruiser",
                     16: "Battlecruiser", 17: "Battleship", 18: "Light Carrier", 19: "Aircraft Carrier"}
eq_systems = {
    1: {1: ("Smoke", -2, 0, 0, 0), 2: ("SK-APS", -3, 0, 0, 0), 3: ("HK-APS", -4, 0, 0, 0),
        4: ("ATGM", 3, (1, 3), 3, 0), 5: ("SR-SAM", 3, 2, 2, 0), 6: ("MR-SAM", 3, 2, 4, 0), 7: ("LR-SAM", 3, 2, 12, 3),
        8: ("MR-AShM", 5, 3, 4, 0), 9: ("LR-AShM", 5, 3, 6, 0), 90: ("tank gun", 5, 1, 2, 0),
        91: ("autocannon", 2, (1, 2), 2, 0), 92: ("heavy MG", 1, (1, 2), 2, 0), 93: ("light MG", 1, 1, 1, 0),
        94: ("crew handheld firearms", 1, 1, 1, 0), 95: ("crew handheld firearms", 1, 1, 1, 0)},
    2: {1: ("Flares", -2, 0, 0, 0), 2: ("Chaff", -2, 0, 0, 0), 3: ("ECM", -2, 0, 0, 0),
        4: ("EWS", -3, 0, 0, 0), 5: ("SRAAM", 4, 2, 2, 0), 6: ("MRAAM", 4, 2, 4, 0), 7: ("LRAAM", 4, 2, 12, 3),
        8: ("AGM", 4, 1, 3, 0), 9: ("MR-AShM", 5, 3, 4, 0), 10: ("SEAD", 5, 4, 4, 0),
        11: ("Cruise Missile", 3, 1, 5, 0), 12: ("Bomb", 2, 1, 1, 0), 13: ("GBU", 4, 1, 1, 0),
        90: ("coaxial cannon", 1, 2, 1, 0), 91: ("coaxial cannon", 2, 2, 1, 0), 92: ("coaxial cannon", 2, 2, 1, 0),
        93: ("coaxial cannon", 1, 2, 1, 0), 94: ("coaxial cannon", 1, 2, 1, 0)},
    3: {1: ("CIWS", -5, 2, 2, 0), 2: ("DEW", -7, 2, 2, 0), 3: ("ECM", -2, 0, 0, 0),
        4: ("Smoke", -2, 0, 0, 0), 5: ("Chaff", -2, 0, 0, 0), 6: ("SR-SAM", 3, 2, 2, 0), 7: ("MR-SAM", 3, 2, 4, 0),
        8: ("LR-SAM", 3, 2, 12, 3), 9: ("MR-AShM", 5, 3, 4, 0), 10: ("LR-AShM", 5, 3, 6, 0),
        11: ("Cruise Missile", 3, 1, 5, 0), 90: ("main battery", 1, (1, 2, 3), 1, 0),
        91: ("main battery", 1, (1, 2, 3), 1, 0), 92: ("main battery", 1, (1, 2, 3), 1, 0),
        93: ("main battery", 1, (1, 2, 3), 2, 0), 94: ("main battery", 1, (1, 2, 3), 3, 0),
        95: ("main battery", 1, (1, 2, 3), 4, 0), 96: ("auxiliary weapons", 1, (2, 3), 1, 0),
        97: ("auxiliary weapons", 1, (2, 3), 1, 0)}
}
state = ["KIA", "Heavily Damaged", "Major Damage taken", "Damaged", "Slightly damaged", "Scratched", "In nominal state",
         "Worried", "New", "Withdrawing"]


def welcome():
    """
    Introducing welcome!
    """
    version = "Welcome to Battle System Manager v0.8.8 (ALPHA)"
    print("=" * len(version), "\n", version, "\n", " " * ((len(version) - 13) // 2), "Made by Toonu\n",
          " " * ((len(version) - 21) // 2), "The Emperor of Iconia\n", " " * (len(version) // 2), "☩\n",
          " " * ((len(version) - 5) // 2), "☩☩☩☩☩\n", " " * (len(version) // 2), "☩\n", "≋" * len(version), "\n",
          sep="")


def oob_main(years=None):
    """
    Main Body of assigning assets.
    :param years: Lower and upper year limit of assets.
    """
    if years is None:
        years = [1975, 2020]
    first = []
    second = []
    battle_info = oob_battle_configuration(years)  # Basic battle configuration and default values.
    if battle_info[2] is not None:  # Changing default years.
        years = battle_info[2]
    print("Stage III: Adding Vehicles\n")
    for side in range(1, 3):  # Creates obj with numbered names and specifications of other functions.
        for i in range(battle_info[0][side]):  # Side a and b objects addition.
            if side == 1:
                first.append("asset{0}_{1}".format(side, i))
                first[i] = Asset("asset{0}_{1}".format(side, i),
                                 oob_asset_configuration(i, side, battle_info[1], years), side)
            else:
                second.append("asset{0}_{1}".format(side, i))
                second[i] = Asset("asset{0}_{1}".format(side, i),
                                  oob_asset_configuration(i, side, battle_info[1], years), side)
    a = first + second
    oob_equipment(a)
    oob_final(a, years)  # Finalizes and prints the OOB.
    clear()
    # Message.wait("", 9)
    battle_core(first, second)


def oob_battle_configuration(years):
    """
    Specify how many each side has and default year.
    :param years: Lower and upper year limit of assets.
    :return: Returns how many unit each side has, default year and lower/upper year limit of years.
    """
    sides = {}
    while True:
        welcome()
        print("Battle configuration mode: Assigning year of battle.")
        year = user_input(years[0], years[1], f"Specify default battle year ({years[0]} - {years[1]}): ", string=True,
                          check="[0-9]{4}-[0-9]{4}")  # Assigns new years when input is year-year.
        if isinstance(year, str) and year[4] == "-":  # Changing min max years to new values. If not, except.
            years = [int(year[0:4]), int(year[5:9])]
            continue

        clear()  # Specify units per side.
        welcome()
        print("Battle configuration mode: Assigning vehicles to their respective sides.")
        for side in range(1, 3):
            sides[side] = user_input(minimum=1, maximum=100, msg=f"Specify how many assets side {side} has: ")

        while True:  # Allows change of units per side.
            clear()
            welcome()
            print(f"Battle configuration mode: Confirming numbers.\nSide 1 | 2\nUnit {sides[1]} | {sides[2]}")
            response = user_input(msg="\nAre the numbers right? (1 YES / 0 NO): ")
            if response == 1 and year is not None:
                return sides, year, years
            while not response:
                response = user_input(1, 2, "What side is wrong? (1/2)")
                sides[response] = user_input(minimum=1, maximum=99, msg="How many assets this side has: ")


def oob_asset_configuration(number, side, year, years):
    """
    Specify each asset category, year and its type
    :param number: Specify asset object number.
    :param side: Specify asset side number.
    :param year: Default asset year accepted if not changed.
    :param years: Lower and upper year limit of assets.
    :return: Returns unit category (veh, air, sea), type (subtype of category) and year of production.
    """
    clear()  # Chooses unit category.
    category = user_input(1, 3, f"Asset configuration mode:\n\nasset{side}_{number}\nAsset #{number + 1} of {side} "
                                f"side.\nWhat category of vehicles you want to add?\n1 | Ground\n2 | Air\n3 | Naval\n"
                                f"Input: ")
    clear()  # Chooses unit type.
    print(f"Asset configuration mode:\n\nasset{side}_{number}\nAsset #{number + 1} of {side} side.\nType number of "
          f"asset you want to add to the order of battle: ")
    for i in range(1, len(vehicles[category]) + 1):  # Prints out all unit types of unit category.
        print(i, "=", vehicles[category][i][0], end=" | ")
    unit_type = user_input(maximum=len(vehicles[category]), msg="\nInput: ")

    clear()  # Chooses unit year.
    while True:
        print(f"Asset configuration mode:\n\nasset{side}_{number}\nAsset #{number + 1} of {side} side.\nWhat year is "
              f"the vehicle from. ({years[0]} - {years[1]})\nIn case the vehicle is from {year}, press enter.\nInput: ")
        new_year = user_input(years[0], years[1], enter=True)  # Assigns new non-default year for the unit.
        if new_year is not None and new_year != "":
            year = new_year
        return category, unit_type, year


def oob_equipment(a):
    """
    Equips units with systems in form of dictionary. Also enable launch of cloning function.
    :param a: All unit objects list.
    :return: Returns Nothing.
    """
    error = ""
    while True:
        for unit in a:
            while True:
                clear()
                print(f"Equipment mode: {error}\n")
                oob_listing(a, name=True)
                print("\nCurrently edited unit:", unit)
                for i in range(1, len(eq_systems[unit.type]) - len(vehicles[unit.type]) + 1):
                    print(i, "=", eq_systems[unit.type][i][0], end=" | ")
                print(f"\n\nTo select system N type its number N. Set amount of 0 to remove system N.\n"
                      f"TO FINISH {len(eq_systems[unit.type]) - len(vehicles[unit.type]) + 2}  "
                      f"CLONING MODE {len(eq_systems[unit.type]) - len(vehicles[unit.type]) + 1}  "
                      f"NEXT UNIT 0\nChoose system you want to add:", end=" ")
                system = user_input(maximum=len(eq_systems[unit.type]) - len(vehicles[unit.type]) + 2)
                if int(system) == len(eq_systems[unit.type]) - len(vehicles[unit.type]) + 2:
                    return
                elif not int(system):
                    break
                elif int(system) == len(eq_systems[unit.type]) - len(vehicles[unit.type]) + 1:
                    oob_cloning(a)
                if system in vehicles[unit.type][unit.external][1]:
                    amount = user_input(maximum=100, msg="What amount: ")
                    unit.add_system(system, int(amount))
                    error = ""
                else:
                    error = f"~~ERROR~~ Wrong system for this vehicle type! Vehicle can have these systems: " \
                            f"{vehicles[unit.type][unit.external][1]}"
            continue


# noinspection PyUnboundLocalVariable
def oob_cloning(a):
    """
    Duplicates equipped system dictionaries to other units.
    :param a: All unit objects list.
    :return: Returns nothing.
    """
    while True:
        clear()
        print("Cloning mode:\n")
        oob_listing(a, True, True)
        source = user_input(msg="\nChoose unit from which the items will be cloned by typing its number found in"
                                "\"assetX_Y\" of the unit.\nEq. 1_0 for asset1_0 | To Exit duplication mode, "
                                "hit enter.\n\nYour input: ", string=True, check="^[0-9]+_[0-9]+", enter=True)
        if source == "":
            clear()
            return
        try:
            source = "asset" + source
            clear()
            print("Cloning mode:\n")
            oob_listing(a, True, True)
            print("\nSource unit:", source)
            target = user_input(msg='Choose units to clone equipment to by typing their number separated by ","\n'
                                    'Eg. 1_1,2_0 for asset1_1 and asset2_0.\n\nYour input: ', string=True,
                                check="([0-9]+_[0-9]+)+")
            for target_unit in target.split(","):
                for source_unit in a:
                    if source_unit.name == source:
                        source_systems = source_unit.systems
                        source_type = source_unit.type
                for unit in a:
                    if unit.name == "asset" + target_unit and unit.type == source_type:
                        unit.systems = source_systems.copy()
                        unit.systems[vehicles[unit.type][unit.external][1][0]] = 1
                        for system in unit.systems.copy():
                            if system not in vehicles[unit.type][unit.external][1]:
                                unit.systems.pop(system)
            clear()
            print("Cloning mode:\n")
            oob_listing(a, True, True)
            exit_mode = user_input(msg="\nExit cloning mode? (1 YES / 0 NO)\n\nYour input:")
            if exit_mode:
                clear()
                return
        except TypeError:
            continue


def oob_listing(a, name=False, year=False, status=False, distance=False, equip=True):
    """
    Lists all units and their equipment, side, year or name.
    :param a: All unit objects list.
    :param equip: Prints also the unit equipment if True.
    :param distance: Prints also the unit distance if True.
    :param status: Prints also the unit status if True.
    :param name: Prints also the unit name if True.
    :param year: Prints also the unit year if True.
    """
    for unit in a:
        message = f"Side {unit.side} |"
        ending = f" {unit.typename}"
        if year:
            message += f" {unit.year} |"
        if name:
            message += f" {unit.name} |"
        if status:
            message += f" {unit.state} |"
        if distance:
            message += f" {unit.distance} |"
        if equip:
            ending += f" equipped with: "

        print(message + ending, end="")
        if equip:
            for thing, amount in unit.systems.items():
                print(eq_systems[unit.type][thing][0], amount, end=", ")
            print()


def oob_final(a, years):
    """
    Checks if everything is set properly after printing final order of battle. Leads to battle part of code.
    :param a: All unit objects list.
    :param years: Upper and lower year limit.
    :return: Returns nothing
    """
    while True:
        clear()
        print("Final Order of Battle:\n")
        oob_listing(a, year=True)
        response = user_input(msg="\nIs everything correct? (1 YES / 0 NO): \nBattle will commence if yes: ")
        if not response:
            wrong_system = user_input(1, 3, "What is wrong?\n1 | Unit composition\n2 | Unit Equipment\n3 | Unit years"
                                            "\nYour input: ")
            if wrong_system == 1:
                oob_mod_asset_type(a, years)
            elif wrong_system == 2:
                oob_equipment(a)
            elif wrong_system == 3:
                oob_mod_year(a, years)
        else:
            return


def oob_mod_asset_type(a, years):
    """
    Changes object unit types and erases its equipment.
    :param a: All unit objects list.
    :param years: Upper and lower year limit.
    :return: Returns nothing
    """
    while True:
        clear()
        print("Unit modification tool:\n")
        oob_listing(a, name=True, year=True)
        response = user_input(msg="\nChoose which asset to edit by typing its number.\nEg. 1_0 for asset1_0.\nTo stop "
                                  "changing assets, type 0.\n\nYour input: ", string=True, check="^[0-9]+_[0-9]+")
        if not response:
            return
        else:
            for unit in a:
                if not isinstance(response, int) and unit.name == "asset" + response:
                    unit.systems = {99: 1}
                    batch = oob_asset_configuration(unit.type, unit.side, unit.year, years)
                    unit.year = batch[2]
                    unit.reliability = unit.year - 1900
                    unit.internal = unit.asset_assign(batch)
                    unit.typename = vehicles[batch[0]][batch[1]][0]
                    unit.external = batch[1]
                    unit.type = batch[0]


def oob_mod_year(a, years):
    """
    Function changes unit year of production.
    :param a: All unit objects list.
    :param years: Upper and lower year limit.
    :return: Returns nothing.
    """
    while True:
        clear()
        print("Year of unit editing:\n")
        oob_listing(a, year=True, name=True)
        response = user_input(msg="\nChoose which asset to edit by typing its number.\nEg. 1_0 for asset1_0.\nTo stop "
                                  "changing years, type 0.\n\nYour input: ", maximum=0, string=True,
                              check="^[0-9]+_[0-9]+")
        if not response:
            return
        else:
            new_year = user_input(years[0], years[1], f"Choose new year of unit ({years[0]} - {years[1]}): ")
            for unit in a:
                if not isinstance(response, int) and unit.name == "asset" + response:
                    unit.year = new_year
                    unit.reliability = new_year / 3000


# noinspection PyShadowingNames,PyUnboundLocalVariable
def clear():
    """
    Clears the terminal
    """
    import platform
    from os import system
    if platform.system() == "Windows" or platform.system() == "Linux":
        clear = lambda: system("cls")
    elif platform.system() == "Darwin":
        clear = lambda: system("clear")
    clear()


def user_input(minimum=0, maximum=1, msg="", enter=False, string=False, check=""):
    """
    User input function.
    :param minimum: Lower limit to number check.
    :param maximum: Upper limit to number check.
    :param msg: Message printed when asking for input.
    :param enter: If enter is permitted as input.
    :param string: If string is permitted as input.
    :param check: String input must have same format as check using RegEx.
    :return: Returns user input.
    """
    from re import match
    while True:
        value = input(msg)
        try:
            if string and match(check, value) is not None:
                return value
            elif minimum <= int(value) <= maximum:
                return int(value)
            else:
                print("Invalid input! Number out of range! Please retry.")
        except ValueError:
            if enter and value == "":
                return value
            print("Invalid input! Please retry.")


def start(bugs=False):
    """
    Starting function for the whole program.
    :param bugs: Enables bug logging for user. Shows error when the program crashes.
    """
    if bugs:
        try:
            oob_main()
        except Exception as e:
            print(f"Program crashed with this error: {e}, {type(e)}, {e.args}, \nPlease report the error to the "
                  f"developers.\nRe-launching program now.\n\n")
            oob_main()
    else:
        oob_main()


notfound = 0
default = Asset("default", [1, 1, 1999], 1)
default.systems[1] = 2
start()

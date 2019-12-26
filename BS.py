import os
import random
import time


class Message:
    """
    Message is printing messages
    """

    @staticmethod
    def message(msg_type, vehicle, system=1, headline="", dot=True, dots=True, repeat=0, header=True, wait=True):
        """
        Prints various random messages from the message dict.
        :param headline: Header subject message.
        :param wait: Disable wait message.
        :param msg_type: Type of message from the dict.
        :param vehicle: Vehicle obj affected.
        :param header: Disable header message.
        :param system: Vehicle obj weapon system.
        :param dot: Triple dots in wait message.
        :param dots: Dots in wait message.
        :param repeat: How many triple dots are repeated in wait message.

         #  0 | Battle start, 1 | Death, 2 | Gun malfunc, 3 | Missile failure, 4 | Hit, 5 |
        """
        messages = {0: ["The battle is about to start.", "The battle is commencing.",
                        "Both forces deployed and started advancing towards each other",
                        "After long waiting, the order to attack has finally came..."],
                    1: [f"Your {vehicle.typename.lower()} has been utterly crushed by your foes.",
                        f"{vehicle.typename.capitalize()} status: Presumed KIA.",
                        f"{vehicle.typename.capitalize()} killed in action.",
                        f"{vehicle.typename.capitalize()} disappeared from your battle control screen.",
                        f"{vehicle.typename.capitalize()} couldn't stood against such strong enemy."],
                    2: [f"Contact was too slippery.", f"Must have been poor luck.", f"Shot lost the mark.",
                        f"{vehicle.define_system(system)} failed to connect."],
                    3: [f"Your {vehicle.define_system(system)} has failed to lock on target after launch.",
                        f"{vehicle.define_system(system)} has run out of fuel and auto destructed itself.",
                        f"{vehicle.define_system(system)} missed the target",
                        f"{vehicle.define_system(system)} failed to lit its engine",
                        f"{vehicle.define_system(system)} failed to connect.",
                        f"{vehicle.define_system(system)} is heading towards the sun now",
                        f"Enemy countermeasures were too much effective.",
                        f"{vehicle.define_system(system)} went and whiffed em’.",
                        f"Failure to decouple."],
                    4: ["Target hit.", "Target damaged."]}
        if header:
            Message.header(header)
        if wait:
            Message.wait(messages[msg_type][random.randint(1, len(messages[msg_type]))], i=repeat, dot=dot, dots=dots)
        if not header and wait:
            Message.wait(messages[msg_type][random.randint(1, len(messages[msg_type]))], i=0, dot=False, dots=False)

    @staticmethod
    def kill(unit_type):
        """
        Prints killing message.
        :param unit_type: Unit type that was killed.
        """
        kill = {1: [f"“Nailed em! He’s finished.”", f"Lad’s a fireball now.", f"Scratch one!",
                    f"Target crew bailed out", f"Our shot penetrated the enemy and destroyed everything inside."],
                2: [f"“Nailed em! He’s finished.”", f"Lad’s a fireball now.", f"Pilot knocked out.",
                    f"Plane burnt down.", f"Engine Died: Fuel Starvation", f"Bandit down, no chute."],
                3: [f"“Nailed em! He’s finished.”", f"Enemy is sinking.", f"Scratch one!",
                    f"Enemy has huge hole in his hull", f"Target is taking water and abandoning the ship was ordered."]}
        Message.wait(kill[unit_type][random.randint(1, len(kill))])

    @staticmethod
    def header(craft):
        """
        Prints header message.
        :param craft: Headline of header message.
        """
        if isinstance(craft, str):
            print("Side:  ", craft)
        else:
            print("Side:  ", craft.name)
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

    @staticmethod
    def fire(system, vehicle, source):
        """
        Printing firing messages depending on the variables.
        :param system: Weapon system fired.
        :param vehicle: Vehicle which was fired upon.
        :param source: Vehicle which fired.
        """
        if source.systemtype in (1, 2):
            fire = {1: f"{system} was fired at {vehicle} from your {source.typename}"}
        elif source.systemtype == 3:
            fire = {1: f"{system} was fired at {vehicle} from your {source.typename}"}
        elif source.systemtype == 4:
            fire = {1: f"{system} was fired at {vehicle} from your {source.typename}"}
        Message.wait(fire[random.randint(1, len(fire))], dots=False)


class Asset:
    """
    Asset objects are the units itself.
    """

    def __init__(self, name, batch, status, side):
        self.name = name
        self.type = self.asset_assign(batch)  # Internal asset type
        self.typename = vehicles[batch[0]][batch[1]]  # Asset name Eg. MBT
        self.systemtype = self.system_type()  # 1 ground 2 radar 3 air 4 sea
        self.state = status  # How much alive asset is
        self.statename = state[self.state]  # How much alive asset is in normal name
        self.side = side  # Fighting side
        self.year = batch[2]  # Year of origin
        self.reliability = self.year / 3000  # Reliability of its WS
        self.systems = {}

    def __str__(self):
        return str(self.name + "_" + self.typename + " - STATE-" + str(self.state))

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
        return eq_systems[self.systemtype][self.systems[system]]

    def system_type(self):
        """
        Assigns system per obj type
        :return: Returns obj system type which sets weapons it can equip.
        """
        if self.type <= 4 or self.type == 6:
            return 1
        elif self.type == 5:
            return 2
        elif 7 <= self.type <= 11:
            return 3
        elif 12 <= self.type:
            return 4

    @staticmethod
    def asset_assign(asset_type):
        """
        Assign internal type of the unit.
        :param asset_type: Unit batch list.
        :return: Returns unit internal type also specified in global vehicle_internals.
        """
        if asset_type[0] == 1:
            result = asset_type[1]
        if asset_type[0] == 2:
            result = asset_type[1] + len(vehicles[1])
        elif asset_type[0] == 3:
            result = asset_type[1] + len(vehicles[1]) + len(vehicles[2])
        return result

    def attack(self, system, target, source):
        """
        Function for reducing asset weapon fired last turn and starting its target defensive method.
        :param system: Weapon system used.
        :param target: Target of the fired weapon system.
        :param source: Unit object that fired.
        :return: Returns nothing. yet...
        """
        if not target:
            print(f"{system} has no target to attack.")
            return
        Message.fire(system_name(self.systemtype, system), target.typename, source)
        self.systems[system] -= 1
        if self.systems[system] == 0:
            self.systems.pop(system)
        target.defense(system, self)
        pass  # TODO

    def defense(self, system, attacker):
        """
        Function of hitting probability and decreasing unit status after hit.
        :param system: Attacking weapon system.
        :param attacker: Attacking vehicle.
        """

        # TODO Add the attacker as enemy next firing?
        print(f"{system} attacked by {attacker}")
        pass


def battle_core(side_a, side_b):
    """
    Core of the battle algorithm.
    :param side_a: Objects of side a.
    :param side_b: Objects of side b.
    """
    print("\n")
    Message.message(0, default, header="unknown")
    won = False
    distance = 11
    while not won:
        distance -= 1
        battle_airland_battle(side_a, side_b, distance)


def battle_airland_battle(side_a, side_b, distance):
    """
    Function launches attacks depending on distance between the groups.
    :param side_a: Objects of side a.
    :param side_b: Objects of side b.
    :param distance: Distance between the groups.
    :return: Returns nothing.
    """
    for a in side_a:  # Air battle first
        distance = 0
        if a.systemtype == 3:
            for weapon in a.systems:
                if weapon == 5 and distance > 2:  # SRAAM on short distance
                    battle_target_acquisition(side_b, a, weapon)
                elif weapon == 6 and distance > 4:  # MRAAM on medium range
                    battle_target_acquisition(side_b, a, weapon)
                elif weapon == 7:  # LRAAM on long range
                    battle_target_acquisition(side_b, a, weapon)
                elif distance > 8:  # guns on short distance
                    battle_target_acquisition(side_b, a, 99)
                a.distance -= 1
                return


def battle_target_acquisition(side_b, unit, weapon):
    """
    Picks primary target depending on the vehicle type.
    :param side_b: Objects of side b.
    :param unit: Object of side a attacking with weapon.
    :param weapon: Object of side a weapon.
    """
    maximum = 0
    target = False
    acquisition = battle_weapon_type(unit, weapon)

    for b in side_b:
        if b.systemtype == acquisition and b.type > maximum:
            maximum = b.type
            target = b

    unit.attack(target, unit, weapon)


def battle_weapon_type(unit, weapon):
    """
    Returns type of weapon target - 1 veh, 2 radar, 3 air, 4 sea
    :param unit: Asset obj.
    :param weapon: Asset obj weapon fired.
    :return: Returns units targeted by this weapon.
    """
    if unit.systemtype == 1:  # Ground units attacking ground units
        return 1
    elif unit.systemtype == 2:  # MLB units against ship 4 and air 3
        if weapon == 7:
            return 4
        return 3
    elif unit.systemtype == 3:  # Planes against 1 vehicles, 4 ships, 2 radars and 3 air
        if weapon in (8, 11, 12, 13):
            return 1
        elif weapon == 9:
            return 4
        elif weapon == 10:
            return 2
        return 3
    elif unit.systemtype == 4:  # Ships against 3 air, 1 ground, 4 ships
        if weapon in (7, 8, 9):
            return 3
        elif weapon == 10:
            return 1
        return 4


def system_name(vehicle, system):
    """
    Function converts system number into its name.
    :param vehicle: Vehicle subtype category.
    :param system: System of vehicle subtype category.
    :return: Returns str name of system of the vehicle.
    """
    return eq_systems[vehicle][system]


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
    2: {0: "None", 1: "Smoke", 2: "HK-APS", 3: "SK-APS", 4: "SR-SAM", 5: "MR-SAM", 6: "LR-SAM", 7: "AShM"},
    3: {0: "None", 1: "Flares", 2: "Chaff", 3: "ECM", 4: "EWS", 5: "SRAAM", 6: "MRAAM", 7: "LRAAM", 8: "AGM", 9: "AShM",
        10: "SEAD", 11: "Cruise Missile", 12: "Bomb", 13: "GBU"},
    4: {0: "None", 1: "CIWS", 2: "DEW", 3: "ECM", 4: "Smoke", 5: "Chaff", 6: "AShM", 7: "SR-SAM", 8: "MR-SAM",
        9: "LR-SAM", 10: "Cruise Missile"}
}
state = {0: "KIA", 1: "Heavily Damaged", 2: "Major Damage taken", 3: "Light Damage", 4: "Scratched", 5: "State Nominal",
         6: "RTB", 7: "MIA", 8: "Disappeared"}


def welcome():
    """
    Introducing welcome!
    """
    version = "Welcome to Battle System Manager v0.7.5 (ALPHA)"
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
                                 oob_asset_configuration(i, side, battle_info[1], years), 5, side)
            else:
                second.append("asset{0}_{1}".format(side, i))
                second[i] = Asset("asset{0}_{1}".format(side, i),
                                  oob_asset_configuration(i, side, battle_info[1], years), 5, side)
    a = first + second
    oob_equipment(a)
    oob_final(a, years)  # Finalizes and prints the OOB.
    clear()
    Message.wait("", 9)
    battle_core(first, second)


def oob_battle_configuration(years):
    """
    Specify how many each side has and default year.
    :param years: Lower and upper year limit of assets.
    :return: Returns how many unit each side has, default year and lower/upper year limit of years.
    """
    sides = {}
    while True:
        print("Battle configuration mode:\n\nStage I: Assigning year of battle.")
        year = user_input(years[0], years[1], f"Specify year ({years[0]} - {years[1]}): ", string=True,
                          check="[0-9]{4}-[0-9]{4}")  # Assigns new years when input is XXXX-YYYY.
        if isinstance(year, str) and year[4] == "-":  # Changing min max years to new values. If not, except.
            years = [int(year[0:4]), int(year[5:9])]
            continue

        clear()  # Specify units per side.
        print("Battle configuration mode:\n\nStage II: Assigning vehicles to their respective sides.")
        for side in range(1, 3):
            sides[side] = user_input(minimum=1, msg=f"Specify how many assets side {side} has: ")

        while True:  # Allows change of units per side.
            clear()
            print(f"Battle configuration mode:\n\nSide 1: {sides[1]} units\nSide 2: {sides[2]} units\nYear: {year}")
            response = user_input(0, 1, "\nAre the numbers right? (1 YES / 0 NO)\nInput: ")
            if response == 1 and year is not None:
                return sides, year, years
            while not response:
                response = user_input(1, 2, "What side is wrong? (1/2)")
                sides[response] = user_input(minimum=1, msg="How many assets this side has?")


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
        print(i, "=", vehicles[category][i], end=" | ")
    unit_type = user_input(0, len(vehicles[category]), "\nInput: ")

    clear()  # Chooses unit year.
    while True:
        print(f"Asset configuration mode:\n\nasset{side}_{number}\nAsset #{number + 1} of {side} side.\nWhat year is "
              f"the vehicle from. ({years[0]} - {years[1]})\nIn case the vehicle is from {year}, press enter.\nInput: ")
        new_year = user_input(years[0], years[1], "", enter=True)  # Assigns new non-default year for the unit.
        if new_year is not None and new_year != "":
            year = new_year
        return category, unit_type, year


def oob_equipment(a):
    """
    Equips units with systems in form of dictionary. Also enable launch of cloning function.
    :param a: All unit objects list.
    :return: Returns Nothing.
    """
    restart = True
    while restart:
        for unit in a:
            while True:
                clear()
                print("Equipment mode:\n")
                oob_listing(a, name=True)
                print("\nCurrently edited unit:", unit)
                for i in range(len(eq_systems[unit.systemtype])):
                    print(i, "=", eq_systems[unit.systemtype][i], end=" | ")
                print(f"\n\nTo move to the next unit, select 0. To remove item, set "
                      f"item type and amount to 0. To finish, press {len(eq_systems[unit.systemtype]) + 1}.\nTo enter "
                      f"cloning mode, type {len(eq_systems[unit.systemtype])}.\n"
                      f"Choose system the vehicle has equipped:", end=" ")
                system = user_input(0, len(eq_systems[unit.systemtype]) + 1)
                if int(system) == len(eq_systems[unit.systemtype]) + 1:
                    return
                elif not int(system):
                    break
                elif int(system) == len(eq_systems[unit.systemtype]):
                    oob_cloning(a)
                else:
                    amount = user_input(msg="Specify how many: ")
                    unit.add_system(system, int(amount))
            continue


# noinspection PyUnboundLocalVariable
def oob_cloning(a):
    """
    Duplicates equipped syste dictionaries to other units.
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
        source = "asset" + source
        clear()
        print("Cloning mode:\n")
        oob_listing(a, True, True)
        print("\nSource unit:", source, end="\n")
        target = user_input(msg='Choose units to clone equipment to by typing their number separated by ","\nEg. 1_1,'
                                '2_0 for asset1_1 and asset2_0.\n\nYour input: ', string=True, check="([0-9]+_[0-9]+)+")
        for target_unit in target.split(","):
            for source_unit in a:
                if source_unit.name == source:
                    source_systems = source_unit.systems
                    source_type = source_unit.systemtype
            for unit in a:
                if unit.name == "asset" + target_unit and unit.systemtype == source_type:
                    unit.systems = source_systems.copy()
        clear()
        print("Cloning mode:\n")
        oob_listing(a, True, True)
        exit_mode = user_input(0, 1, "\nExit cloning mode? (1 YES / 0 NO)\n\nYour input:")
        if exit_mode:
            clear()
            return


def oob_listing(a, name=False, year=False):
    """
    Lists all units and their equipment, side, year or name.
    :param a: All unit objects list.
    :param name: Prints also the unit name if True.
    :param year: Prints also the unit year if True.
    """
    for unit in a:
        if year and name:
            print(f"Side {unit.side} | {unit.year} | {unit.name} | {unit.typename} equipped with:", end=" ")
        elif year:
            print(f"Side {unit.side} | {unit.year} | {unit.typename} equipped with:", end=" ")
        elif name:
            print(f"Side {unit.side} | {unit.name} | {unit.typename} equipped with:", end=" ")
        else:
            print(f"Side {unit.side} | {unit.typename} equipped with:", end=" ")
        if not unit.systems == {}:
            for thing, amount in unit.systems.items():
                print(eq_systems[unit.systemtype][int(thing)], amount, end=", ")
            print()
        else:  # In case no weapons at specific unit.
            print("only its own weapon system.")


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
        oob_listing(a, False, True)
        response = user_input(0, 1, "\nIs everything correct? (1 YES / 0 NO): \nBattle will commence if yes: ")
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
                    unit.systems = {}
                    batch = oob_asset_configuration(unit.type, unit.side, unit.year, years)
                    unit.year = batch[2]
                    unit.reliability = unit.year / 3000
                    unit.type = unit.asset_assign(batch)
                    unit.typename = vehicles[batch[0]][batch[1]]
                    unit.systemtype = unit.system_type()


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
                                  "changing years, type 0.\n\nYour input: ", minimum=0, maximum=0, string=True,
                              check="^[0-9]+_[0-9]+")
        if not response:
            return
        else:
            new_year = user_input(years[0], years[1], f"Choose new year of unit ({years[0]} - {years[1]}): ")
            for unit in a:
                if not isinstance(response, int) and unit.name == "asset" + response:
                    unit.year = new_year
                    unit.reliability = new_year / 3000


def clear():
    """
    Clears the terminal
    """
    import platform
    if platform.system() == "Windows" or platform.system() == "Linux":
        clear = lambda: os.system("cls")
    elif platform.system() == "Darwin":
        clear = lambda: os.system("clear")
    clear()


def user_input(minimum=0, maximum=100, msg="", enter=False, string=False, check=""):
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
            welcome()
            oob_main()
        except Exception as e:
            print(f"Program crashed with this error: {e}, {type(e)}, {e.args}, \nPlease report the error to the "
                  f"developers.\nRe-launching program now.\n\n")
            welcome()
            oob_main()
    else:
        welcome()
        oob_main()


default = Asset("default", [1, 1, 1999], 5, 1)
default.systems[1] = 2
start()

"""
BS 1.0
"""

import random
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


def welcome():
    """
    Introducing welcome!
    """
    headline = f"Welcome to Battle System Manager v 0.9.2 (ALPHA)"
    message = f"{headline}\n" \
              f"{' ' * ((len(headline) // 2) + 7)}Made by Toonu\n" \
              f"{' ' * ((len(headline) // 2) + 1)}The Emperor of Iconia\n" \
              f"{' ' * ((len(headline) // 2) - 10)}With the help of Red, Litz and Sleepy"
    return message


def oob_input(check, minimum=0, maximum=1):
    try:
        if minimum <= int(check.text) <= maximum:
            return True
        else:
            return False
    except ValueError:
        return False


class Message:
    """
    Message is printing random messages
    """

    def battle_start(self, dot=False):
        """
        Prints
        """
        text = ["The battle is about to start.", "The battle is commencing.",
                "Both forces deployed and started advancing towards each other",
                "After long waiting, the order to attack has finally came..."]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    def fail_gun(self, unit, system_num, dot=False):
        """
        Prints
        """
        text = [f"{unit} | Contact was too slippery and the rounds bounced.",
                f"{unit} | Must have been poor luck, rounds haven't penetrated.",
                f"{unit} | Shots lost the mark.",
                f"{unit} | No penetration",
                f"{unit} | No good hits on the target.",
                f"{unit} | Rounds haven't even scratched the enemy plates.",
                f"{unit} | Shot missed by a country mile.",
                f"{unit} | {unit.define_system(system_num)} failed to connect and couldn't have been fired.",
                f"{unit} | {unit.define_system(system_num)} malfunctioned."]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    def fail_missile(self, unit, system, dot=False):
        """
        Prints
        """
        text = [f"{unit} | The {unit.define_system(system)} has failed to lock onto the target after launch.",
                f"{unit} | {unit.define_system(system)} has run out of fuel and auto destructed itself.",
                f"{unit} | {unit.define_system(system)} failed to lit its engine.",
                f"{unit} | {unit.define_system(system)} failed to connect and malfunctioned.",
                f"{unit} | Enemy countermeasures were too much effective and misguided the "
                f"{unit.define_system(system)} into the surface.",
                f"{unit} | {unit.define_system(system)} went and whiffed em’.",
                f"{unit} | Failure to decouple.",
                f"{unit} | Failure to launch.."]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    def hit(self, unit, target, system, damage, dot=False):
        """
        Prints
        """
        text = [f"{unit.name} | >>> {target.typename.lower()} {target.name} using "
                f"{unit.define_system(system)} with {damage} dmg."]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    def ending(self, dot=False):
        """
        Prints
        """
        text = ["End of report.\nSigned Electronically", "End of report.\nProceed with your operation."]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    def miss_missile(self, unit, system, dot=False):
        """
        Prints
        :param unit:
        :param dot:
        :param system:
        """
        text = [f"{unit} | {unit.define_system(system)} missed the target.",
                f"{unit} | {unit.define_system(system)} is heading towards the sun now."]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    def miss_gun(self, unit, system, dot=False):
        """
        Prints
        :param unit:
        :param dot:
        :param system:
        """
        text = [f"{unit} | {unit.define_system(system)} shots missed the target.",
                f"{unit} | {unit.define_system(system)} FCS calculated the enemy speed with error and missed.",
                f"{unit} | {unit.typename} crew miscalculated the enemy movement and missed.",
                f"{unit} | {unit.define_system(system)} FCS error margin was too high.",
                f"{unit} | Missed the mark, trying again."]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    def kill(self, unit, dot=False):
        """
        Prints
        """
        text = {
            1: [f"KILL {unit} | “Nailed em! The {unit.typename}’s finished.”",
                f"KILL {unit} | Lad’s a fireball now. ({unit.name})",
                f"KILL {unit} | Scratch one, he's finished! ({unit.name})",
                f"KILL {unit} | Target crew bailed out! ({unit.name})",
                f"KILL {unit} | Our shot penetrated the enemy and destroyed everything inside. ({unit.name})",
                f"KILL {unit} | The {unit.typename} has been utterly crushed by his foes. ({unit.name})",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} status: Presumed KIA.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} killed in action.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} disappeared from battle control screen.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} couldn't stood against such strong enemy."],
            2: [f"KILL {unit} | “Nailed em! The {unit.typename}’s finished.”",
                f"KILL {unit} | Lad’s a fireball now. ({unit.name})",
                f"KILL {unit} | Pilot of the {unit.typename} knocked out. ({unit.name})",
                f"KILL {unit} | Plane burnt down. ({unit.name})",
                f"KILL {unit} | Engine of {unit.typename} Died: Fuel Starvation ({unit.name})",
                f"KILL {unit} | Bandit down, no chute to be seen. ({unit.name})",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} status: Presumed KIA.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} disappeared from battle control screen.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} killed in action.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} couldn't stood against such strong enemy."
                ],
            3: [f"KILL {unit} | “Nailed em! The {unit.typename}’s finished.”",
                f"KILL {unit} | Enemy is sinking. ({unit.name})",
                f"KILL {unit} | Scratch one {unit.typename}! ({unit.name})",
                f"KILL {unit} | Enemy has huge hole in his hull! ({unit.name})",
                f"KILL {unit} | Target {unit.typename} is taking water and abandoning the ship was ordered! "
                f"KILL {unit} | They’ve gone to the Krusty Krab and never returned. ({unit.name})",
                f"KILL {unit} | They’re going under, we got em! ({unit.name})",
                f"KILL {unit} | The target {unit.typename} has achieved Salvation, by force. ({unit.name})",
                f"KILL {unit} | May Neptune have mercy on them. ({unit.name})",
                f"KILL {unit} | She got shoved into Davy Jones’ locker by the Sea Chad. ({unit.name})",
                f"KILL {unit} | “Something something crisp white sheets.” ({unit.name})",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} status: Presumed KIA.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} killed in action.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} disappeared from battle control screen.",
                f"KILL {unit} | {unit.typename.capitalize()} {unit.name} couldn't stood against such strong enemy."
                ]}
        if dot:
            self.dotted()
        print(text[unit.type][random.randint(0, len(text) - 1)])

    def critical(self, unit, system, dot=False):
        """
        Prints
        """
        text = [f"{unit} | Critical hit!",
                f"{unit} | The enemy has been hit precisely into weakspot!",
                f"{unit} | Devastating blow!",
                f"{unit} | The {unit.typename} {unit.name} has been hit precisely into weakspot!",
                f"{unit} | {unit.define_system(system)} critically hit the enemy"]
        if dot:
            self.dotted()
        print(text[random.randint(0, len(text) - 1)])

    @staticmethod
    def dotted():
        """
        Prints the message with dots and waiting.
        """
        for i in range(random.randint(3, 6)):
            print("." * i, end="")
            time.sleep(0.8)
        print()

    @staticmethod
    def report(msg=""):
        """
            Prints the message in a report.
            :param msg: Message to print as report name.
            """
        if msg != "":
            print(msg)
        else:
            print("")
        print("Report:", random.randint(25000, 300000), time.strftime("       %D-%H:%M:%S", time.localtime()))
        print("        Confidental eyes only\n         Classified Document\n   To OPFOR, MoD, AFHC, TLBC, BCTC\n")


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
        self.state = vehicles[batch[0]][batch[1]][2]  # How much alive asset is
        self.statename = self.set_state()  # How much alive asset is in normal name
        self.side = side  # Fighting side
        self.year = batch[2]  # Year of origin
        self.reliability = (self.year - 1945) // 2  # Reliability of its WS
        self.systems = self.systems_ammo()
        self.distance = self.distance_per_side()
        self.turn = 1
        self.has_radar = self.has_radar_fn()

    def __str__(self):
        return str(f"{self.name}_{self.typename} - State: {str(self.statename)} | Dist: {self.distance}")

    def distance_per_side(self):
        """
        Distance
        :return:
        """
        if self.side == 1:
            return 6
        else:
            return -6

    def systems_ammo(self):
        """
        Returns ammunition for specfied system
        :return:
        """
        if self.type == 2:
            return {89 + self.external: 10}
        elif self.type == 3:
            return {89 + self.external: 120}
        elif self.type == 1 and self.external == 1:
            return {89 + self.external: 45}
        elif self.type == 1 and self.external in (2, 3):
            return {89 + self.external: 120}
        elif self.type == 1 and self.external == 4:
            return {89 + self.external: 240}
        elif self.type == 1:
            return {89 + self.external: 80}

    def set_state(self):
        """
        Sets unit state name
        :return:
        """
        result = 9
        if vehicles[self.type][self.external][2] == 4 and self.state != 9:
            result = state[self.state * 2]
        elif vehicles[self.type][self.external][2] == 6 and self.state != 9:
            result = state[round(self.state * 1.25)]
        elif vehicles[self.type][self.external][2] == 8 and self.state != 9:
            result = state[self.state]
        elif vehicles[self.type][self.external][2] == 10 and self.state != 9:
            result = state[round(self.state / 1.25)]
        elif vehicles[self.type][self.external][2] == 16 and self.state != 9:
            result = state[self.state // 2]
        elif self.state != 9:
            result = state[round(self.state / 2.5)]
        if self.state < vehicles[self.type][self.external][2] // 2:
            print(f"{self.name} {self.typename} withdrawing!")
            result = state[9]
        return result

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

    def attack(self, side_a, side_b):
        """

        :param side_b:
        :param side_a:
        :return: Returns None if nothing could have been attacked, if something was attacked, returns
        """
        attack_result = (0, 0), 0
        target = 0
        cont = False
        while len(side_b) > 0 and len(side_a) > 0:
            target = (side_a + side_b)[random.randint(0, len(side_a + side_b) - 1)]
            if self.systems is None:
                self.statename = "Withdrawing"
            if target.side != self.side:
                maximum = 0
                best_system = 0
                for system in self.systems:
                    cont = False
                    try:
                        if target.has_radar and eq_systems[self.type][system][2] == 4 and \
                                eq_systems[self.type][system][3] >= abs(self.distance - target.distance) >= \
                                eq_systems[self.type][system][4]:
                            cont = True
                        elif target.type in eq_systems[self.type][system][2] and eq_systems[self.type][system][3] >= \
                                abs(self.distance - target.distance) >= eq_systems[self.type][system][4]:
                            cont = True
                    except TypeError:
                        if eq_systems[self.type][system][2] == target.type and eq_systems[self.type][system][3] >= \
                                abs(self.distance - target.distance) >= eq_systems[self.type][system][4]:
                            cont = True
                    if cont and eq_systems[self.type][system][1] > maximum:  # getting max damage weapon
                        maximum = eq_systems[self.type][system][1]
                        best_system = system
                if cont:
                    self.systems[best_system] -= 1
                    if self.systems[best_system] <= 0:
                        self.systems.pop(best_system)
                    probability = self.probability(self, best_system)
                    if probability < 30:
                        self.failure(best_system, probability, target)
                    else:
                        attack_result = target.defense(self, best_system, probability)
                        self.failure(best_system, attack_result[0], target, attack_result[1])
                    break
                break
            else:
                continue

        self.turn += 1
        if self.statename == "Withdrawing":  # Withdrawal
            if self.side == 1:
                self.distance += 2
            else:
                self.distance -= 2
            if self.distance < -9 or self.distance > 9:
                global retreated
                retreated.append(self)
                return 5, self
        if self.side == 1 and self.pursue(side_b) and self.distance < -9:
            self.distance -= 2
        elif self.side == 2 and self.pursue(side_a) and self.distance > 9:
            self.distance += 2
        elif self.distance > 0 and self.side == 1:
            self.distance -= 1
        elif self.distance < 0 and self.side == 2:
            self.distance += 1

        return attack_result[0], target

    @staticmethod
    def pursue(side):
        """
        :return:
        """
        pursue = True
        for a in side:
            if a.statename != "Withdrawing":
                pursue = False
        return pursue

    def failure(self, system, fail, target, damage=0):
        """
        Fail messages.
        :param target:
        :param damage:
        :param system:
        :param fail:
        """
        if fail == 1:  # Mafunction message
            if system > 89 or self.type == 3 and system == 1:
                message.fail_gun(self, system)
            else:
                message.fail_missile(self, system)
        elif fail == 2:
            if system > 89 or (self.type == 3 and system == 1):
                message.miss_gun(self, system)
            else:
                message.miss_missile(self, system)
        elif fail == 3:
            message.hit(self, target, system, damage)
        elif fail == 4:
            message.critical(self, system)
        elif fail == 5:
            message.hit(self, target, system, damage)
            message.kill(target)

    def probability(self, attacker, system):
        """
        Calculates probability minus countermeasures.
        :param attacker:
        :param system:
        :return:
        """
        if attacker.reliability + random.randint(0, 50) > 50:  # Malfunction by reliability.
            probability = random.randint(0, 100)
            for def_sys in self.systems.copy():
                if eq_systems[self.type][def_sys][1] < 0 and system < 90:
                    if not (attacker.type == 1 and def_sys == 2) or not (
                            attacker.type == 2 and def_sys in (3, 4)) or not \
                            (attacker.type == 3 and def_sys in (2, 3)):  # Systems without ammunition to decrease.
                        self.systems[def_sys] -= 1
                        if self.systems[def_sys] == 0:  # Removing system if empty.
                            self.systems.pop(def_sys)
                    probability -= random.randint(10 * -eq_systems[self.type][self.external][1] // 2,
                                                  10 * -eq_systems[self.type][self.external][1])
            if probability < 30:
                return 2  # Miss return
            else:
                return probability
        else:
            return 1  # Malfunction return

    def defense(self, unit, system, probability):
        """
        Function of hitting probability and decreasing unit status after hit.
        :param probability:
        :param unit: Attacking vehicle.
        :param system: Attacking weapon system.
        """
        critical = 3
        if probability > 90:
            critical = 4
        damage = (eq_systems[unit.type][system][1] * (critical - 2)) - random.randint(-2, 1)
        self.state -= damage

        if self.state < 1:  # Asset destroyed.
            self.state = 0
            self.statename = self.set_state()
            return 5, damage
        else:
            self.statename = self.set_state()
        return critical, damage


class WelcomeScreen(Screen):
    years = [1975, 2020]
    welcome_message = welcome()
    years.append(f"Specify default battle year {years[0]} - {years[1]}:")

    def blinker(self, check, blink, minimum=0, maximum=1):
        if oob_input(check, minimum, maximum):
            blink.text = "Valid input"
        else:
            blink.text = "Invalid input"

    def check(self, check1, check2, check3, result):
        if oob_input(check1, self.years[0], self.years[1]) and oob_input(check2, maximum=99) and \
                oob_input(check3, maximum=99):
            App.get_running_app().root.current = "oob"
        else:
            result.text = "Wrong inputs!\nPlease retry!"


class OOB(Screen):
    asset = 1

    def on_kv_post(self, base_widget):
        # self.import_variables()
        pass

    def import_variables(self):
        # self.yearsX = self.manager.get_screen("WelcomeScreen").years
        # print(self.yearsX)
        pass

    def next(self, button, years_changer):
        if self.counter_a == self.sides[0] or self.counter_b == self.sides[1]:
            if oob_input(years_changer.text, self.years[0], self.years[1]):
                return True
                # restart the screen
            elif years_changer.text == "":
                return True
                # restart the screen
            else:
                return False


class BSApp(App):
    def align_text(self, label):  # makes the text half size of the box
        label.font_size = 0.5 * label.height

    def build(self):
        self.root = Builder.load_file("bs.kv")


vehicles = {
    1: {1: ("MBT", (90, 1, 2, 3, 4, 5, 6, 7), 8), 2: ("AFV", (91, 1, 2, 3, 4, 5, 6, 7), 8),
        3: ("IFV", (92, 1, 2, 3, 4, 5, 6), 6), 4: ("APC", (93, 1, 2, 3, 6), 4),
        5: ("SAM", (94, 1, 2, 3, 6, 8, 9, 10), 4), 6: ("MLB", (95, 1, 2, 3, 6, 11, 12), 4)},
    2: {1: ("Small Multirole Aircraft", (90, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), 4),
        2: ("Medium Multirole Aircraft", (91, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), 6),
        3: ("Large Multirole Aircraft", (92, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), 8),
        4: ("Large Heavy Aircraft", (93, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), 10),
        5: ("Very Large Heavy Aircraft", (94, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), 10)},
    3: {1: ("Corvette", (90, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 4),
        2: ("Frigate", (91, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 6),
        3: ("Destroyer", (92, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 8),
        4: ("Cruiser", (93, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 10),
        5: ("Battlecruiser", (94, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 16),
        6: ("Battleship", (95, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 20),
        7: ("Light Carrier", (96, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 16),
        8: ("Aircraft Carrier", (97, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 20)}
}
vehicles_internal = {1: "MBT", 2: "AFV", 3: "IFV", 4: "APC", 5: "SAM", 6: "MLB", 7: "Small Multirole Aircraft",
                     8: "Medium Multirole Aircraft", 9: "Large Multirole Aircraft", 10: "Large Heavy Aircraft",
                     11: "Very Large Heavy Aircraft", 12: "Corvette", 13: "Frigate", 14: "Destroyer", 15: "Cruiser",
                     16: "Battlecruiser", 17: "Battleship", 18: "Light Carrier", 19: "Aircraft Carrier"}
eq_systems = {
    1: {1: ("Smoke", -2, 0, 0, 0), 2: ("SK-APS", -3, 0, 0, 0), 3: ("HK-APS", -4, 0, 0, 0), 4: ("ERA", -6, 0, 0, 0),
        5: ("NxRA", -8, 0, 0, 0), 6: ("Applique", -3, 0, 0, 0), 7: ("ATGM", 4, (1, 3), 3, 0),
        8: ("SR-SAM", 3, 2, 2, 0), 9: ("MR-SAM", 3, 2, 4, 0), 10: ("LR-SAM", 3, 2, 12, 3), 11: ("MR-AShM", 5, 3, 4, 0),
        12: ("LR-AShM", 5, 3, 6, 0), 90: ("tank gun", 5, 1, 2, 0), 91: ("autocannon", 2, (1, 2), 2, 0),
        92: ("heavy MG", 1, (1, 2), 2, 0), 93: ("light MG", 1, 1, 1, 0), 94: ("crew handheld firearms", 1, 1, 1, 0),
        95: ("crew handheld firearms", 1, 1, 1, 0)},
    2: {1: ("Flares", -2, 0, 0, 0), 2: ("Chaff", -2, 0, 0, 0), 3: ("ECM", -2, 0, 0, 0),
        4: ("EWS", -3, 0, 0, 0), 5: ("SRAAM", 4, 2, 2, 0), 6: ("MRAAM", 4, 2, 4, 0), 7: ("LRAAM", 4, 2, 12, 3),
        8: ("AGM", 4, 1, 3, 0), 9: ("MR-AShM", 5, 3, 4, 0), 10: ("SEAD", 5, 6, 4, 0),
        11: ("Cruise Missile", 3, 1, 5, 0), 12: ("Bomb", 2, 1, 1, 0), 13: ("GBU", 4, 1, 1, 0),
        90: ("coaxial cannon", 1, (1, 2), 1, 0), 91: ("coaxial cannon", 2, (1, 2), 1, 0),
        92: ("coaxial cannon", 2, (1, 2), 1, 0), 93: ("defense turrets", 1, 2, 1, 0),
        94: ("defense turrets", 1, 2, 1, 0)},
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
         "Worried", "New", "Withdrawing", "unknown"]

"""sm = ScreenManager()
sm.add_widget(WelcomeScreen(name="WelcomeScreen"))
sm.current = "WelcomeScreen"
"""

default = Asset("default", [1, 1, 1999], 1)
default.systems[1] = 2
retreated = []

message = Message()

notfound = 0

if __name__ == '__main__':
    BSApp().run()

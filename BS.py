"""
Battle system for NoU.
by Toonu
"""

import random
import time

# TODO
"""
Add countermeasure system overwhelm by adding them 0 effect if they was attacked 
already in that turn, then reset the value.

Add ability to attack each type of target once per turn

Rewrite adding units by their type in batches
"""


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
                f"{unit} | {unit.define_system(system_num)} failed to connect and could not have been fired.",
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
        self.reliability = self.year - 1945  # Reliability of its WS
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
        Returns ammunition for specified system
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

    def set_state(self, finals=False):
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
        if not finals and self.state < vehicles[self.type][self.external][2] // 2:
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
                cont = False
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
                    if cont and eq_systems[self.type][system][1] >= maximum:  # getting max damage weapon
                        maximum = eq_systems[self.type][system][1]
                        best_system = system
                if cont:
                    try:
                        if 8 not in eq_systems[self.type][best_system][2]:
                            self.systems[best_system] -= 1
                    except TypeError:
                        if 8 != eq_systems[self.type][best_system][2]:
                            self.systems[best_system] -= 1
                    if self.systems[best_system] <= 0:
                        self.systems.pop(best_system)
                    probability = target.probability(self, best_system)
                    if probability < 30:
                        self.failure(best_system, probability, target)
                    else:
                        attack_result = target.defense(self, best_system, probability)
                        self.failure(best_system, attack_result[0], target, attack_result[1])
                    break
                break
            else:
                continue

        if self.distance == 0 and not cont and len(self.systems) < 2:  # Withdrawal when nothing can be fired upon.
            self.statename = "Withdrawing"

        self.turn += 1
        if self.statename == "Withdrawing":  # Withdrawal
            print(f"{self.name} {self.typename} withdrawing!")
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
        if fail == 1:  # Malfunction message
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
        if attacker.reliability + random.randint(-10, 50) > 50:  # Malfunction by reliability.
            probability = random.randint(20, 80)
            for def_sys in self.systems.copy():
                if probability >= 0 and system < 90:
                    defend = False
                    try:
                        if eq_systems[self.type][def_sys][2][-1] in (8, 9) and system < 90:
                            defend = True
                    except TypeError:
                        if (9 == eq_systems[self.type][def_sys][2] or 8 == eq_systems[self.type][def_sys][2]) \
                                and system < 90:
                            defend = True
                    finally:
                        if defend:
                            try:
                                if 8 not in eq_systems[self.type][def_sys][2]:
                                    # Systems without ammunition to decrease.
                                    self.systems[def_sys] -= 1
                            except TypeError:
                                if 8 != eq_systems[self.type][def_sys][2]:  # Systems without ammunition to decrease.
                                    self.systems[def_sys] -= 1

                            if self.systems[def_sys] == 0:  # Removing system if empty.
                                self.systems.pop(def_sys)
                            probability -= random.randint(
                                eq_systems[self.type][def_sys][1] * self.systems[def_sys] * 4,
                                eq_systems[self.type][def_sys][1] * self.systems[def_sys] * 10
                            )
                            print(f"{self.name} {self.typename} fired "
                                  f"{eq_systems[self.type][def_sys][0]} in self-defence")

                        elif eq_systems[2][14] == def_sys:
                            probability += 20

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


def battle_core(side_a, side_b):
    """
    Core of the battle algorithm.
    :param side_a: Objects of side a.
    :param side_b: Objects of side b.
    """
    turn = 0
    print(f"Turn: {turn}\n{oob_listing(side_a + side_b, name=True, status=True, distance=True)}\n")
    while len(side_b) > 0 and len(side_a) > 0:
        turn += 1
        clear()

        for unit in (side_a + side_b).copy():
            if unit.turn == turn:
                result = unit.attack(side_a, side_b)
                if result[0] == 5:
                    if result[1].side == 1:
                        for i in range(len(side_a)):
                            if side_a[i] == result[1]:
                                side_a.pop(i)
                                break
                    else:
                        for i in range(len(side_b)):
                            if side_b[i] == result[1]:
                                side_b.pop(i)
                                break
        print(f"Turn: {turn}\n{oob_listing(side_a + side_b, name=True, status=True, distance=True)}\n")
        input(f"Enter turn {turn + 1}:")
    finalize(side_a, side_b)


def finalize(side_a, side_b):
    """
    Ending
    :param side_a:
    :param side_b:
    """
    clear()
    message.report("Finalizing report")
    print("\nThe remaining units:")
    oob_listing(side_a + side_b)
    for i in retreated:
        print(f"{i.name} {i.typename} retreated successfully with {i.state} ({i.set_state(True)}) remaining health.")
    print("\nThe battle has ended with this results. Stay strong! Long live the Emperor!")
    message.ending()
    input("The program will end after pressing enter. Screenshot the results!!!")


# Eq System Category: {System: {Name str, dmg int, target int/tuple, max range int, min range int}}
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
    1: {1: ("Smoke", 2, 9, 0, 0), 2: ("SK-APS", 3, 8, 0, 0), 3: ("HK-APS", 4, 9, 0, 0), 4: ("ERA", 6, 9, 0, 0),
        5: ("NxRA", 8, 9, 0, 0), 6: ("Applique", 3, 9, 0, 0), 7: ("ATGM", 4, (1, 3), 3, 0),
        8: ("SR-SAM", 3, 2, 3, 0), 9: ("MR-SAM", 3, 2, 6, 0), 10: ("LR-SAM", 3, 2, 10, 3), 11: ("MR-AShM", 6, 3, 4, 0),
        12: ("LR-AShM", 5, 3, 6, 0), 13: ("Heavy MG Turret", 1, 2, 1, 0), 14: ("Autocannon Turret", 2, 2, 1, 0),
        90: ("Tank gun", 5, 1, 2, 0), 91: ("Autocannon", 2, (1, 2), 2, 0),
        92: ("Heavy MG", 1, (1, 2), 2, 0), 93: ("Light MG", 1, 1, 1, 0), 94: ("Crew Handheld Firearms", 1, 1, 1, 0),
        95: ("Crew Handheld Firearms", 1, 1, 1, 0)},
    2: {1: ("Flares", 2, 9, 0, 0), 2: ("Chaff", 2, 9, 0, 0), 3: ("ECM", 2, 8, 0, 0),
        4: ("EWS", 3, 8, 0, 0), 5: ("SRAAM", 4, 2, 2, 0), 6: ("MRAAM", 4, 2, 4, 0), 7: ("LRAAM", 4, 2, 12, 3),
        8: ("AGM", 4, 1, 3, 0), 9: ("MR-AShM", 6, 3, 4, 0), 10: ("SEAD", 5, 6, 4, 0),
        11: ("Cruise Missile", 3, 1, 5, 0), 12: ("Bomb", 2, 1, 1, 0), 13: ("GBU", 4, 1, 1, 0),
        14: ("Drop Tank", 0, 0, 0, 0),
        90: ("Autocannon", 1, (1, 2), 1, 0), 91: ("Autocannon", 2, (1, 2), 1, 0),
        92: ("Autocannon", 2, (1, 2), 1, 0), 93: ("Defense Turrets", 1, 2, 1, 0),
        94: ("Defense Turrets", 1, 2, 1, 0)},
    3: {1: ("CIWS", 1, (2, 8), 1, 0), 2: ("DEW", 2, (2, 8), 1, 0), 3: ("ECM", 1, 8, 0, 0),
        4: ("Smoke", 2, 9, 0, 0), 5: ("Chaff", 2, 9, 0, 0), 6: ("SR-SAM", 3, (2, 9), 3, 0),
        7: ("MR-SAM", 3, (2, 9), 6, 0), 8: ("LR-SAM", 3, 2, 10, 3), 9: ("MR-AShM", 6, 3, 4, 0),
        10: ("LR-AShM", 8, 3, 6, 0), 11: ("Cruise Missile", 3, 1, 5, 0), 90: ("Main Battery", 1, (1, 2, 3), 1, 0),
        91: ("Main Battery", 1, (1, 2, 3), 1, 0), 92: ("Main Battery", 1, (1, 2, 3), 1, 0),
        93: ("Main Battery", 1, (1, 2, 3), 2, 0), 94: ("Main Battery", 1, (1, 2, 3), 3, 0),
        95: ("Main Battery", 1, (1, 2, 3), 4, 0), 96: ("Auxiliary Weapons", 1, (2, 3), 1, 0),
        97: ("Auxiliary Weapons", 1, (2, 3), 1, 0)}
}
state = ["KIA", "Heavily Damaged", "Major Damage taken", "Damaged", "Slightly damaged", "Scratched",
         "In nominal condition", "Worried", "New", "Withdrawing", "unknown"]


def welcome():
    """
    Introducing welcome!
    """
    version = "0.9.9"
    headline = f"Welcome to Battle System Manager v{version} (ALPHA)"
    print("=" * len(headline), "\n", headline, "\n", " " * ((len(headline) - 13) // 2), "Made by Toonu\n",
          " " * ((len(headline) - 21) // 2), "The Emperor of Iconia\n", " " * (len(headline) // 2), "☩\n",
          " " * ((len(headline) - 5) // 2), "☩☩☩☩☩\n", " " * (len(headline) // 2), "☩\n",
          " " * ((len(headline) - 37) // 2), "With the help of Red, Litz and Sleepy\n", " " * (len(headline) // 2),
          "☩\n", "≋" * len(headline), "\n", sep="")


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


def oob_asset_configuration_new(number, side, year, years, maximum):
    """
    Specify each asset category, year and its type
    :param number: Specify asset object number.
    :param side: Specify asset side number.
    :param year: Default asset year accepted if not changed.
    :param years: Lower and upper year limit of assets.
    :return: Returns unit category (veh, air, sea), type (subtype of category) and year of production.
    """
    clear()  # Chooses unit category.
    category = user_input(1, 3, f"Asset configuration mode:\n\nSide: A\nWhat category of vehicles you want to add?"
                                f"\n1 | Ground\n2 | Air\n3 | Naval\nInput: ")
    clear()  # Chooses unit type.
    print(f"Asset configuration mode:\n\nChoose type subcategory: ")
    for i in range(1, len(vehicles[category]) + 1):  # Prints out all unit types of unit category.
        print(i, "=", vehicles[category][i][0], end=" | ")
    unit_type = user_input(maximum=len(vehicles[category]), msg="\nInput: ")

    clear()  # Chooses unit year.
    print(f"Asset configuration mode:\n\nChoose amount of vehicles: ")
    amount = user_input(1, maximum)
    while True:
        print(f"Asset configuration mode:\n\nVehicle origin year. ({years[0]} - {years[1]})"
              f"\nPress enter if: {year}\nInput: ")
        new_year = user_input(years[0], years[1], enter=True)  # Assigns new non-default year for the unit.
        if new_year is not None and new_year != "":
            year = new_year
        return category, unit_type, year, amount


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
                        for key, item in source_systems.items():
                            unit.systems[key] = item

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
        printed = f"Side {unit.side} |"
        ending = f" {unit.typename}"
        if year:
            printed += f" {unit.year} |"
        if name:
            printed += f" {unit.name} |"
        if status:
            printed += f" {unit.state} |"
        if distance:
            printed += f" {unit.distance} |"
        if equip:
            ending += f" equipped with: "

        print(printed + ending, end="")
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
            wrong_system = user_input(1, 3, "What is wrong?\n1 | Unit composition"
                                            "\n2 | Unit Equipment\n3 | Unit years\nYour input: ")
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
                    batch = oob_asset_configuration(unit.type, unit.side, unit.year, years)
                    unit.year = batch[2]
                    unit.reliability = unit.year - 1945
                    unit.internal = unit.asset_assign(batch)
                    unit.typename = vehicles[batch[0]][batch[1]][0]
                    unit.external = batch[1]
                    unit.type = batch[0]
                    unit.systems = unit.systems_ammo()


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


def start(bugs=True):
    """
    Starting function for the whole program.
    :param bugs: Enables bug logging for user. Shows error when the program crashes.
    """
    import traceback
    if bugs:
        try:
            oob_main()
        except Exception as e:
            print(f"Program crashed with this error: {e}, {type(e)}, {e.args}, \nPlease report the error to the "
                  f"developers.\n\n")
            print(traceback.format_exc())
            input("Program will restart after pressing enter:")
    else:
        oob_main()


default = Asset("default", [1, 1, 1999], 1)
default.systems[1] = 2
retreated = []

message = Message()

notfound = 0
start()

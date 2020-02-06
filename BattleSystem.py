"""
Welcome
"""

import random
from sys import exit

# noinspection PyPep8Naming
import PySimpleGUI as sg


class Asset:
    """
    Asset objects are the units itself.
    """

    def __init__(self, name, side, unit_type, year):
        has_radar = lambda x: True if x == 4 else False
        set_distance = lambda x: 6 if x == 1 else -6
        set_side_unit = lambda x: (1, 1, 2) if x == 1 else (2, -1, 1)
        self.default_eq = lambda x: {vehicles[x.type[0]][x.type[1]][1][0]: vehicles[x.type[0]][x.type[1]][3]}
        self.name = name
        self.type = category(unit_type)  # 0 Class 1 Subclass 2 Internal, 3 str name
        self.type.insert(2, unit_type)
        self.state = [vehicles[self.type[0]][self.type[1]][2]]  # 0 State 1 str state
        self.state.append(self.set_state())
        self.side = set_side_unit(side)  # Fighting side
        self.year = year  # Year of origin
        self.distance = set_distance(side)
        self.systems = self.default_eq(self)
        self.has_radar = has_radar(unit_type)

        self.is_withdrawing = False
        self.oversaturated = []
        self.turn = 0

    def __str__(self):
        return str(f"{self.name}_{self.type[3]}: {self.state[0]}-{str(self.state[1])} | Dist: {self.distance}")

    def set_state(self):
        """
        Sets unit state name
        :return:
        """
        result = 9
        if vehicles[self.type[0]][self.type[1]][2] == 4 and self.state[0] != 9:
            result = state[self.state[0] * 2]
        elif vehicles[self.type[0]][self.type[1]][2] == 6 and self.state[0] != 9:
            result = state[round(self.state[0] * 1.25)]
        elif vehicles[self.type[0]][self.type[1]][2] == 8 and self.state[0] != 9:
            result = state[self.state[0]]
        elif vehicles[self.type[0]][self.type[1]][2] == 10 and self.state[0] != 9:
            result = state[round(self.state[0] / 1.25)]
        elif vehicles[self.type[0]][self.type[1]][2] == 16 and self.state[0] != 9:
            result = state[self.state[0] // 2]
        elif self.state[0] != 9:
            result = state[round(self.state[0] / 2.5)]
        return result

    def define_system(self, system, reverse=False):
        """
        Inverts system from int to its str name.
        @param system: System to invert.
        @param reverse: Inverts str to its int name.
        @return: Returns inverted int/str.
        """
        if not reverse:
            try:
                return eq_systems[self.type[0]][system][0]
            except KeyError:
                return "weapon system"
        else:
            try:
                for item in eq_systems[self.type[0]]:
                    if eq_systems[self.type[0]][item][0] == system:
                        return item
            except KeyError:
                return 0

    def add_system(self, system, amount, default=False):
        """
        Adds equipment to the systems dict of object.
        @param system: System to be added.
        @param amount: How much of them should be added.
        @param default: Allows also systems above 90 if true.
        """
        try:
            if default and int(amount) > 0 and system in vehicles[self.type[0]][self.type[1]][1]:
                self.systems[system] = int(amount)
            elif system < 90 and int(amount) > 0 and system in vehicles[self.type[0]][self.type[1]][1]:
                self.systems[system] = int(amount)
            elif default and system in self.systems:
                self.systems.pop(system)
            elif system in self.systems:
                self.systems[system] = int(amount)
        except ValueError:
            sg.popup_auto_close("Wrong input", auto_close_duration=1)

    def search(self, sides, stats):
        """
        Find enemy object of each unit category including SEAD mechanics. Makes list of enemies and returns it.
        @param sides: Two sides of unit objects.
        @param stats: General Database of lists and main informations used through the program.
        @return: List of dictionaries of enemy to be attacked.
        """
        targets = {"denied": [], "attacked": {}, "weapons": {}}
        dist_calc = lambda x, y: abs(x - y)

        while not len(sides[self.side[2]]) == len(targets["attacked"]) + len(targets["denied"]):
            if len(sides[self.side[2]]) > 0:
                target = sides[self.side[2]][random.randint(0, len(sides[self.side[2]]) - 1)]
            # noinspection PyUnboundLocalVariable
            if target not in targets["denied"] and target.type[0] not in targets["attacked"]:
                attackable = False

                for weapon in self.systems:
                    if ((target.type[0] in eq_systems[self.type[0]][weapon][2])
                        or (eq_systems[self.type[0]][weapon][2] == 6 and target.has_radar)) \
                            and dist_calc(self.distance, target.distance) <= eq_systems[self.type[0]][weapon][3]:
                        # Successful weapon <=> target <=> distance lock | OR | SEAD mechanics.
                        targets["attacked"][target.type[0]] = target
                        targets["weapons"][target.type[0]] = weapon
                        attackable = True
                if not attackable:
                    targets["denied"].append(target)
            else:
                targets["denied"].append(target)
        for target in targets["attacked"]:
            for weapon in targets["weapons"]:
                if targets["attacked"][target].type[0] in eq_systems[self.type[0]][targets["weapons"][weapon]][2]:
                    print(f"{self} > {targets['attacked'][target]} | {self.define_system(targets['weapons'][weapon])}")
        return targets

    def status(self, sides, stats):
        """
        Modify unit object distance, turn number, withdraw and pursue moves and adds it to the database when withdrawn
        or destroyed including its weapons.
        @param sides: Two sides of unit objects.
        @param stats: General Database of lists and main informations used through the program.
        @return: Returns modified stats updated with new informations.
        """
        pursue = True
        self.turn += 1

        if self.state[0] <= 0:
            stats[6][0].append(self)
            for system in self.systems:
                try:
                    stats[6][2][self.side[0]][self.define_system(system)] += self.systems[system]
                except KeyError:
                    stats[6][2][self.side[0]][self.define_system(system)] = self.systems[system]
            sides[self.side[0]].remove(self)
            return
        elif not self.is_withdrawing and self.state[0] < vehicles[self.type[0]][self.type[1]][2] \
                and random.randint(0, 100) > 50:
            self.is_withdrawing = True
        elif self.is_withdrawing and (self.distance < -9 or self.distance > 9):
            stats[6][1].append(self)
            sides[self.side[0]].remove(self)
            return
        elif self.is_withdrawing:
            self.distance += 2 * self.side[1]

        for enemy in sides[self.side[2]]:
            if not enemy.is_withdrawing:
                pursue = False
                break

        if pursue and -10 < self.distance < 10:  # Pursue
            self.distance -= 2 * self.side[1]
        elif self.distance != 0 and -10 < self.distance < 10:  # Normal
            self.distance -= 1 * self.side[1]


def battle_turn(sides, stats, dmg=False):
    """
    @param dmg:
    @param stats:
        0 - Default Year
        1,2 - Unused
        3 - Program version
        4 - List:
            0 Minimal
            1 maximal year
        5 - Turn number
        6 - Database:
            0 - Destroyed Units
            1 - Withdrawn Units
            2 - List - 1 - SideA consumed systems, 2 - SideB consumed systems

    @param sides:
        1 - Side A Unit Objects
        2 - Side B Unit Objects
    """

    sg.theme('DarkBlue13')
    layout = []
    menu_def = [['&Edit', ['Units', '---', 'Exit']], ['&Properties', []]]
    layout.append([sg.Menu(menu_def)])

    col = unit_listing((sides[1] + sides[2]).copy(), [])

    layout.append([sg.T(f"Battle Simulator - Turn: {stats[5]}")])
    layout.append([sg.Col(col)])
    layout.append([sg.B("Next Turn", size=(20, 5), button_color=("#000000", "#dbc867"))])
    window = sg.Window(f'Battle System {stats[3]}', layout, resizable=True,
                       size=(600, 600), return_keyboard_events=True)

    while True:
        event, values = window.read()
        if event in (None, "Exit"):  # User closes window or presses Exit button.
            exit()
        elif event in ("Next Turn", "\r"):  # User presses Next button to get to the next turn.
            print()
            for unit in sides[1] + sides[2]:
                targets = unit.search(sides, stats)
                # unit.attack(sides, stats, targets)
                unit.status(sides, stats)
            stats[5] += 1  # Adding turn +1
            break
        elif event == "Units":  # Show unit tab view only.
            oob_units(sides, stats, view_only=True)
        elif event == "h:72":
            dmg = True
            break
        elif "Damage-" in event and dmg:
            name = "asset" + event.replace("Damage-", "")  # Getting assetx_y name from button key (event).
            for unit in sides[1] + sides[2]:
                if unit.name == name:
                    unit.state[0] -= 4
                    unit.state[1] = unit.set_state()
                    dmg = True
                    break
            break
    window.close()
    return stats, dmg


def final(sides, stats):
    """
    Prints out results of the battle from stats and sides lists.
    @param sides: Two sides of unit objects.
    @param stats: General Database of lists and main informations used through the program.
    """
    print("\nWinning Side\n")
    for unit in sides[1] + sides[2]:
        print(unit)
    print("\nDestroyed: \n")
    for destroyed in stats[6][0]:
        print(destroyed)
    print("\nSurvived: \n")
    for survived in stats[6][1]:
        print(survived)
    print("\nLost or Fired Weapons Side A")
    try:
        for system, value in stats[6][2][1].items():
            if len(str(value)) <= 1:  # Align the values with spaces for better look.
                value = str(value) + "   "
            elif len(str(value)) <= 2:
                value = str(value) + "  "
            elif len(str(value)) <= 3:
                value = str(value) + " "
            print(f"{value} | {system} ")
    except IndexError:
        pass
    print("\nLost or Fired Weapons Side B")
    try:
        for system, value in stats[6][2][2].items():
            print(f"{system} {value}")
    except IndexError:
        pass


def oob():
    """
    Main body for input
    """
    side1 = []
    side2 = []
    print("Do not dare to close this or I will haunt you in the sleep!")

    stats = oob_stats()  # Stats 0 default year, 1 sideA, 2 sideB, 3 version, 4 min_max years, 5 turn
    sides = oob_asset_creator(stats, side1, side2)

    for i in range(1, 4):
        cont = False
        for unit in sides[1] + sides[2]:
            if unit.type[0] == i:
                cont = True
                break
        if cont:
            # noinspection PyUnboundLocalVariable
            oob_eq(sides, stats, i, unit)

    oob_units(sides, stats)

    stats.append(0)
    stats.append([[], [], {1: {}, 2: {}}])

    values = False  # Handles special damage mode of battle_turn
    while len(sides[1]) > 0 < len(sides[2]):
        stats, values = battle_turn(sides, stats, values)

    final(sides, stats)


# noinspection SpellCheckingInspection
def oob_stats(bypass=True, def_years=None):
    """
    Sets up default year, amount of units per side and can change default years via properities.
    """
    if def_years is None:
        def_years = [1945, 2020]
    version = "1.0.0"
    result = True

    sg.theme('DarkBlue13')
    layout = [[sg.Image("img/IS128.png", size=(128, 128), background_color="#00247d")],
              [sg.Image("img/Air128.png", background_color="#00247d"),
               sg.Text(f"Welcome to Battle System Manager v {version} (BETA)\n"
                       f"Made by Toonu\nThe Emperor of Iconia\nWith the help of Red, "
                       f"Litz and Sleepy", justification="center", background_color="#00247d"),
               sg.Image("img/Navy128.png", background_color="#00247d")],
              [sg.Text("Year:    ", background_color="#00247d"),
               sg.InputText(justification="center", default_text="19", enable_events=True, key="year"),
               sg.Text(f"{def_years[0]} - {def_years[1]}", background_color="#00247d")],
              [sg.Text("Side A: ", background_color="#00247d"),
               sg.InputText(justification="center", enable_events=True, key="a"),
               sg.Text("1< #         .", background_color="#00247d")],
              [sg.Text("Side B: ", background_color="#00247d"),
               sg.InputText(justification="center", enable_events=True, key="b"),
               sg.Text("1< #         .", background_color="#00247d")],
              [sg.Button("Finish", size=(20, 2), button_color=("#000000", "#dbc867"))]]
    menu_def = [['&Edit', ['Exit']], ['&Properties', ["&Switch default years"]]]
    layout.append([sg.Menu(menu_def)])
    window = sg.Window(f'Battle System {version}', layout, return_keyboard_events=True, element_justification="center",
                       background_color="#00247d")

    while True:
        event, values = window.read()
        if event is None or event == "Exit":  # if user closes window or clicks Exit in menu.
            break
        elif event == "Finish" or event == "\r":  # Button checks validity of inputs and then returns result.
            if (user_input(values["year"], def_years[0], def_years[1]) and user_input(values["a"], maximum=81)
                    and user_input(values["b"], maximum=81)):
                result = [values["year"], values["a"], values["b"], version, def_years]
                break
            elif bypass:  # Bypasses the check for testing.
                values["a"] = 4
                values["b"] = 4
                values["year"] = 1999
                result = [values["year"], values["a"], values["b"], version, def_years]
                break
        elif event == "Switch default years":
            # Launches properity change of default years, then re-launch program with new years assigned.
            def_years = oob_ch_year(def_years, version)
            window.close()
            result = oob_stats(def_years=def_years)

    window.close()
    # noinspection PyUnboundLocalVariable
    return result


def oob_ch_year(def_years, version):
    """
    Sets up a new default year for the whole program.
    @param def_years: Original default years.
    @param version: Program version for headline of the program.
    @return: Returns new default years.
    """
    sg.theme('DarkBlue13')
    layout = [[sg.T("Choose new default year:")],
              [sg.Input(f"{def_years[0]}", size=(6, 1), key="minimal"),
               sg.Input(f"{def_years[1]}", size=(6, 1), key="maximal")], [sg.B("Edit")]]
    window = sg.Window(f'Battle System {version}', layout, return_keyboard_events=True)

    while True:
        event, values = window.read()
        if event is None:  # When user closes window.
            break
        elif event == "Edit" or event == "\r":  # Button checks validity of input and then assign new default years.
            if user_input(values["minimal"], 1900, int(values["maximal"])) and \
                    user_input(values["maximal"], int(values["minimal"]), 2200):
                def_years[0] = int(values["minimal"])
                def_years[1] = int(values["maximal"])
                break
    window.close()
    return def_years


def oob_asset_creator(stats, side1, side2, i=1):  # Stats 0 def_year, 1 side_a, 2 side_b
    """
    Creating new objects after the user inputs.
    @param stats: Imported default stats.
    @param side1: Side 1 list
    @param side2: Side 2 list
    @param i: Side added
    @return: Returns new object assets in a list.
    """
    sg.theme('DarkBlue13')
    tab1_layout = [[sg.Radio("MBT", "1")],
                   [sg.Radio("AFV", "1")],
                   [sg.Radio("IFV", "1")],
                   [sg.Radio("APC", "1")],
                   [sg.Radio("SAM", "1")],
                   [sg.Radio("MLB", "1")]]
    tab2_layout = [[sg.Radio("Small Multirole", "1")],
                   [sg.Radio("Medium Multirole", "1")],
                   [sg.Radio("Large Multirole", "1")],
                   [sg.Radio("Large Airframe", "1")],
                   [sg.Radio("Very Large Airframe", "1")]]
    tab3_layout = [[sg.Radio("Corvette", "1")],
                   [sg.Radio("Frigate", "1")],
                   [sg.Radio("Destroyer", "1")],
                   [sg.Radio("Cruiser", "1")],
                   [sg.Radio("Battlecruiser", "1")],
                   [sg.Radio("Battleship", "1")],
                   [sg.Radio("Light Carrier", "1")],
                   [sg.Radio("Carrier", "1")]]
    layout = [[sg.Text("Asset Creator")],
              [sg.TabGroup([[sg.Tab('Ground Unit', tab1_layout),
                             sg.Tab('Aerial Unit', tab2_layout),
                             sg.Tab('Naval Unit', tab3_layout)]]),
               sg.T(f"Assets remaining: {stats[i]}\nSide: {i}", key="rem")],
              [sg.T("Amount:             ", ), sg.In(justification="center", focus=True)],
              [sg.T("Year if different:  "), sg.In(f"{stats[0]}", justification="center")],
              [sg.Button('Next', size=(20, 2), button_color=("#000000", "#dbc867"))]]
    window = sg.Window(f'Battle System {stats[3]}', layout, return_keyboard_events=True, use_default_focus=False)

    while True:
        length = 0
        event, values = window.read()
        if event is None:  # User closes window.
            exit()
        elif event == "Next" or event == "\r":  # User clicks next or press enter.
            if user_input(values[20], 1945, 2020, enter=True) and \
                    user_input(values[19], minimum=1, maximum=int(stats[i])):  # Checks inputs and proceeds.
                for j in range(len(values) - 2):  # j are buttons of unit type - ending text values.
                    if values[j]:  # Button which is True - future unit type
                        if values[20] != "" and int(values[20]) != stats[0]:
                            # Assigns new year if not blank or same as default year.
                            stats[0] = int(values[20])
                        length = len(locals()['side' + str(i)])  # Calculate next asset by gaining past maximal asset.
                        for k in range(int(values[19])):  # k = how many units of that type are created.
                            locals()["side" + str(i)].append(f"asset{i}_{length + k}")  # creating the objects itself.
                            locals()["side" + str(i)][length + k] = Asset(f"asset{i}_{length + k}", i, j, stats[0])
                        stats[i] = int(stats[i]) - int(values[19])  # deducting created assets for refreshed screen.
                        window.close()

                        if stats[1] == 0 == stats[2]:  # Ends refreshing screen if no assets can be made.
                            break
                        if stats[1] == 0 and i == 1:  # Refresh screen with new variables when 1st side is done.
                            i += 1
                        oob_asset_creator(stats, side1, side2, i)
                        break
                break
    window.close()
    return {1: side1, 2: side2}


def oob_eq(sides, stats, unit_type, template):
    """
    Equips unit with dictionary of weapon: amount.
    @param template: Default craft to mirror in the systems used.
    @param unit_type: Unit type.
    @param sides: All objects.
    @param stats: Program stats.
    """

    sg.theme('DarkBlue13')
    layout = [[sg.T(f"Equipment Editor - {return_type(unit_type)}", justification="center")],
              [sg.Text('_' * (len(sides[1]) + len(sides[2]) * 30))], []]
    leftcol = []
    column1 = [[]]
    column2 = [[]]
    leftcol.append([sg.T("Units:", size=(14, 1))])

    for i in range(1, 3):  # Making the grid.
        column = locals()["column" + f"{i}"]  # Assigning column to each side by i.
        for asset in sides[i]:  # Objects iteration per side.
            if asset.type[0] == unit_type:  # Only units of unit_type are allowed to be shown.
                column[-1].append(sg.T(f"{cut(asset)} ", justification="left", auto_size_text=True,
                                       key=f"{cut(asset)}"))  # Making unit names headline.
        for item in eq_systems[unit_type]:  # Grid of weapons bellow id:90
            if item < 90:
                if not i == 2:  # Prints left column of weapons for this type of units.
                    # noinspection PyUnboundLocalVariable
                    leftcol.append([sg.T(f"{template.define_system(item)}", size=(14, 1))])
                column.append([])  # Adds new row for each iteration bellow.
                for asset in sides[i]:  # Iterate in one side.
                    if asset.type[0] == unit_type and item in vehicles[asset.type[0]][asset.type[1]][1]:
                        # Prints only right unit type vs system type combinations. Disabled handled in else.
                        column[-1].append(sg.InputText(default_text="0", size=(4, 1),
                                                       key=f"{str(asset.name)}_{str(item)}"))
                    elif asset.type[0] == unit_type:  # Systems that unit cannot have are filled with 4 spaces.
                        column[-1].append(sg.T("   ", size=(4, 1)))

    maincol = [[]]
    maincol[-1].append(sg.Col(leftcol))
    maincol[-1].append(sg.Col(column1))
    maincol[-1].append(sg.VerticalSeparator())
    maincol[-1].append(sg.Col(column2))

    layout.append([sg.Col(maincol, scrollable=True, size=(80 * len(sides[1] + sides[2]), 460))])
    layout.append([sg.Button("Finish", size=(20, 2), button_color=("#000000", "#dbc867"))])

    menu_def = [['&Edit', ['Units', '---', 'Exit']], ['&Properties', []]]
    layout.append([sg.Menu(menu_def)])

    window = sg.Window(f'Battle System {stats[2]}', layout, resizable=True,
                       size=(100 + 80 * len(sides[1] + sides[2]), 600), return_keyboard_events=True)

    while True:
        event, values = window.read()
        if event in (None, "Exit"):  # User closes window or click Exit button.
            exit()
        elif event == "Finish" or event == "\r":  # Button checks validity and then returns result.
            check = True
            for asset in sides[1] + sides[2]:
                if asset.type[0] == unit_type:  # Only units of correct type go through.
                    for j in range(1, len(eq_systems[asset.type[0]]) - len(vehicles[asset.type[0]]) + 1):
                        try:  # j iterate in range of weapon systems for that unit type.
                            if not user_input(values[str(asset.name) + '_' + str(j)], maximum=400):
                                check = False  # If any wrong input is found, popup. Until fixed, won't let through.
                                break
                        except KeyError:  # Exception for non-existing j for systems unit subtype cannot obtain.
                            pass
            if check:  # When everything correct, add systems.
                for asset in sides[1] + sides[2]:
                    for j in range(1, len(eq_systems[asset.type[0]]) - len(vehicles[asset.type[0]]) + 1):
                        try:
                            if asset.type[0] == unit_type and user_input(values[str(asset.name) + '_' + str(j)],
                                                                         minimum=1, maximum=400, skip=True):
                                asset.add_system(j, values[str(asset.name) + '_' + str(j)])
                        except KeyError:  # Exception for non-existing j for systems unit subtype cannot obtain.
                            pass
                break
        elif event == "Units":  # Show unit view only.
            oob_units(sides, stats, view_only=True)
    window.close()


def oob_units(sides, stats, clone=None, default=False, view_only=False):
    """
    Main screen after inputs. Allows edit each unit individually and clone them.
    @param sides: Sides list.
    @param stats: Program stats.
    @param clone: Memory of cloned systems.
    @param default: Default admin editing mode.
    @param view_only: View only access switch.
    """
    sg.theme('DarkBlue13')
    column = []
    layout = [[sg.T(f"Unit Editor - Df: {default} | Copied: {clone}", justification="center")]]
    menu_def = [['&Edit', ['Exit']], ['&Properties', ["&Switch default editing"]]]

    if view_only:
        layout[-1].append(sg.T("VIEW ONLY - You can move this window anywhere!"))
    for unit in sides[1] + sides[2]:
        if view_only:  # Prints unit names and their radars.
            column.append([sg.T(f"{cut(unit)} - {unit.type[3]}", key=f"{unit.name}"), sg.T(f"R: {unit.has_radar}")])
        else:  # Prints unit buttons and their radars.
            column.append([sg.B(f"{cut(unit)} - {unit.type[3]}", key=f"{unit.name}"), sg.T(f"R: {unit.has_radar}")])
        column.append([sg.T(f"{unit.year}", size=(5, 1))])  # Prints unit years.
        systems = "Equipment: "  # Variable to store all systems per unit.
        for item in unit.systems:
            systems += f"{str(eq_systems[unit.type[0]][item][0])}: {unit.systems[item]}, "  # Adds to systems.
        column[-1].append(sg.T(f"{systems}", key=f"{cut(unit)}",  # Print systems of each unit and is r-clickable/copy.
                               right_click_menu=['&Right', [f"Copy-{cut(unit)}", f"Paste-{cut(unit)}"]]))

    layout.append([sg.Col(column, scrollable=True, size=(500, 500))])
    layout.append([sg.Button("Start Battle", key="battle", size=(20, 5), button_color=("#000000", "#dbc867"))])
    layout[-1].append(sg.Button("Refresh", size=(20, 5), button_color=("#000000", "#dbc867")))
    layout.append([sg.Menu(menu_def)])
    window = sg.Window(f'Battle System {stats[3]}', layout, resizable=True, size=(600, 600),
                       return_keyboard_events=True)

    while True:
        event, values = window.read()
        if event in (None, "Exit"):  # User closes with Close button or X.
            if not view_only:
                exit()
            break
        elif "Copy-" in event:  # Copying
            clone = {}
            name = "asset" + event.replace("Copy-", "")  # Getting assetx_y name from button key (event).
            for unit in sides[1] + sides[2]:
                if unit.name == name:
                    import copy
                    clone = copy.deepcopy(unit.systems)  # Clone source unit whole dictionary of systems.
            window.close()
            oob_units(sides, stats, clone, default)  # Reload window with copied memory.
            break
        elif "Paste-" in event and clone is not None:  # Pasting
            name = "asset" + event.replace("Paste-", "")  # Getting assetx_y name from button key (event).
            for unit in sides[1] + sides[2]:
                if unit.name == name:
                    for item in clone:
                        if item in vehicles[unit.type[0]][unit.type[1]][1]:
                            unit.add_system(item, clone[item], default)  # If default false, over 90 aren't allowed.
            window.close()
            oob_units(sides, stats, clone, default)  # Reload window copied items.
            break
        elif event == "Switch default editing" and not view_only:
            window.close()
            default = not default  # Switch default to opposite.
            oob_units(sides, stats, default=default)
            break
        elif event in ("\r", "battle"):  # Finalises this stage and goes into next window.
            break
        elif event == "Refresh":
            window.close()
            oob_units(sides, stats, view_only=view_only)
            break
        elif event is not None:  # Clicking any unit button opens the unit editor.
            for unit in sides[1] + sides[2]:
                if unit.name == event:
                    window.close()
                    oob_edit(sides, stats, unit, default=default)
                    break
            break

    window.close()


def oob_edit(sides, stats, unit, default=False):
    """
    Unit editor changing unit year, modifying its systems and changing the unit type while erasing its systems.
    @param sides: Sides list.
    @param stats: Program stats.
    @param unit: Modified unit.
    @param default: Default Mode switch
    """
    sg.theme('DarkBlue13')
    layout = []
    frame_layout = []
    year_layout = []
    type_layout = []
    column = []

    for item in unit.systems:
        if item < 90:  # Print all weapons of the unit.
            column.append([sg.T(f"{eq_systems[unit.type[0]][item][0]}", size=(16, 1), auto_size_text=True)])
            column[-1].append(sg.I(f"{unit.systems[item]}", size=(4, 1), key=eq_systems[unit.type[0]][item][0]))
        elif default:  # Default Mode enable showing editing even default systems. (over 90)
            column.append([sg.T(f"{eq_systems[unit.type[0]][item][0]}", size=(16, 1), auto_size_text=True)])
            column[-1].append(sg.I(f"{unit.systems[item]}", size=(4, 1), key=eq_systems[unit.type[0]][item][0]))

    adding = []
    types = []
    for _ in eq_systems[unit.type[0]]:  # Listing of weapons for weapons adding.
        if _ < 90 and _ in vehicles[unit.type[0]][unit.type[1]][1]:
            adding.append(eq_systems[unit.type[0]][_][0])
        elif default and _ in vehicles[unit.type[0]][unit.type[1]][1]:
            # Default Mode enable showing editing even default systems. (over 90)
            adding.append(eq_systems[unit.type[0]][_][0])
    for i in vehicles:
        for j in vehicles[i]:  # Builds all unit types for its switcher.
            types.append(vehicles[i][j][0])

    frame_layout.append([sg.Button("Add Weapon", key="add"),
                         sg.Combo(adding, size=(10, 1), key="wp", enable_events=True),
                         sg.T("#"), sg.InputText(key="amount", size=(5, 1))])  # Editor of weapons.
    type_layout.append([sg.T("Change Type:", size=(6, 1)), sg.Combo(types, size=(10, 1), key="type"),
                        sg.B("Change", tooltip="WARNING - Will erase the unit weapons!")])  # Editor of Type-Erases sys.
    year_layout.append([sg.T("Unit year: ", size=(8, 1)), sg.InputText(f"{unit.year}", key="uyear", size=(4, 1)),
                        sg.B("Edit", key="eyear")])
    frame_layout.append([sg.B("Modify", key="wmodify")])
    frame_layout.append([sg.Col(column)])
    layout.append([sg.B("Close"), sg.T(f"Unit: {unit}")])
    layout.append([sg.Frame("Year Editor", year_layout, font='Any 12', title_color='white')])
    layout[-1].append(sg.Frame("Type Editor", type_layout, font='Any 12', title_color='white'))
    layout.append([sg.Frame("Systems Editor", frame_layout, font='Any 12', title_color='white')])

    menu_def = [['&Edit', ['Units', '---', 'Exit']], ['&Properties', ["&Switch default editing"]]]
    layout.append([sg.Menu(menu_def)])
    window = sg.Window(f'Battle System {stats[3]}', layout, resizable=True,
                       size=(600, 600), return_keyboard_events=True)

    while True:
        event, values = window.read()
        if event in (None, "Exit"):  # User closes window or presses Exit button.
            exit()
        elif event == "Close":  # User presses Close button to get back to units.
            break
        elif event == "Switch default editing":  # Switches default mode.
            window.close()
            default = not default
            oob_edit(sides, stats, unit, default=default)
        elif event == "Change":  # Changes unit type completely.
            for vehicle in vehicles_internal:
                if values["type"] == vehicles_internal[vehicle]:
                    unit.type = category(vehicle)  # Class and subclass
                    unit.type.insert(2, vehicle)
                    unit.state = [vehicles[unit.type[0]][unit.type[1]][2]]  # How much alive asset is
                    unit.state.append(unit.set_state())  # Name of unit state
                    unit.systems = unit.default_eq(unit)
                    window.close()
                    oob_edit(sides, stats, unit, default)
        elif event == "eyear":  # Modify unit year.
            if unit.year != values["uyear"] and user_input(values["uyear"], minimum=stats[4][0], maximum=stats[4][1]):
                unit.year = values["uyear"]  # Checks and assigns new unit year.
                window.close()
                oob_edit(sides, stats, unit, default)
        elif event == "add":  # Add weapons or modify them with 0.
            for _ in eq_systems[unit.type[0]]:
                if values["wp"] == eq_systems[unit.type[0]][_][0]:
                    unit.add_system(_, values["amount"], default)
                    break
            window.close()
            oob_edit(sides, stats, unit, default)
        elif event == "Units":  # Show unit tab view only.
            oob_units(sides, stats, view_only=True)
        elif event == "wmodify":  # Add weapons or modify them with 0.
            for system in unit.systems.copy():
                for value in values.keys():
                    if value == eq_systems[unit.type[0]][system][0] and \
                            unit.systems[unit.define_system(value, True)] != values[value]:
                        unit.add_system(system, values[value], default)
                        break
            window.close()
            oob_edit(sides, stats, unit, default)
    window.close()
    oob_units(sides, stats, default=default)


# noinspection SpellCheckingInspection
vehicles = {
    1: {0: ("MBT", (90, 1, 2, 3, 4, 5, 6, 7, 13, 14), 8, 45),
        1: ("AFV", (91, 1, 2, 3, 4, 5, 6, 7), 8, 120),
        2: ("IFV", (92, 1, 2, 3, 4, 5, 6), 6, 120),
        3: ("APC", (93, 1, 2, 3, 6), 4, 200),
        4: ("SAM", (94, 1, 2, 3, 6, 8, 9, 10, 13), 4, 80),
        5: ("MLB", (95, 1, 2, 3, 6, 11, 12, 13), 4, 80)},
    2: {0: ("Small Multirole Aircraft", (90, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 4, 8),
        1: ("Medium Multirole Aircraft", (91, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 6, 10),
        2: ("Large Multirole Aircraft", (92, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 8, 20),
        3: ("Large Heavy Aircraft", (93, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 10, 4),
        4: ("Very Large Heavy Aircraft", (94, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 10, 4)},
    3: {0: ("Corvette", (90, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 4, 80),
        1: ("Frigate", (91, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 6, 100),
        2: ("Destroyer", (92, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 8, 120),
        3: ("Cruiser", (93, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 10, 140),
        4: ("Battlecruiser", (94, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 16, 200),
        5: ("Battleship", (95, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 20, 200),
        6: ("Light Carrier", (96, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 16, 40),
        7: ("Aircraft Carrier", (97, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 20, 80)}
}
# noinspection SpellCheckingInspection
vehicles_internal = {0: "MBT", 1: "AFV", 2: "IFV", 3: "APC", 4: "SAM", 5: "MLB", 6: "Small Multirole Aircraft",
                     7: "Medium Multirole Aircraft", 8: "Large Multirole Aircraft", 9: "Large Heavy Aircraft",
                     10: "Very Large Heavy Aircraft", 11: "Corvette", 12: "Frigate", 13: "Destroyer", 14: "Cruiser",
                     15: "Battlecruiser", 16: "Battleship", 17: "Light Carrier", 18: "Aircraft Carrier"}
# noinspection SpellCheckingInspection
eq_systems = {
    1: {1: ("Smoke (CM)", 2, [9], 0, 0),
        2: ("SK-APS (SCM)", 3, [8], 0, 0),
        3: ("HK-APS (CM)", 4, [9], 0, 0),
        4: ("ERA (CM)", 6, [9], 0, 0),
        5: ("NxRA (CM)", 8, [9], 0, 0),
        6: ("Applique (CM)", 3, [9], 0, 0),
        7: ("ATGM", 4, (1, 3), 3, 0),
        8: ("SR-SAM", 3, [2], 3, 0),
        9: ("MR-SAM", 3, [2], 6, 0),
        10: ("LR-SAM", 3, [2], 10, 3),
        11: ("MR-AShM", 6, [3], 4, 0),
        12: ("LR-AShM", 5, [3], 6, 0),
        13: ("Heavy MG Turret", 1, [2], 1, 0),
        14: ("Autocannon Turret", 2, [2], 1, 0),
        90: ("Tank gun", 5, [1], 2, 0),
        91: ("Autocannon", 2, (1, 2), 2, 0),
        92: ("Heavy MG", 1, (1, 2), 2, 0),
        93: ("Light MG", 1, [1], 1, 0),
        94: ("Crew Handheld Firearms", 1, [1], 1, 0),
        95: ("Crew Handheld Firearms", 1, [1], 1, 0)},
    2: {1: ("Flares (CM)", 2, [9], 0, 0),
        2: ("Chaff (CM)", 2, [9], 0, 0),
        3: ("ECM (SCM)", 2, [8], 0, 0),
        4: ("EWS (SCM)", 3, [8], 0, 0),
        5: ("SRAAM", 4, [2], 2, 0),
        6: ("MRAAM", 4, [2], 4, 0),
        7: ("LRAAM", 4, [2], 12, 3),
        8: ("AGM", 4, [1], 3, 0),
        9: ("MR-AShM", 6, [3], 4, 0),
        10: ("SEAD", 5, [6], 4, 0),
        11: ("Cruise Missile", 3, [1], 5, 0),
        12: ("Bomb", 2, [1], 1, 0),
        13: ("GBU", 4, [1], 1, 0),
        14: ("Drop Tank", 0, [0], 0, 0),
        90: ("Autocannon", 1, (1, 2), 1, 0),
        91: ("Autocannon", 2, (1, 2), 1, 0),
        92: ("Autocannon", 2, (1, 2), 1, 0),
        93: ("Defense Turrets", 1, [2], 1, 0),
        94: ("Defense Turrets", 1, [2], 1, 0)},
    3: {1: ("CIWS (SCM)", 1, (2, 8), 1, 0),
        2: ("DEW (SCM)", 2, (2, 8), 1, 0),
        3: ("ECM (SCM)", 1, [8], 0, 0),
        4: ("Smoke (CM)", 2, [9], 0, 0),
        5: ("Chaff (CM)", 2, [9], 0, 0),
        6: ("SR-SAM (CM)", 3, (2, 9), 3, 0),
        7: ("MR-SAM (CM)", 3, (2, 9), 6, 0),
        8: ("LR-SAM", 3, [2], 10, 3),
        9: ("MR-AShM", 6, [3], 4, 0),
        10: ("LR-AShM", 8, [3], 6, 0),
        11: ("Cruise Missile", 3, [1], 5, 0),
        90: ("Main Battery", 1, (1, 2, 3), 1, 0),
        91: ("Main Battery", 1, (1, 2, 3), 1, 0),
        92: ("Main Battery", 1, (1, 2, 3), 1, 0),
        93: ("Main Battery", 1, (1, 2, 3), 2, 0),
        94: ("Main Battery", 1, (1, 2, 3), 3, 0),
        95: ("Main Battery", 1, (1, 2, 3), 4, 0),
        96: ("Auxiliary Weapons", 1, (2, 3), 1, 0),
        97: ("Auxiliary Weapons", 1, (2, 3), 1, 0)}
}
# noinspection SpellCheckingInspection
state = ["KIA", "Heavily Damaged", "Major Damage taken", "Damaged", "Slightly damaged", "Scratched",
         "In nominal condition", "Worried", "New", "Withdrawing", "unknown"]

return_type = lambda x: "Surface Units" if x == 1 else ("Naval Units" if x == 3 else "Aerial Units")


def category(unit):
    """

    @param unit:
    @return:
    """
    if unit < 6:
        return [1, unit, vehicles[1][unit][0]]
    elif 5 < unit < 11:
        return [2, unit - 6, vehicles[2][unit - 6][0]]
    else:
        return [3, unit - 11, vehicles[3][unit - 11][0]]


def user_input(value, minimum=0, maximum=1, enter=False, string=False, check="", skip=False):
    """
    User input function.
    :param minimum: Lower limit to number check.
    :param maximum: Upper limit to number check.
    :param string: If string is permitted as input.
    :param check: String input must have same format as check using RegEx.
    :return: Returns user input.
    @param skip:
    @param string:
    @param check:
    @param enter:
    @param maximum:
    @param minimum:
    @param value: Checked value
    """
    from re import match
    try:
        if (string and match(check, value) is not None) or minimum <= int(value) <= maximum or enter:
            return True
        elif not skip:
            sg.PopupAutoClose("Invalid input!", auto_close_duration=1)
        return False
    except ValueError:
        if enter:
            return True
        elif not skip:
            sg.PopupAutoClose("Invalid input!", auto_close_duration=1)
        return False


def cut(unit):
    """
    Removes the asset from asset name.
    @param unit:
    @return:
    """
    if isinstance(unit, str):
        return unit.replace("asset", "")
    else:
        return unit.name.replace("asset", "")


def unit_listing(sides, col):
    """

    @param sides:
    @param col:
    @return:
    """
    if len(sides):
        for unit in sides.copy():  # Listing of units.
            systems = "Eq: "
            counter = 0
            col.append([sg.T(f"{unit.name} | {unit.distance} | {unit.state[0]} | ", key=f"{cut(unit)} ",
                             right_click_menu=['&Right', [f"Damage-{cut(unit)}"]])])
            for item in unit.systems:
                counter += 1
                if counter <= 6:  # Overflow prevention adding another row with \n.
                    systems += f"{unit.define_system(item)}: {unit.systems[item]}, "  # Adds to systems.
                else:
                    systems += f"\n{unit.define_system(item)}: {unit.systems[item]}, "
                    counter = 0
            col[-1].append(sg.T(f"{systems}", key=f"{cut(unit)}"))
    else:
        return [None]
    return col


if __name__ == "__main__":
    import traceback

    oob()
    try:
        oob()
    except Exception as e:
        print(f"Program crashed with this error: {e}, {type(e)}, {e.args}, \nPlease report the error to the "
              f"developers.\n")
        print(traceback.format_exc())
        input("Program will restart after pressing enter (in console):")

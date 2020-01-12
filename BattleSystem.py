"""
Welcome
"""

from sys import exit

# noinspection PyPep8Naming
import PySimpleGUI as sg


class Asset:
    """
    Asset objects are the units itself.
    """

    def __init__(self, name, side, unit_type, year):
        has_radar = lambda x: True if x == 4 else False
        set_distance = lambda x: -6 if x == 1 else 6
        self.default_eq = lambda x: {vehicles[x.type[0]][x.type[1]][1][0]: vehicles[x.type[0]][x.type[1]][3]}
        self.name = name
        self.type = category(unit_type)  # 0 Class 1 Subclass 2 Internal, 3 str name
        self.type.insert(2, unit_type)
        self.state = [vehicles[self.type[0]][self.type[1]][2]]  # 0 State 1 str state
        self.state.append(self.set_state())
        self.side = side  # Fighting side
        self.year = year  # Year of origin
        self.distance = set_distance(side)
        self.systems = self.default_eq(self)
        self.has_radar = has_radar(unit_type)

    def __str__(self):
        return str(f"{self.name}_{self.type[3]}: {str(self.state[1])} | Dist: {self.distance}")

    def set_state(self, finals=False):
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
        if not finals and self.state[0] < vehicles[self.type[0]][self.type[1]][2] // 2:
            result = state[9]
        return result

    def define_system(self, system):
        """
        Defines system str name.
        :param system:  System int defining system name string.
        :return:        Returns str of the obj name.
        """
        try:
            return eq_systems[self.type[0]][system][0]
        except KeyError:
            return "weapon system"


def oob():
    """
    Main body for input
    """
    side1 = []
    side2 = []
    print("Do not dare to close this or I will haunt you in the sleep!")

    stats = oob_stats()
    sides = oob_asset_creator(stats, side1, side2)

    veh = air = sea = False
    for unit in sides[1] + sides[2]:
        if unit.type[0] == 1:
            veh = True
        elif unit.type[0] == 2:
            air = True
        elif unit.type[0] == 3:
            sea = True
        if veh and sea and air:
            break
    if veh:
        oob_eq(sides, stats, 1)
    if air:
        oob_eq(sides, stats, 2)
    if sea:
        oob_eq(sides, stats, 3)

    oob_units(sides, stats)
    print("after")
    pass


# noinspection SpellCheckingInspection
def oob_stats(bypass=True, def_years=None):
    """
    Introducing welcome!
    """
    if def_years is None:
        def_years = [1945, 2020]
    version = "1.0.0"
    result = True

    sg.theme('DarkBlue13')
    # All the stuff inside your window.
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
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event is None or event == "Exit":  # if user closes window or clicks cancel
            break
        elif event == "Finish" or event == "\r":  # Button checks validity and then returns result.
            if (user_input(values["year"], def_years[0], def_years[1]) and user_input(values["a"], maximum=81)
                    and user_input(values["b"], maximum=81)):
                result = [values["year"], values["a"], values["b"], version, def_years]
                break
            elif bypass:
                values["a"] = 4
                values["b"] = 4
                values["year"] = 1999
                result = [values["year"], values["a"], values["b"], version, def_years]
                break
            else:
                continue
        elif event == "Switch default years":
            def_years = oob_ch_year(def_years, version)
            window.close()
            result = oob_stats(def_years=def_years)

    window.close()
    # noinspection PyUnboundLocalVariable
    return result


def oob_ch_year(def_years, version):
    """

    @param def_years:
    @param version:
    @return:
    """
    sg.theme('DarkBlue13')
    # All the stuff inside your window.
    layout = [[sg.T("Choose new default year:")],
              [sg.Input(f"{def_years[0]}", size=(6, 1), key="minimal"),
               sg.Input(f"{def_years[1]}", size=(6, 1), key="maximal")], [sg.B("Edit")]]

    window = sg.Window(f'Battle System {version}', layout, return_keyboard_events=True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event is None:  # if user closes window or clicks cancel
            break
        elif event == "Edit" or event == "\r":  # Button checks validity and then returns result.
            if user_input(values["minimal"], 1900, int(values["maximal"])) and \
                    user_input(values["maximal"], int(values["minimal"]), 2200):
                def_years[0] = int(values["minimal"])
                def_years[1] = int(values["maximal"])
                break
    window.close()
    return def_years


def oob_asset_creator(stats, side1, side2, i=1):  # Stats 0 def_year, 1 side_a, 2 side_b
    """
    Specify each asset category, year and its type
    :return: Returns unit category (veh, air, sea), type (subtype of category) and year of production.
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
              [sg.T("Amount:             "), sg.In(justification="center")],
              [sg.T("Year if different:  "), sg.In(f"{stats[0]}", justification="center")],
              [sg.Button('Next', size=(20, 2), button_color=("#000000", "#dbc867"))]]

    while True:
        window = sg.Window(f'Battle System {stats[3]}', layout, return_keyboard_events=True)
        while True:
            length = 0
            event, values = window.read()
            if event is None:  # if user closes window or clicks cancel
                exit()
            elif event == "Next" or event == "\r":
                if user_input(values[20], 1945, 2020, enter=True) and \
                        user_input(values[19], minimum=1, maximum=int(stats[i])):
                    for j in range(len(values) - 2):
                        if values[j]:
                            if values[20] != "":
                                if int(values[20]) != stats[0]:
                                    stats[0] = int(values[20])
                            length = len(locals()['side' + str(i)])
                            for k in range(int(values[19])):
                                locals()["side" + str(i)].append(f"asset{i}_{length + k}")

                                locals()["side" + str(i)][length + k] = Asset(f"asset{i}_{length + k}", i, j, stats[0])

                            stats[i] -= int(values[19])
                            window.close()
                            if stats[1] == 0 and stats[2] == 0:
                                break
                            if stats[i] == 0 or i == 2:
                                oob_asset_creator(stats, side1, side2, 2)
                            else:
                                oob_asset_creator(stats, side1, side2)
                            break
                    break
        window.close()
        return {1: side1, 2: side2}


def oob_eq(sides, stats, unit_type):
    """

    @param unit_type:
    @param sides:
    @param stats:
    """

    template_unit = Asset("template_unit", 1, 1, 2000)

    sg.theme('DarkBlue13')
    layout = [[sg.T(f"Equipment Editor - {return_type(unit_type)}", justification="center")],
              [sg.Text('_' * (len(sides[1]) + len(sides[2]) * 30))], []]
    leftcol = []
    column1 = [[]]
    column2 = [[]]
    leftcol.append([sg.T("Units:", size=(14, 1))])

    for i in range(1, 3):  # Making the grid
        column = locals()["column" + f"{i}"]
        for asset in sides[i]:  # of units
            if asset.type[0] == unit_type:
                column[-1].append(sg.T(f"{cut(asset)} ", justification="left", auto_size_text=True,
                                       key=f"{cut(asset)}"))
        for item in eq_systems[unit_type]:  # of weapons
            if item < 90:
                if not i == 2:
                    for unit in sides[1] + sides[2]:
                        if unit.type[0] == unit_type:
                            template_unit = unit
                    leftcol.append([sg.T(f"{template_unit.define_system(item)}", size=(14, 1))])
                column.append([])
                for asset in sides[i]:
                    if asset.type[0] == unit_type and item in vehicles[asset.type[0]][asset.type[1]][1]:
                        column[-1].append(sg.InputText(default_text="0", size=(4, 1),
                                                       key=f"{str(asset.name) + '_' + str(item)}"))
                    elif asset.type[0] == unit_type:

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
    # Event Loop to process "events" and get the "values" of the inputs
    while True:  # Working with the grid inputs, checking and adding to assets.
        event, values = window.read()
        if event in (None, "Exit"):  # if user closes window or clicks cancel
            exit()
        elif event == "Finish" or event == "\r":  # Button checks validity and then returns result.
            check = True
            for asset in sides[1] + sides[2]:
                if asset.type[0] == unit_type:
                    for j in range(1, len(eq_systems[asset.type[0]]) - len(vehicles[asset.type[0]]) + 1):
                        try:
                            if not user_input(values[str(asset.name) + '_' + str(j)], maximum=400):
                                check = False
                                break
                        except KeyError:
                            pass
            if check:
                for asset in sides[1] + sides[2]:
                    if asset.type[0] == unit_type:
                        for j in range(1, len(eq_systems[asset.type[0]]) - len(vehicles[asset.type[0]]) + 1):
                            try:
                                if user_input(values[str(asset.name) + '_' + str(j)], minimum=1, maximum=400,
                                              skip=True):
                                    asset.systems[j] = values[str(asset.name) + '_' + str(j)]
                            except KeyError:
                                pass
                break
            else:
                continue
        elif event == "Units":
            oob_units(sides, stats, view_only=True)
    window.close()


def oob_units(sides, stats, clone=None, default=False, view_only=False):
    """

    @param sides:
    @param stats:
    @param clone:
    @param default:
    @param view_only:
    @return:
    """
    sg.theme('DarkBlue13')
    layout = [[sg.T(f"Unit Editor - Df: {default} | Copied: {clone}", justification="center")]]
    column = []

    for unit in sides[1] + sides[2]:
        if view_only:
            column.append([sg.T(f"{cut(unit)} - {unit.type[3]}", key=f"{unit.name}"), sg.T(f"R: {unit.has_radar}")])
        else:
            column.append([sg.Button(f"{cut(unit)} - {unit.type[3]}", key=f"{unit.name}"),
                           sg.T(f"R: {unit.has_radar}")])
        column.append([sg.T(f"{unit.year}", size=(5, 1))])
        systems = ""
        for item in unit.systems:
            systems += f"{str(eq_systems[unit.type[0]][item][0])}: {unit.systems[item]}, "
        column[-1].append(sg.T(f"Equipment: {systems}", key=f"{cut(unit)}",
                               right_click_menu=['&Right', [f"Copy-{cut(unit)}", f"Paste-{cut(unit)}"]]))

    layout.append([sg.Col(column, scrollable=True, size=(500, 500))])
    menu_def = [['&Edit', ['Exit']], ['&Properties', ["&Switch default editing"]]]

    layout.append([sg.Button("Start Battle", key="battle", size=(20, 5), button_color=("#000000", "#dbc867"))])
    layout.append([sg.Menu(menu_def)])

    window = sg.Window(f'Battle System {stats[3]}', layout, resizable=True,
                       size=(600, 600), return_keyboard_events=True)

    while True:  # Working with the grid inputs, checking and adding to assets.
        event, values = window.read()
        if event in (None, "Close"):
            if not view_only:
                exit()
            else:
                break
        elif event == "Exit":
            window.close()
            return True
        elif "Copy-" in event:
            clone = {}
            name = "asset" + event.replace("Copy-", "")
            for unit in sides[1] + sides[2]:
                if unit.name == name:
                    import copy
                    clone = copy.deepcopy(unit.systems)
            window.close()
            oob_units(sides, stats, clone, default)
        elif "Paste-" in event and clone is not None:
            name = "asset" + event.replace("Paste-", "")
            for unit in sides[1] + sides[2]:
                if unit.name == name:
                    for item in clone:
                        if default and item in vehicles[unit.type[0]][unit.type[1]][1]:
                            unit.systems[item] = clone[item]
                        elif item < 90:
                            unit.systems[item] = clone[item]
            window.close()
            oob_units(sides, stats, clone, default)
        elif event == "Switch default editing" and not view_only:
            window.close()
            if default:
                oob_units(sides, stats)
            else:
                oob_units(sides, stats, default=True)
        elif event in ("\r", "battle"):
            break
        else:  # Clicking unit button
            for unit in sides[1] + sides[2]:
                if unit.name == event:
                    window.close()
                    oob_edit(sides, stats, unit, default)
    window.close()


def oob_edit(sides, stats, unit, default=False):
    """

    @param sides:
    @param stats:
    @param unit:
    @param default:
    """
    sg.theme('DarkBlue13')
    layout = []
    frame_layout = []
    year_layout = []
    type_layout = []
    column = []

    for item in unit.systems:
        if not default:
            if item < 90:
                column.append([sg.T(f"{eq_systems[unit.type[0]][item][0]}", size=(16, 1), auto_size_text=True)])
                column[-1].append(sg.InputText(f"{unit.systems[item]}", size=(4, 1),
                                               key=eq_systems[unit.type[0]][item]))
        else:
            column.append([sg.T(f"{eq_systems[unit.type[0]][item][0]}", size=(16, 1), auto_size_text=True)])
            column[-1].append(sg.InputText(f"{unit.systems[item]}", size=(4, 1), key=eq_systems[unit.type[0]][item]))

    adding = []
    for _ in eq_systems[unit.type[0]]:  # Listing of weapons for weapons adding.
        if default and _ in vehicles[unit.type[0]][unit.type[1]][1]:
            adding.append(eq_systems[unit.type[0]][_][0])
        elif _ < 90 and _ in vehicles[unit.type[0]][unit.type[1]][1]:
            adding.append(eq_systems[unit.type[0]][_][0])

    types = []
    for i in vehicles:
        for j in vehicles[i]:
            types.append(vehicles[i][j][0])

    frame_layout.append([sg.Button("Add Weapon", key="add"),
                         sg.Combo(adding, size=(10, 1), key="wp", enable_events=True),
                         sg.T("#"), sg.InputText(key="amount", size=(5, 1))])
    type_layout.append([sg.T("Change Type:", size=(6, 1)), sg.Combo(types, size=(10, 1), key="type"),
                        sg.B("Change", tooltip="WARNING - Will erase the unit weapons!")])
    year_layout.append([sg.T("Unit year: ", size=(8, 1)), sg.InputText(f"{unit.year}", key="uyear", size=(4, 1))])

    frame_layout.append([sg.Col(column)])
    layout.append([sg.Button("Modify / Close"), sg.T(f"Unit: {unit}")])
    layout.append([sg.Frame("Year Editor", year_layout, font='Any 12', title_color='white')])
    layout[-1].append(sg.Frame("Type Editor", type_layout, font='Any 12', title_color='white'))
    layout.append([sg.Frame("Systems Editor", frame_layout, font='Any 12', title_color='white')])

    menu_def = [['&Edit', ['Units', '---', 'Exit']], ['&Properties', ["&Switch default editing"]]]
    layout.append([sg.Menu(menu_def)])

    window = sg.Window(f'Battle System {stats[3]}', layout, resizable=True,
                       size=(600, 600), return_keyboard_events=True)

    while True:  # Working with the grid inputs, checking and adding to assets.
        event, values = window.read()
        if event in (None, "Exit"):
            exit()
        elif event in ("Modify / Close", "\r"):  # Save & Close
            for item in unit.systems.copy():
                if not default:
                    if item < 90 and unit.systems[item] != values[eq_systems[unit.type[0]][item]]:
                        unit.systems[item] = int(values[eq_systems[unit.type[0]][item]])
                    if item < 90 and unit.systems[item] == 0:
                        unit.systems.pop(item)
                else:
                    if unit.systems[item] != values[eq_systems[unit.type[0]][item]]:
                        unit.systems[item] = int(values[eq_systems[unit.type[0]][item]])
                    if unit.systems[item] == 0:
                        unit.systems.pop(item)
            if unit.year != values["uyear"] and user_input(values["uyear"], minimum=stats[4][0], maximum=stats[4][1]):
                unit.year = values["uyear"]
            break
        elif event == "add":
            for _ in eq_systems[unit.type[0]]:
                if values["wp"] == eq_systems[unit.type[0]][_][0] and int(values["amount"]) == 0:
                    if _ in unit.systems:
                        unit.systems.pop(_)
                        break
                elif values["wp"] == eq_systems[unit.type[0]][_][0] and \
                        user_input(values["amount"], minimum=1, maximum=400):
                    unit.systems[_] = values["amount"]
                    break
            window.close()
            oob_edit(sides, stats, unit, default)
        elif event == "Switch default editing":
            window.close()
            if default:
                oob_edit(sides, stats, unit)
            else:
                oob_edit(sides, stats, unit, True)
        elif event == "Change":
            for vehicle in vehicles_internal:
                if values["type"] == vehicles_internal[vehicle]:
                    unit.type = category(vehicle)  # Class and subclass
                    unit.type.insert(2, vehicle)
                    unit.state = [vehicles[unit.type[0]][unit.type[1]][2]]  # How much alive asset is
                    unit.state.append(unit.set_state())  # Name of unit state
                    unit.systems = unit.default_eq(unit)
                    window.close()
                    oob_edit(sides, stats, unit, default)
        elif event == "Units":
            oob_units(sides, stats, view_only=True)
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
# noinspection SpellCheckingInspection
state = ["KIA", "Heavily Damaged", "Major Damage taken", "Damaged", "Slightly damaged", "Scratched",
         "In nominal condition", "Worried", "New", "Withdrawing", "unknown"]


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
        if string and match(check, value) is not None:
            return True
        elif minimum <= int(value) <= maximum:
            return True
        elif enter:
            return True
        if not skip:
            sg.PopupAutoClose("Invalid input!", auto_close_duration=1)
        return False
    except ValueError:
        if enter:
            return True
        if not skip:
            sg.PopupAutoClose("Invalid input!", auto_close_duration=1)
        return False


def cut(unit):
    """
    Removes the asset from asset name.
    @param unit:
    @return:
    """
    if isinstance(unit, str):
        result = unit.replace("asset", "")
    else:
        result = unit.name.replace("asset", "")
    return result


def return_type(num):
    """

    @param num:
    @return:
    """
    if num == 1:
        return "Surface Units"
    elif num == 2:
        return "Aerial Units"
    else:
        return "Naval Units"


if __name__ == "__main__":
    oob()

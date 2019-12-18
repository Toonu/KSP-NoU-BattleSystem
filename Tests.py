class Asset:
    def __init__(self, type, state, side, year, dice):
        self._type = type
        self._state = state
        self._dice = dice
        self._side = side
        self._year = year
        self.system = self.createsystems()
        self.__message = ""

    def __str__(self):
        return str(self._type)

    def createsystems(self):
        return Asset.Systems(self, 1, self._year, 5)

    class Systems:
        def __init__(self, asset, system_type, year, amount):
            self.asset = asset
            self._amount = amount
            self._year = year
            self._name = system_type
            self._system_type = system_type
            self._reliability = system_type
            self._speed = system_type


test = Asset(1, 3, 1, 1990, 5)
print(test._type)
print(test.system._system_type)
test._type = 2
print(test._type)
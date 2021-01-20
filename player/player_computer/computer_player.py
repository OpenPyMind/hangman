from player.player import AbstractPlayer


class ComputerPlayer(AbstractPlayer):
    def __init__(self, number):
        super().__init__(number)
        self.__number = number
        self.__role = None
        self.__name = None
        self.__word = None
        self.__wins = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, other):
        self.__role = other

    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, value):
        self.__word = value

    @property
    def wins(self):
        return self.__wins

    @wins.setter
    def wins(self, value):
        self.__wins += 1

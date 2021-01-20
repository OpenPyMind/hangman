from player.player import AbstractPlayer


class HumanPlayer(AbstractPlayer):
    def __init__(self, number):
        super().__init__(number)
        self.__number = number
        self.__name = self.set_name()
        self.__role = None
        self.__word = None
        self.__wins = 0

    def set_name(self):
        name = input(f"Player {self.__number}, enter your name: ")
        return name

    def pick_word(self):
        word = input(f"{self.__name}, pick a word. It should be an English word without punctuation or numbers:\n")
        try:
            if not word.isalpha():
                raise ValueError
            self.word = word.lower()
        except ValueError:
            return self.pick_word()

    @property
    def name(self):
        return self.__name

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


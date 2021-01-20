from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    @abstractmethod
    def __init__(self, number):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def role(self):
        pass

    @role.setter
    @abstractmethod
    def role(self, other):
        pass

    @property
    @abstractmethod
    def word(self):
        pass

    @word.setter
    def word(self, value):
        pass

    @property
    @abstractmethod
    def wins(self):
        pass

    @wins.setter
    @abstractmethod
    def wins(self, value):
        pass
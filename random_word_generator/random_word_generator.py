import json
from random import choice
import urllib.request


class RandomWordGenerator:
    __URL = "https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json"

    def __init__(self):
        self.__url_request = urllib.request.urlopen(self.__URL)
        self.__words = json.loads(self.__url_request.read())

    def __fetch_random_word(self):
        """Returns a random English word"""
        return choice(self.__words)

    @property
    def fetch_random_word(self):
        return self.__fetch_random_word()

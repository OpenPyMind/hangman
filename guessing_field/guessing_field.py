class GuessingField:
    __SYMBOLS = {
        "space": " ",
        "underline": "-"
    }

    def __init__(self, word_to_guess: str):
        self.__word_to_guess = word_to_guess
        self.__field_values: list = self.__initialize_field_values()
        self.__field: str = self.__draw_field()
        self.__guesses: list = []

    def evaluate_guess(self, guess: str) -> bool:
        """The guessed letter is entered into 'self.__guesses' list. Returns False if the letter is already there or if
        the guess is wrong, returns True otherwise, while updating the field values and the field string
        representation"""

        self.__guesses.append(guess)
        if (guess not in self.__word_to_guess) or (self.__guesses.count(guess) > 1):
            return False
        self.__update_field_values(guess)
        self.__field = self.__draw_field()
        return True

    def __draw_field(self) -> str:
        field = ""
        for row in self.__field_values:
            field += " ".join(row) + "\n"

        return field

    def __initialize_field_values(self) -> list:
        """Creates an initial guessing field values 2D-matrix"""

        width = len(self.__word_to_guess)
        letters_space = [self.__SYMBOLS["space"]] * width
        footer = [self.__SYMBOLS["underline"]] * width
        field_values = [letters_space, footer]
        return field_values

    def __update_field_values(self, guessed_letter: str) -> None:
        for idx, c in enumerate(self.__word_to_guess):
            if guessed_letter == c:
                self.__field_values[0][idx] = guessed_letter

    @property
    def field(self):
        return self.__field

    @property
    def guesses(self):
        return self.__guesses

    @property
    def correct_guesses(self):
        return "".join(self.__field_values[0])

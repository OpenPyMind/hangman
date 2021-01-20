from typing import List, Tuple


class Gallows:
    __SYMBOLS = {
            "start footer": " GAME STARTS! ",
            "space": " ",
            "base": "=",
            "vertical": "|",
            "crossbar": "_",
            "head": "O",
            "forward limb": "/",
            "reverse limb": "\\"
        }

    def __init__(self):
        self.__gallows_height = 9
        self.__gallows_width = 14
        self.__depiction_values = self.__initiate_depiction_values()
        self.__draw_hangee_counter = 0
        self.__has_started = False

    def __draw(self) -> str:
        """Returns a string representation of the gallows."""
        depiction = ""
        for row in self.__depiction_values:
            depiction += "".join(row) + "\n"
        return depiction

    def __initiate_depiction_values(self) -> List[List]:
        """The initial gallows values (8 x 13 matrix) will be set here. Return the matrix."""
        initial = []
        for i in range(self.__gallows_height):
            row = []
            for j in range(self.__gallows_width):
                if i == 0:
                    if 3 <= j <= 6:
                        row.append(self.__SYMBOLS["crossbar"])
                    else:
                        row.append(self.__SYMBOLS["space"])
                elif i == 1:
                    if j in (2, 7):
                        row.append(self.__SYMBOLS["vertical"])
                    else:
                        row.append(self.__SYMBOLS["space"])
                elif 2 <= i <= 6:
                    if j == 2:
                        row.append(self.__SYMBOLS["vertical"])
                    else:
                        row.append(self.__SYMBOLS["space"])
                elif i == 7:
                    row.append(self.__SYMBOLS["base"])
                elif i == 8:
                    row.append(self.__SYMBOLS["start footer"][j])
            initial.append(row)
        return initial

    def update_depiction_values(self, overall_moves) -> None:
        """Updates the value matrix for the gallows.
        Removes the 'GAME STARTS!' footer once the first guess has been made.
        If the '__hangee_limb_coordinates' function returns False (KeyError), no action will be taken (correct guess).
        Otherwise, the gallows matrix values will be updated (if the hangee guessed wrongly)"""

        if overall_moves == 1:
            self.__depiction_values[self.__gallows_height - 1] = [self.__SYMBOLS["space"]] * self.__gallows_width
        coordinates_value = self.__hangee_limb_coordinates()
        if not coordinates_value:
            return
        i, j, value = coordinates_value
        self.__depiction_values[i][j] = value

    def __hangee_limb_coordinates(self) -> Tuple[int, int, str] or False:
        """Upon incrementing the 'draw_hangee_counter', the matrix coordinates and the limb symbols will be returned."""

        limb_coordinates = {
            1: (2, 7, self.__SYMBOLS["head"]),
            2: (3, 7, self.__SYMBOLS["vertical"]),
            3: (3, 6, self.__SYMBOLS["forward limb"]),
            4: (3, 8, self.__SYMBOLS["reverse limb"]),
            5: (4, 6, self.__SYMBOLS["forward limb"]),
            6: (4, 8, self.__SYMBOLS["reverse limb"]),
        }
        try:
            return limb_coordinates[self.draw_hangee_counter]
        except KeyError:
            return False

    @property
    def draw_hangee_counter(self):
        return self.__draw_hangee_counter

    @draw_hangee_counter.setter
    def draw_hangee_counter(self, value):
        self.__draw_hangee_counter += 1

    def __str__(self) -> str:
        return self.__draw()

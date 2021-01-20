from os import name, system
from typing import Tuple, Callable

from player.player_computer.computer_player import ComputerPlayer
from player.player_human.human_player import HumanPlayer
from random_word_generator.random_word_generator import RandomWordGenerator
from gallows.gallows import Gallows
from guessing_field.guessing_field import GuessingField


class Game:
    __PLAYERS_NUMBERS = [1, 2]
    __PLAYERS_ROLES = ["hangman", "hangee"]

    def __init__(self):
        self.__gallows = None
        self.__guessing_field = None
        self.__word_generator = None
        self.__game_mode = None
        self.__player_1 = None
        self.__player_2 = None

    def setup_main(self) -> None:
        """Main game logic"""
        print(self.__welcome_message())
        player_1_number = self.__PLAYERS_NUMBERS[0]
        player_2_number = self.__PLAYERS_NUMBERS[1]

        self.__game_mode = self.__set_game_mode()
        if self.__game_mode == "c":
            self.__player_1 = ComputerPlayer(player_1_number)
            self.__player_1.name = "Computer"
            self.__player_2 = HumanPlayer(player_2_number)
            self.__pvc_mode()
        elif self.__game_mode == "p":
            self.__player_1 = HumanPlayer(player_1_number)
            self.__player_2 = HumanPlayer(player_2_number)
            while self.__player_2.name.lower() == self.__player_1.name.lower():
                print(f"Player {player_2_number}, pick a different name!")
                self.__player_2 = HumanPlayer(player_2_number)
            self.__pvp_mode()

    def __pvp_mode(self) -> None:
        """Sets up player vs player game mode"""
        hangman, hangee = self.__assign_player_roles_pvp()
        hangman.pick_word()
        self.__clear_screen()
        self.__gallows = Gallows()
        self.__guessing_field = GuessingField(hangman.word)
        self.__game_loop(hangman, hangee)

    def __pvc_mode(self) -> None:
        """Sets up player vs computer game mode"""
        hangman, hangee = self.__assign_player_roles_pvc()
        self.__word_generator = RandomWordGenerator()
        self.__gallows = Gallows()
        hangman.word = self.__word_generator.fetch_random_word
        self.__guessing_field = GuessingField(hangman.word)
        self.__game_loop(hangman, hangee)

    def __game_loop(self, hangman: HumanPlayer or ComputerPlayer, hangee: HumanPlayer) -> None:
        """Both game modes converge here."""
        errors_committed = 0
        while True:
            print(self.__gallows)
            print(self.__guessing_field.field)
            has_lost = self.__has_lost(errors_committed)
            has_won = self.__has_won(hangman.word, self.__guessing_field.correct_guesses)
            if has_won or has_lost:
                if has_lost:
                    print(f"{hangee.name}, you lost!")
                    print(f"The word was '{hangman.word}'")
                    hangman.wins = "increment"
                if has_won:
                    print(f"{hangee.name}, you won!")
                    hangee.wins = "increment"
                if self.__continue_playing():
                    if not self.__switch_game_mode():
                        if self.__game_mode == "p":
                            self.__pvp_mode()
                        elif self.__game_mode == "c":
                            self.__pvc_mode()
                    else:
                        self.setup_main()
                else:
                    print(self.__statistics())
                    return

            moves = len(self.__guessing_field.guesses)
            if moves == 0:
                print(f"{hangee.name}, the word is {len(hangman.word)} letters long.")
            guess = self.__guess(hangee)
            if not self.__guessing_field.evaluate_guess(guess):
                print(f"{hangee.name}, you guessed wrong!")
                self.__gallows.draw_hangee_counter = "increment"
            else:
                print(f"{hangee.name}, your guess is correct!")
            self.__gallows.update_depiction_values(moves)

            print(f"\nGuessed letters so far: {', '.join(self.__guessing_field.guesses)}")
            errors_committed = self.__gallows.draw_hangee_counter
            print(f"Errors committed: {errors_committed}\n")

    def __guess(self, hangee: HumanPlayer) -> str:
        """Will check for guess validity"""
        guess = input(f"{hangee.name}, enter your guess. It must be an English alphabet letter: ")
        try:
            if not (guess.isalpha() and len(guess) == 1):
                raise ValueError
            return guess.lower()
        except ValueError:
            return self.__guess(hangee)

    def __assign_player_roles_pvp(self) -> Tuple[HumanPlayer, HumanPlayer]:
        """Assigns player roles in player vs player mode (hangman and hangee)"""
        plays_as_hangman = input(f"{self.__player_1.name}, do you want to be the hangman? y/other: ")
        hangman, hangee = None, None
        if plays_as_hangman == "y":
            self.__player_1.role = self.__PLAYERS_ROLES[0]
            self.__player_2.role = self.__PLAYERS_ROLES[1]
            hangman, hangee = self.__player_1, self.__player_2
        else:
            self.__player_1.role = self.__PLAYERS_ROLES[1]
            self.__player_2.role = self.__PLAYERS_ROLES[0]
            hangman, hangee = self.__player_2, self.__player_1
        return hangman, hangee

    def __assign_player_roles_pvc(self) -> Tuple[ComputerPlayer, HumanPlayer]:
        """Assigns player roles in player vs computer mode (hangman and hangee)"""
        self.__player_1.role = self.__PLAYERS_ROLES[0]
        self.__player_2.role = self.__PLAYERS_ROLES[1]
        hangman, hangee = self.__player_1, self.__player_2
        return hangman, hangee

    def __set_game_mode(self) -> str or Callable:
        """Performs validity checks for entered game mode abbreviation and returns the mode if valid"""
        mode = input("Press 'c' for player vs. computer mode or 'p' for player vs. player mode: ")
        try:
            if mode not in ("c", "p"):
                raise ValueError
            return mode
        except ValueError:
            return self.__set_game_mode()

    def __switch_game_mode(self) -> bool:
        choice = input(f"{self.__player_1.name}, {self.__player_2.name}, do you want to switch game mode? y/other: ")
        return choice == "y"

    def __continue_playing(self) -> bool:
        """Prompts the players whether they wont to keep playing the game"""
        choice = input(f"{self.__player_1.name}, {self.__player_2.name}, do you want to continue playing? y/other: ")
        return choice == "y"

    def __statistics(self) -> str:
        """Returns string with the game statistics of the current session"""

        wins_p_1 = self.__player_1.wins
        wins_p_2 = self.__player_2.wins
        overall_winner = None
        if wins_p_1 > wins_p_2:
            overall_winner = self.__player_1.name
        elif wins_p_1 < wins_p_2:
            overall_winner = self.__player_2.name
        else:
            overall_winner = "draw"
        statistics_str = f"{self.__player_1.name} wins: {wins_p_1}\n" \
                         f"{self.__player_2.name} wins: {wins_p_2}\n" \
                         f"Overall winner: {overall_winner}"

        return statistics_str

    @staticmethod
    def __has_lost(errors_committed: int) -> bool:
        """Losing condition check"""
        return errors_committed == 6

    @staticmethod
    def __has_won(hangman_word: str, hangee_correct_guesses) -> bool:
        """Winning condition check"""
        return hangman_word == hangee_correct_guesses

    @staticmethod
    def __clear_screen():
        """Clears the screen in player vs player mode, after the hangman has entered the word to be guessed"""
        if name == "nt":
            _ = system("cls")
        else:
            esc = chr(27)
            print(esc + "[2j")

    @staticmethod
    def __welcome_message():
        message = """
Welcome to this hangman game. It supports both player vs. player and player vs. computer modes.
After six wrong guesses, you've lost the game.
Beware! If you enter an already correctly guessed letter, it will be counted as an error!
Same goes for repeating wrong guesses!
Enjoy the game!
"""
        return message

import numpy as np
import pandas


class Board:
    def __init__(self):
        self.state = np.zeros((15, 15), "str")
        self.temp_state = np.zeros((15, 15), "str")
        self.multiplier = np.array((
            ("tw", "", "", "dl", "", "", "", "tw", "", "", "", "dl", "", "", "tw"),
            ("", "dw", "", "", "", "tl", "", "", "", "tl", "", "", "", "dw", ""),
            ("", "", "dw", "", "", "", "dl", "", "dl", "", "", "", "dw", "", ""),
            ("dl", "", "", "dw", "", "", "", "dl", "", "", "", "dw", "", "", "dl"),
            ("", "", "", "", "dw", "", "", "", "", "", "dw", "", "", "", ""),
            ("", "tl", "", "", "", "tl", "", "", "", "tl", "", "", "", "tl", ""),
            ("", "", "dl", "", "", "", "dl", "", "dl", "", "", "", "dl", "", ""),
            ("tw", "", "", "dl", "", "", "", "", "", "", "", "dl", "", "", "tw"),
            ("", "", "dl", "", "", "", "dl", "", "dl", "", "", "", "dl", "", ""),
            ("", "tl", "", "", "", "tl", "", "", "", "tl", "", "", "", "tl", ""),
            ("", "", "", "", "dw", "", "", "", "", "", "dw", "", "", "", ""),
            ("dl", "", "", "dw", "", "", "", "dl", "", "", "", "dw", "", "", "dl"),
            ("", "", "dw", "", "", "", "dl", "", "dl", "", "", "", "dw", "", ""),
            ("", "dw", "", "", "", "tl", "", "", "", "tl", "", "", "", "dw", ""),
            ("tw", "", "", "dl", "", "", "", "tw", "", "", "", "dl", "", "", "tw")
        ))
        self.dictionary = pandas.read_csv("dictionary.csv")
        self.dictionary = list(self.dictionary.to_numpy())
        for i in range(len(self.dictionary)):
            self.dictionary[i] = self.dictionary[i][0]

    def update_board(self):
        self.state = self.temp_state.copy()

    def is_valid(self, word):
        return word in self.dictionary  # outputs the boolean decision "word is in dictionary?"

    def is_placeable(self, word, position, orientation, player):
        self.temp_state = self.state.copy()
        word_set = []
        for letter in word:
            word_set.append(letter)
        for letter in word:
            square = self.temp_state[position[1]][position[0]]
            if square == letter:
                word_set.remove(letter)
            elif square != "":
                return False, []
            if orientation == "h":
                position[0] += 1
            else:
                position[1] += 1
        pieces = player.pieces.copy()
        for letter in word_set:
            if letter not in pieces:
                return False, []
            else:
                pieces.remove(letter)
        return True, word_set  # this is so we don't have to calculate word set twice

    def place_letter(self, letter, position):
        self.temp_state[position[1]][position[0]] = letter

    def place_word(self, word, position, orientation):  # orientation is "h" or "v", position is a tuple of coordinates
        for letter in word:
            self.place_letter(letter, position)
            if orientation == "h":
                position[0] += 1
            else:
                position[1] += 1

    def place_if_possible(self, word, position, orientation, player):
        if not self.is_valid(word):
            return
        placeable, word_set = self.is_placeable(word, position, orientation, player)
        if not placeable:
            return
        self.place_word(word, position, orientation)
        for letter in word_set:
            player.pieces.remove(letter)

    def calculate_score(self):
        word_multiplier = 1
        for i in range(len(self.state)):
            for j in range(len(self.state[:])):
                if self.state != self.temp_state:
                    # if it's different, it's new, so calculate score, multipliers etc

    def move(self, word, position, orientation, player):
        self.place_if_possible(word, position, orientation, player)
        player.points += self.calculate_score()


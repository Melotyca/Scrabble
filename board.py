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
        is_attached = False # we haven't done this yet
        for letter in word:
            word_set.append(letter)
        for letter in word:
            square = self.temp_state[position[1]][position[0]]
            if square == letter:
                word_set.remove(letter)
                is_attached = True
            elif square != "":
                print("Square isn't empty or equal")
                return False, []
            if orientation == "h":
                position[0] += 1
            else:
                position[1] += 1
        pieces = player.pieces.copy()
        for letter in word_set:
            if letter not in pieces:
                print("Player doesn't have the pieces >:(")
                return False, []
            else:
                pieces.remove(letter)
        # Check for destroying pre-existing words
        if orientation == "h":
            position[0] -= len(word)
        else:
            position[1] -= len(word)
        self.place_word(word, position[:], orientation)
        temp_position = position[:]
        temp_word = ""
        while self.temp_state[temp_position[1]][temp_position[0]] != "":
            temp_word = self.temp_state[temp_position[1]][temp_position[0]] + temp_word
            if orientation == "h":
                temp_position[0] -= 1
            else:
                temp_position[1] -= 1
            if temp_position[0] == -1 or temp_position[1] == -1:
                break
        temp_position = position[:]
        while self.temp_state[temp_position[1]][temp_position[0]] != "":
            if orientation == "h":
                temp_position[0] += 1
            else:
                temp_position[1] += 1
            if temp_position[0] == len(self.state) or temp_position[1] == len(self.state):
                break
            temp_word = temp_word + self.temp_state[temp_position[1]][temp_position[0]]
        if temp_word not in self.dictionary:
            print("Word in direction of word isn't a word")
            print("Word detected:" + temp_word)
            return False, []
        if temp_word != word:
            is_attached = True
        for i in range(len(word)):
            temp_word = ""
            temp_position = position[:]
            if orientation == "h":
                temp_position[0] += i
            else:
                temp_position[1] += i
            while self.temp_state[temp_position[1]][temp_position[0]] != "":
                temp_word = self.temp_state[temp_position[1]][temp_position[0]] + temp_word
                if orientation == "v":
                    temp_position[0] -= 1
                else:
                    temp_position[1] -= 1
                if temp_position[0] == -1 or temp_position[1] == -1:
                    break
            temp_position = position[:]
            if orientation == "h":
                temp_position[0] += i
            else:
                temp_position[1] += i
            while self.temp_state[temp_position[1]][temp_position[0]] != "":
                if orientation == "v":
                    temp_position[0] += 1
                else:
                    temp_position[1] += 1
                if temp_position[0] == len(self.state) or temp_position[1] == len(self.state):
                    break
                temp_word = temp_word + self.temp_state[temp_position[1]][temp_position[0]]
            if temp_word not in self.dictionary and len(temp_word) != 1:
                print(f"word perpendicular to word isn't a word at index {i}")
                return False, []
            if len(temp_word) != 1:
                is_attached = True
        #if is_attached is False:
            #return False, []
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
        self.update_board()

    def calculate_score(self, bag):
        score = 0
        word_multiplier = 1
        for i in range(len(self.state)):
            for j in range(len(self.state[:])):
                if self.state[i][j] != self.temp_state[i][j]:
                    score += bag.values[self.temp_state[i][j]]
                    if self.multiplier[i][j] == "dw":
                        word_multiplier *= 2
                    elif self.multiplier[i][j] == "tw":
                        word_multiplier *= 3
                    elif self.multiplier[i][j] == "dl":
                        score += bag.values[self.temp_state[i][j]]
                    elif self.multiplier[i][j] == "dl":
                        score += bag.values[self.temp_state[i][j]] * 2
                    # if it's different, it's new, so calculate score, multipliers etc
        score *= word_multiplier
        return score

    def move(self, word, position, orientation, player, bag):
        self.temp_state = self.state.copy()
        self.place_if_possible(word.lower(), position, orientation, player)
        player.points += self.calculate_score(bag)
        bag.draw_to_seven(player)

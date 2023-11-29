import random


class Bag:
    def __init__(self):
        self.values = {"a":1, "b":3, "c":3, "d":2, "e":1, "f":4, "g":2, "h":4, "i":1, "j":8,
               "k":5, "l":1, "m":3, "n":1, "o":1, "p":3, "q":10, "r":1, "s":1, "t":1,
               "u":1, "v":4, "w":4, "x":8, "y":4, "z":10, " ":0}
        self.letters = ["a"] * 9 + ["b"] * 2 + ["c"] * 2 + ["d"] * 4 + ["e"] * 12 + ["f"] * 2 + ["g"] * 3 + ["h"] * 2 + ["i"] * 9 + ["j"] * 1 + ["k"] * 1 + ["l"] * 4 + ["m"] * 2 + ["n"] * 6 + ["o"] * 8 + ["p"] * 2 + ["q"] * 1 + ["r"] * 6 + ["s"] * 4 + ["t"] * 6 + ["u"] * 4 + ["v"] * 2 + ["w"] * 2 + ["x"] * 1 + ["y"] * 2 + ["z"] * 1 + [" "] * 2

    def draw(self):
        index = random.randint(0, len(self.letters)-1)
        return self.letters.pop(index)

    def draw_to_seven(self, player):
        while len(player.pieces) < 7:
            if len(self.letters) == 0:
                return
            player.pieces.append(self.draw())

    def exchange(self, player, exchanges):
        for letter in exchanges:
            player.pieces.remove(letter)
            self.letters.append(letter)
            player.pieces.append(self.draw())


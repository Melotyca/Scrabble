import numpy as np
from board import Board
from player import Player
from bag import Bag
import random


def draw_to_seven(player, bag):
    while len(player.pieces) < 7:
        if len(bag) == 0:
            return
        index = random.randint(0, len(bag)-1)
        player.pieces.append(bag.pop(index))


def play():
    board = Board()
    bag = Bag()
    players = []
    for i in range(2):
        new_player = Player(input(f"Hello Player {i+1}, what's your name? "))
        bag.draw_to_seven(new_player)
        players.append(new_player)
    current_player_index = 0
    board.place_word("hello", [1, 1], "h")
    players[0].pieces = ["r", "o", "a", "d", "t", "a", "d"]
    board.move("ROAD", [2, 3], "h", players[0], bag)
    print(board.state)
    print(players[0].pieces)
    board.move("TOAD", [3, 2], "v", players[0], bag)
    print(board.state)
    print(players[0].pieces)
    while True:


        current_player_index += 1
        if current_player_index == len(players):
            current_player_index = 0

























if __name__ == "__main__":
    play()

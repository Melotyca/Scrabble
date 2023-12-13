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
    # board.place_word("hello", [1, 1], "h")
    # players[0].pieces = ["r", "o", "a", "d", "t", "a", "d"]
    # board.move("ROAD", [2, 3], "h", players[0], bag)
    # print(board.state)
    # print(players[0].pieces)
    # board.move("TOAD", [3, 2], "v", players[0], bag)
    # print(board.state)
    # print(players[0].pieces)

    while True:
        current_player_index += 1
        if current_player_index == len(players):
            current_player_index = 0
        print(board.state)
        print(players[current_player_index].pieces)
        done = False
        while not done:
            choice = input(f"{players[current_player_index].name}, Do you want to replace pieces from your hand[r] or place words[p]?")
            if choice.lower() == "r":
                to_be_exchanged = input("Please type the letters you wish to replace.")
                bag.exchange(players[current_player_index], to_be_exchanged)
                print(players[current_player_index].pieces)
                done = True
            elif choice.lower() == "p":
                complete = False
                while not complete:
                    word = input("What word do you want to create?")
                    position = input("Where do you want the word to start?")
                    position = position.split()
                    position[0] = int(position[0])-1
                    position[1] = int(position[1])-1
                    orientation = input("Should the word be horizontal[h] or vertical[v]?")
                    board.move(word.lower(), position, orientation.lower(), players[current_player_index], bag)
                    print(board.state)
                    print(players[current_player_index].pieces)
                    leave = input("Are you done placing?[Y/N]")
                    if leave.lower() == "y":
                        complete = True
                done = True
            else:
                print("Invalid command, please try again.")
        bag.draw_to_seven(players[current_player_index])
























if __name__ == "__main__":
    play()

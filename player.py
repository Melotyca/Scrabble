class Player:
    def __init__(self, name=""):
        self.name = name
        self.points = 0
        self.pieces = []
        print(id(self))

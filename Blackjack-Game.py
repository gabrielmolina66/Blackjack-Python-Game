# creating 52-card deck
ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
deck = []
for i in range(4):
    deck += ranks

class Player:
    def __init__(self):
        self.current_points = 1000

    def stand(self):
        pass

    def hit(self):
        pass

    def split(self):
        pass

    def double(self):
        pass

class Dealer(Player):
    def __init__(self):
        pass


dealer = Dealer()
play_1 = Player()

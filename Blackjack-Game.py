import random
import sys

# creating 52-card deck
ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
deck = []
for i in range(4):
    deck += ranks

class Player:
    def __init__(self):
        self.current_points = 1000
        self.current_hand = []

    def stand(self):
        pass

    def hit(self):
        new_card = random.choice(deck)
        deck.remove(new_card)
        self.current_hand.append(new_card)

    def split(self):
        pass

    def double(self):
        pass

class Dealer(Player):
    def __init__(self):
        self.current_hand = []

current_round = 0



def deal():
    player.hit()
    dealer.hit()
    player.hit()
    dealer.hit()
    print("You were dealt a {first} and a {second}.".format(first=player.current_hand[0], second=player.current_hand[1]))
    print("The dealer shows a {first}.".format(first=dealer.current_hand[0]))

def get_choices():
    global choices
    choices = ["Hit", "Stand", "Double"]
    if (type(player.current_hand[0]) == str) and (type(player.current_hand[1]) == str):
        choices.append("Split")
    

def new_round():
    global current_round
    current_round += 1
    print()
    current_bet = input("Type \"Leave\", or place your bet for round {num}: ".format(num=current_round))
    if current_bet == "leave" or current_bet == "Leave":
        print()
        print("You finished with {num} points!".format(
            num=player.current_points))
        sys.exit()
    elif int(current_bet) > player.current_points:
        print()
        print("You can't bet more than you have! (It's for your own good.)")
        ##### Find a way to return to input here
    print()
    deal()
    get_choices()
    print()
    print("You can: " + str(choices))
    print()
    player_move = input("What's your move? ")
    


dealer = Dealer()
player = Player()





# Start game
def play_game():
    # Intro text
    print()
    print("Welcome to the Blackjack table! You will start with {num} points.".format(num=player.current_points))

    new_round()
    print()
    print("Your current points balance is: {pts}".format(pts=player.current_points))
    new_round()


play_game()
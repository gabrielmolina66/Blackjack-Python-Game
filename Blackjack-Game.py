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
        global current_bet
        current_bet *= 2

class Dealer(Player):
    def __init__(self):
        self.current_hand = []

current_round = 0

##### figure how to get an accurate sum
sum_of_hand = 22


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
    
def make_move(input):
    global choices
    global current_bet
    if input.title() not in choices:
        print("You're not allowed to choose that with your current hand.")
    if input.lower() == "hit":
        print()
        player.hit()
        print("You were dealt a {new}. Your current hand is ".format(new=player.current_hand[-1]) + str(player.current_hand))
        if sum_of_hand > 21:
            print("Bust!")
            player.current_points -= current_bet
            print()
            print("Since you're curious, the dealer's full hand was " + str(dealer.current_hand))
            return
    elif input.lower() == "stand":
        return
    elif input.lower() == "double":
        player.double()
        player.hit()
        print()
        print("You doubled your bet to {bet} and were dealt a {new}. Your current hand is ".format(bet=current_bet, new=player.current_hand[-1]) + str(player.current_hand))


def new_round():
    global choices
    global current_round
    current_round += 1
    print()
    global current_bet
    current_bet = input("Type \"Leave\", or place your bet for round {num}: ".format(num=current_round))
    if current_bet.lower() == "leave":
        print()
        print("You finished with {num} points!".format(
            num=player.current_points))
        sys.exit()
    elif int(current_bet) > player.current_points:
        print()
        print("You can't bet more than you have! (It's for your own good.)")
        ##### Find a way to return to input here
    else:
        current_bet = int(current_bet)
    print()
    deal()
    get_choices()
    print()
    print("You can: " + str(choices))
    print()
    global player_move
    player_move = input("What's your move? ")
    make_move(player_move)
    if sum_of_hand < 21:
        get_choices()
        print()
        print("You can: " + str(choices))
        print()
        player_move = input("What's your move? ")
        make_move(player_move)




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
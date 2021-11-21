import random
import sys

# creating 52-card deck
ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
full_deck = []
for i in range(4):
    full_deck += ranks
global deck
deck = full_deck

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
    
    def get_sum_of_hand(self, current_hand):
        hand_values = []
        aces = 0
        for card in current_hand:
            if card == 'J' or card == 'Q' or card == 'K':
                hand_values.append(10)
            elif card == 'A':
                aces += 1
            else:
                hand_values.append(card)
        while aces > 0:
            if sum(hand_values) <= 10:
                hand_values.append(11)
                aces -= 1
            else:
                hand_values.append(1)
                aces -= 1
        # global sum_of_hand
        self.sum_of_hand = sum(hand_values)
        return self.sum_of_hand

class Dealer(Player):
    def __init__(self):
        self.current_hand = []

current_round = 0
global face_cards
face_cards = ['K', 'Q', 'J', 10]
global result
result = ''

def deal():
    player.hit()
    dealer.hit()
    player.hit()
    dealer.hit()
    print("You were dealt a {first} and a {second}".format(first=player.current_hand[0], second=player.current_hand[1]) + ", totalling to " + str(player.get_sum_of_hand(player.current_hand)) + ".")
    print("The dealer shows a {first}.".format(first=dealer.current_hand[0]))

def get_choices():
    global choices
    choices = ["Stand", "Hit"]
    if (len(player.current_hand) == 2) and ((all(card in face_cards for card in player.current_hand)) or (player.current_hand[0] == player.current_hand[1])):
        choices.append("Split")
    if (player.current_points >= (2*int(current_bet))) and (len(player.current_hand) == 2):
        choices.append("Double")
    else:
        choices = ["Stand", "Hit"]
    
def make_move(user_input):
    global choices
    global current_bet
    # global sum_of_hand
    if user_input.title() not in choices:
        print()
        if user_input.title() == "Double":
            print("You don't have enough points to double your bet.")
            print ()
            print("----------------------------------------")
            another_move()
            return
        else:
            print("You're not allowed to choose that with your current hand.")
            print()
            print("----------------------------------------")
            another_move()
            return
    # player choices
    if user_input.lower() == "hit":
        print()
        player.hit()
        print("You were dealt a {new}. Your current hand is ".format(bet=current_bet, new=player.current_hand[-1]) + str(player.current_hand) + ", totalling to " + str(player.get_sum_of_hand(player.current_hand)) + ".")
        player.get_sum_of_hand(player.current_hand)
        if player.sum_of_hand > 21:
            print()
            print("Bust!")
            player.current_points -= current_bet
            print()
            print("The dealer's hand was " + str(dealer.get_sum_of_hand(dealer.current_hand)) + ", totalling to " + str(dealer.get_sum_of_hand(dealer.current_hand)) + ".")
            return
        else:
            another_move()
    elif user_input.lower() == "stand":
        player.get_sum_of_hand(player.current_hand)
        dealer_play()
        compare_to_dealer()
        return
    elif user_input.lower() == "double":
        player.double()
        player.hit()
        print()
        print("You doubled your bet to {bet} and were dealt a {new}.".format(bet=current_bet, new=player.current_hand[-1]))
        print("Your current hand is " + str(player.current_hand) + ", totalling to " + str(player.get_sum_of_hand(player.current_hand)) + ".")
        # reused code from above :(
        if player.sum_of_hand > 21:
            print()
            print("Bust!")
            player.current_points -= current_bet
            print()
            print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.get_sum_of_hand(dealer.current_hand)) + ".")
            return
        else:
            dealer_play()
            compare_to_dealer()
            return

def another_move():
    global player_move
    get_choices()
    print()
    print("You can: " + str(choices))
    print()
    player_move = input("What's your move? ")
    print()
    print("----------------------------------------")
    make_move(player_move)
    return


def dealer_play():
    dealer_sum = dealer.get_sum_of_hand(dealer.current_hand)
    if dealer_sum < 17:
        dealer.hit()
        dealer_play()
    elif dealer_sum >= 17 and dealer_sum <= 21:
        dealer.stand()
        dealer.get_sum_of_hand(dealer.current_hand)
    elif dealer_sum > 21:
        print()
        print("The dealer busted with a hand totalling to " + str(dealer_sum) + "! You win this round!")
        player.current_points += current_bet

def compare_to_dealer():
    if dealer.sum_of_hand <= 21:
        print()
        print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.sum_of_hand) + ".")
        print()
        if dealer.sum_of_hand > player.sum_of_hand:
            print("You lose this round!")
            player.current_points -= current_bet
        elif dealer.sum_of_hand < player.sum_of_hand:
            print("You win this round!")
            player.current_points += current_bet
        elif dealer.sum_of_hand == player.sum_of_hand:
            print("It's a push, no points are exchanged.")
    else:
        return


def leave():
    print()
    print("You finished with {num} points.".format(num=player.current_points))
    print()
    sys.exit()

def new_round():
    global choices
    global current_round
    global deck
    #global sum_of_hand
    player.current_hand = []
    dealer.current_hand = []
    deck = full_deck
    current_round += 1
    print()
    if player.current_points == 0:
        print("----------------------------------------")
        print()
        print("You have nothing left to bet!")
        leave()
    print("----------------------------------------")
    print()
    print("Your current points balance is: {pts}".format(pts=player.current_points))
    print()
    global current_bet
    current_bet = input("Type \"Leave\", or place your bet for round {num}: ".format(num=current_round))
    print()
    print("----------------------------------------")
    if current_bet.lower() == "leave":
        leave()
    try:
        current_bet = int(current_bet)
    except ValueError:
        print()
        print("Not a valid bet.")
        current_round -= 1
        new_round()
        return
    if current_bet > player.current_points:
        print()
        print("You can't bet more than you have! (It's for your own good.)")
        current_round -= 1
        new_round()
        return
    elif current_bet == 0:
        print()
        print("You can't bet zero.")
        current_round -= 1
        new_round()
        return
    print()
    deal()
    another_move()


dealer = Dealer()
player = Player()

# Start game
def play_game():
    # Intro text
    print()
    print("Welcome to the Blackjack table! You will start with {num} points.".format(num=player.current_points))
    print("The default length of the game is 10 rounds, but you can leave at any time between rounds.")
    for i in range(5):
        new_round()
    leave()


# Space to test stuff:


play_game()
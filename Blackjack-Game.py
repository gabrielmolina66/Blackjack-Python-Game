import random
import sys
import math

# creating 52-card deck
ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
full_deck = []
for i in range(4):
    full_deck += ranks
global deck

class Player:
    def __init__(self):
        self.current_points = 1000
        self.current_hand = []

    def stand(self):
        pass

    def hit(self, hand):
        new_card = random.choice(deck)
        deck.remove(new_card)
        hand.append(new_card)

    def split(self, hand):
        global split_phase
        # if 0, neither hand is active. if 1, first hand is being played. if 2, second hand is being played.
        split_phase = 0
        self.hit(hand)
        self.hit(hand)
        self.hand1 = [self.current_hand[0], self.current_hand[2]]
        self.hand2 = [self.current_hand[1], self.current_hand[3]]

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
global split_phase
split_phase = None
global bust_count
bust_count = 0

def deal(player_hand, dealer_hand):
    player.hit(player_hand)
    dealer.hit(dealer_hand)
    player.hit(player_hand)
    dealer.hit(dealer_hand)

    # manual hand to test split
    # player.current_hand = [10, 'K']
    
    print("You were dealt a {first} and a {second}".format(first=player.current_hand[0], second=player.current_hand[1]) + ", totalling to " + str(player.get_sum_of_hand(player.current_hand)) + ".")
    print("The dealer shows a {first}.".format(first=dealer.current_hand[0]))

def get_choices(hand):
    global choices
    choices = ["Stand", "Hit"]
    if (len(hand) == 2) and ((all(card in face_cards for card in hand)) or (hand[0] == hand[1])) and split_phase == None and current_bet <= (player.current_points / 2):
        choices.append("Split")
    # currently no double allowed after split
    if (player.current_points >= (2*int(current_bet))) and (len(hand) == 2) and split_phase == None:
        choices.append("Double")
    
def make_move(user_input, hand):
    global choices
    global current_bet
    global split_phase
    global bust_count
    global doubled
    # global sum_of_hand
    if user_input.title() not in choices:
        print()
        if ((user_input.title() == "Double") or (user_input.title() == "Split" and current_bet > (player.current_points / 2))) and len(hand) == 2:
            print("You don't have enough points to do that.")
            print ()
            print("----------------------------------------")
            another_move(hand)
            return
        else:
            print("You're not allowed to choose that with your current hand.")
            print()
            print("----------------------------------------")
            another_move(hand)
            return
    # player choices
    if user_input.lower() == "hit":
        print()
        player.hit(hand)
        print("You were dealt a {new}. Your current hand is ".format(new=hand[-1]) + str(hand) + ", totalling to " + str(player.get_sum_of_hand(hand)) + ".")
        player.get_sum_of_hand(hand)
        if player.sum_of_hand > 21:
            # if playing first hand of a split
            if split_phase == 1:
                print()
                print("Bust!")
                bust_count += 1
                # player.current_points -= math.floor(current_bet / 2)
                print()
                return
            # if playing second hand of a split
            if split_phase == 2:
                print()
                print("Bust!")
                bust_count += 1
                print()
                dealer_play(dealer.current_hand)
                compare_to_dealer()
                return
            bust()
            bust_count += 1
        else:
            another_move(hand)
    elif user_input.lower() == "stand":
        player.get_sum_of_hand(hand)
        if split_phase == 1:
            return
        if split_phase == 2:
            dealer_play(dealer.current_hand)
            compare_to_dealer()
            return
        dealer_play(dealer.current_hand)
        compare_to_dealer()
        return
    elif user_input.lower() == "double":
        player.double()
        player.hit(hand)
        print()
        print("You doubled your bet and were dealt a {new}.".format(new=hand[-1]))
        print()
        print("Your current hand is " + str(hand) + ", totalling to " + str(player.get_sum_of_hand(hand)) + ".")
        if player.sum_of_hand > 21:
            if split_phase == 1:
                print()
                print("Bust!")
                print()
                bust_count += 1
                doubled[0] = True
                return
            bust()
        else:
            dealer_play(dealer.current_hand)
            compare_to_dealer()
            return
    elif user_input.lower() == "split":
        current_bet *= 2
        player.split(hand)
        print()
        print("Your first hand is {first} and your second hand is {second},".format(first=str(player.hand1), second=player.hand2))
        print("each totalling to {first_sum} and {second_sum}, respectively.".format(first_sum=player.get_sum_of_hand(player.hand1), second_sum=player.get_sum_of_hand(player.hand2)))
        print()
        split_phase = 1
        print("For your first hand, " + str(player.hand1) + ":")
        another_move(player.hand1)
        print()
        split_phase = 2
        print("For your second hand, " + str(player.hand2) + ":")
        another_move(player.hand2)
        return

def bust():
    print()
    print("Bust!")
    player.current_points -= current_bet
    print()
    print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.get_sum_of_hand(dealer.current_hand)) + ".")
    return
        

def another_move(hand):
    global player_move
    get_choices(hand)
    print()
    print("You can: " + str(choices))
    print()
    player_move = input("What's your move? ")
    print()
    print("----------------------------------------")
    make_move(player_move, hand)
    return


def dealer_play(hand):
    global dealer_bust
    dealer_sum = dealer.get_sum_of_hand(dealer.current_hand)
    if dealer_sum < 17:
        dealer.hit(hand)
        dealer_play(hand)
    elif dealer_sum >= 17 and dealer_sum <= 21:
        dealer.stand()
        # dealer.get_sum_of_hand(dealer.current_hand)
    elif dealer_sum > 21:
        dealer_bust = True
        # player.current_points += current_bet

def compare_to_dealer():
    dealer.sum_of_hand = dealer.get_sum_of_hand(dealer.current_hand)
    player_sum_1 = player.get_sum_of_hand(player.hand1)
    player_sum_2 = player.get_sum_of_hand(player.hand2)
    player_sum_single_hand = player.get_sum_of_hand(player.current_hand)
    # print()
    # print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.sum_of_hand) + ".")
    # print()
    if split_phase == None:
        if bust_count == 0:
            print()
            print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.sum_of_hand) + ".")
            print()
            if dealer_bust == True:
                print("The dealer busts!")
                print()
                print("You win this round!")
                player.current_points += current_bet
            elif player_sum_single_hand > dealer.sum_of_hand:
                print("You win this round!")
                player.current_points += current_bet
            elif player_sum_single_hand < dealer.sum_of_hand:
                print("You lose this round.")
                player.current_points -= current_bet
            else:
                print("It's a push, no points are exchanged.")
        else:
            return # single-hand bust is taken care of in the bust() function
    else:
        if bust_count == 0:
            print()
            print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.sum_of_hand) + ".")
            print()
            if dealer_bust == True:
                print("The dealer busts!")
                print()
                print("You win this round!")
                player.current_points += current_bet
            elif player_sum_1 > dealer.sum_of_hand and player_sum_2 > dealer.sum_of_hand:
                print("You win both hands!")
                player.current_points += current_bet
            elif player_sum_1 < dealer.sum_of_hand and player_sum_2 < dealer.sum_of_hand:
                print("You lose both hands.")
                player.current_points -= current_bet
            elif player_sum_1 > dealer.sum_of_hand and player_sum_2 < dealer.sum_of_hand:
                print("You won your first hand but lost your second.")
                print()
                print("No points are exchanged.")
            elif player_sum_1 < dealer.sum_of_hand and player_sum_2 > dealer.sum_of_hand:
                print("You lost your first hand but won your second.")
                print()
                print("No points are exchanged.")
        elif bust_count == 1:
            print()
            print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.sum_of_hand) + ".")
            print()
            if (player_sum_1 < dealer.sum_of_hand or player_sum_2 < dealer.sum_of_hand) and dealer_bust == False:
                print("You lose both hands.")
                player.current_points -= current_bet
            elif player_sum_1 <= 21 and dealer_bust == True:
                print("The dealer busts!")
                print()
                print("You won your first hand but lost your second.")
                print()
                print("No points are exchanged.")
            elif player_sum_2 <= 21 and dealer_bust == True:
                print("The dealer busts!")
                print()
                print("You lost your first hand but won your second.")
                print()
                print("No points are exchanged.")
            elif player_sum_1 == dealer.sum_of_hand and dealer_bust == False:
                print("Your first hand resulted in a push and you lost your second hand.")
                player.current_points -= (current_bet / 2)
            elif player_sum_2 == dealer.sum_of_hand and dealer_bust == False:
                print("You lost your first hand and your second resulted in a push.")
                player.current_points -= (current_bet / 2)
            elif player_sum_1 > dealer.sum_of_hand and dealer_bust == False:
                if player_sum_1 > 21:
                    print("You lost your first hand but won your second.")
                    print()
                    print("No points are exchanged.")
                    return
                print("You won your first hand but lost your second.")
                print()
                print("No points are exchanged.")
            elif player_sum_2 > dealer.sum_of_hand and dealer_bust == False:
                if player_sum_2 > 21:
                    print("You won your first hand but lost your second.")
                    print()
                    print("No points are exchanged.")
                    return
                print("You lost your first hand but won your second.")
                print()
                print("No points are exchanged.")
        elif bust_count == 2:
            print()
            print("You lose both hands.")
            print()
            print("The dealer's hand was: " + str(dealer.current_hand) + ", totalling to " + str(dealer.sum_of_hand) + ".")
            player.current_points -= current_bet


def leave():
    print()
    print("You finished with {num} points.".format(num=player.current_points))
    print()
    print("----------------------------------------")
    print()
    sys.exit()

def new_round():
    global choices
    global current_round
    global deck
    global dealer_bust
    global bust_count
    global split_phase
    global doubled
    # doubled shows which hand if any has been doubled. [0] refers to if the player has doubled their only hand. [1] and [2] refer to if the player has split their hand and if they've doubled either.
    doubled = [False, False, False]
    player.current_hand = []
    dealer.current_hand = []
    player.hand1 = []
    player.hand2 = []
    bust_count = 0
    dealer_bust = False
    split_phase = None
    deck = full_deck[:]
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
    elif current_bet < 0:
        print()
        print("You can't bet a negative number, I see what you're trying to do.")
        current_round -= 1
        new_round()
        return
    print()
    deal(player.current_hand, dealer.current_hand)
    if player.get_sum_of_hand(player.current_hand) == 21:
        if dealer.get_sum_of_hand(dealer.current_hand) != 21:
            print()
            print("You got blackjack!")
            print()
            print("You win 1.5 times your bet.")
            player.current_points += math.floor(current_bet * 1.5)
        if dealer.get_sum_of_hand(dealer.current_hand) == 21:
            print()
            print("You got blackjack, but so did the dealer!")
            print()
            print("No points are exchanged.")
    else:
        another_move(player.current_hand)


dealer = Dealer()
player = Player()


def play_game():
    # Intro text
    print()
    print("Welcome to the Blackjack table! You will start with {num} points.".format(num=player.current_points))
    print("The default length of the game is 10 rounds, but you can leave at any time between rounds.")
    # num of rounds
    for i in range(10):
        new_round()
    print()
    print("----------------------------------------")
    leave()


play_game()
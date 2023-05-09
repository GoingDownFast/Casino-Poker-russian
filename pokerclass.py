import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if(rank == 'J'):   self.val = 11
        elif(rank == 'Q'): self.val = 12
        elif(rank == 'K'): self.val = 13
        elif(rank == 'A'): self.val = 14
        else: self.val = int(rank)
        
class Hand:
    def __init__(self):
        self.cont = []
        self.pow = 0
        self.conf = "high card"

    def add_card(self, card):
        self.cont.append(card)

    def rep_hand(self):
        for card in self.cont:
            print(card.rank + card.suit, end = ", ")

    def switch_cards(self, ind, card):
        self.cont.pop(ind)
        self.add_card(card)
    
    def eval(self):
        rank_list = []
        suit_list = []
        value_list = []
        pairs = []
        colors = []
        for item in self.cont:
            rank_list.append(item.rank)
            suit_list.append(item.suit)
            value_list.append(item.val)
        for i in range(0,5):
            pairs += [rank_list.count(rank_list[i])]
            colors += [suit_list.count(suit_list[i])]
        value_list.sort()
        if max(pairs) > 1:
            pair_val = self.cont[pairs.index(max(pairs))].val
            for i in range(0, max(pairs)):
                value_list.remove(pair_val)
            if 4 in pairs:
                self.pow = 10*pow(10,5) + 4*pair_val*10 + value_list[0]
                self.conf = "4 of a kind"
            elif 3 in pairs:
                if 2 in pairs:
                    self.pow = 9*pow(10,5) + 3*pair_val*100 + 2*value_list[0]
                    self.conf = "Full house"
                else:
                    self.pow = 4*pow(10,5) + 3*pair_val*1000 + value_list[1]*100 + value_list[0]
                    self.conf = "3 of a kind"
            elif 2 in pairs:
                if pairs.count(2) == 4:
                    if pair_val > value_list[1]:
                        if value_list[1] == value_list[0]:
                            self.pow = 3*pow(10,5) + 2*pair_val*1000 + 2*value_list[1]*10 + value_list[2]
                        else:
                            self.pow = 3*pow(10,5) + 2*pair_val*1000 + 2*value_list[1]*10 + value_list[0]
                    else:
                        if value_list[1] == value_list[0]:
                            self.pow = 3*pow(10,5) + 2*value_list[1]*1000 + 2*pair_val*10 + value_list[2]
                        else:
                            self.pow = 3*pow(10,5) + 2*value_list[1]*1000 + 2*pair_val*10 + value_list[0]
                    self.conf = "Two pair"
                else:
                    self.pow = 2*pow(10,5) + 2*pair_val*1000 + value_list[2]*100 + value_list[1]*10 + value_list[0]
                    self.conf = "Pair"
        
        else:
            self.pow = 0
            for i in range(0, 5):
                self.pow += value_list[i]*pow(10, i)
            if 5 in colors:
                self.pow += 7*pow(10,5)
                self.conf = "Flush"

            cons = 0
            for i in range(0, len(value_list)-1):
                if value_list[i+1] - value_list[i] == 1: cons += 1
            if cons == 4:
                self.pow += 5*pow(10,5)
            elif value_list == [2, 3, 4, 5, 14]:
                self.pow = 5*pow(10,5)
            
            if self.pow in range(5*pow(10,5), 7*pow(10,5)): self.conf = "Straight"
            if self.pow >= 12*pow(10,5): self.conf = "Straight Flush"
        
def freshDeck():
    suits = ["\u2764", #heart
             "\u2666", #diamond
             "\u2663", #club
             "\u2660"] #spade
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = []
    deck +=[Card(i, j) for i in suits for j in ranks]
    random.shuffle(deck)
    return deck

def showHand(hand):
        hand.eval()
        hand.rep_hand()
        print(hand.conf)

def mockHand():
    while True:
        keep_hand = input("Continue with this hand? (y/n) ")
        if keep_hand == 'y':
            return False
        elif keep_hand == 'n':
            return True
        else:
            print("Invalid input")

def win(pow_list):
    winner = pow_list.index(max(pow_list))
    print("Winner: Hand nr " + str(winner + 1))
    if winner == 0:
        return True
    else:
        return False

def tie(pow_list):
    tie_list = []
    for i in range(0, pow_list.count(max(pow_list))):
        ind = pow_list.index(max(pow_list))
        tie_list.append(ind + 1)
        pow_list.pop(ind)
    print("Tie between hands: " + tie_list)
    if 0 in tie_list:
        return True
    else:
        return False

def game(deck, stack):

    if stack < 20:
        print("Game Over, not enough money left")
        exit(0)
    ind = 0
    bet = 10
#------------------- Hands dealing -------------------------
    hands = [Hand(), Hand(), Hand(), Hand()]
    for hand in hands:
        for i in range(ind, ind+5):
            hand.add_card(deck[i])
        ind += 5

    print("\n-------------New Hand------------------")
    print("Stack: " + str(stack) + " - ante(" + str(bet) + ")")
    stack -= bet

    showHand(hands[0])
    print("-----Oponnents-------")
    print("XXXXX, XXXXX, XXXXX")

    if mockHand():
        game(freshDeck(), stack)
    
    #------------------- Cards switching -------------------------
    while True:
        try:
            switch_list = [int(num) for num in input("Which cards to switch? Refer by index (1-5), seperate by space: ").split()]
            for num in switch_list:
                if num < 1 or num > 5:
                    raise ValueError
            break
        except ValueError:
            print("Invalid input")

    for k in sorted(switch_list, reverse=True):
        hands[0].switch_cards(k-1, deck[ind])
        ind += 1
    #---------------- Final hands evaluation ---------------------
    pow_list = []
    for hand in hands:
        showHand(hand)
        pow_list.append(hand.pow)
        
    if pow_list.count(max(pow_list)) > 1:
        winner = tie(pow_list)
    else:
        winner = win(pow_list)

    if(winner):
        stack += bet*4
    else:
        stack -= bet

    print("Stack = " + str(stack))
        
    game(freshDeck(), stack)

def main():

    deck = freshDeck()
    stack = 100
    game(deck, stack)

main()
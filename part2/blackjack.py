# codeskulptor http://www.codeskulptor.org/#user40_EbvqBoFwPh_2.py
#  Mini-project #6 - Blackjack

import simplegui
import random

BLACKJACK = 21

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = "Game on"
player_prompt = "Hit or Stand?"
score = 0
deck =  None
player_hand = None
dealer_hand = None


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if not (suit in SUITS) or not (rank in RANKS):
            raise ValueError("Invalid card : %s %s" % (suit, rank))
        self.suit = suit
        self.rank = rank
        self.loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(suit))

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_pos = [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]]
        canvas.draw_image(card_images, self.loc, CARD_SIZE, card_pos, CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.has_aces = False

    def __str__(self):
        if not self.cards:
            return "Empty Hand"
        else:
            return "Hand Contains : %s" % " ".join([str(c) for c in self.cards])

    def add_card(self, card):
        self.cards.append(card)
        self.has_aces = self.has_aces or card.rank == 'A'

    def get_value(self):
        value = sum([VALUES[c.rank] for c in self.cards])
        if self.has_aces and (value + 10) <= BLACKJACK:
            value += 10
        return value

    def is_busted(self):
        return self.get_value() > BLACKJACK

    def draw(self, canvas, pos, hide_first=False):
        s = int(hide_first)
        if s:
            card_pos = [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]]
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, card_pos, CARD_BACK_SIZE)

        for i in range(s, len(self.cards)):
            card_pos = pos[0] +  i *(CARD_SIZE[0] + 10), pos[1]
            self.cards[i].draw(canvas, card_pos)

        if not s:
            value_pos = card_pos[0] + CARD_SIZE[0], card_pos[1] + CARD_SIZE[1] // 2
            canvas.draw_text(str(self.get_value()), value_pos, 24, 'Black')


# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in SUITS for r in RANKS]
        self.reset()

    def is_empty(self):
        return self.index >= len(self.cards)

    def deal_card(self):
        if self.is_empty():
            raise ValueError('deck is empty')
        self.index += 1
        return self.cards[self.index-1]

    def reset(self):
        random.shuffle(self.cards)
        self.index = 0

    def __str__(self):
        if self.is_empty():
            return 'Deck is empty'
        return 'Deck Contains : %s' % " ".join(str(c) for c in self.cards[self.index:])

    def __len__(self):
        return 52 - self.index


def deal_to(hand):
    hand.add_card(deck.deal_card())

#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, player_hand, dealer_hand

    if in_play:
        score -= 1
        in_play = False
        deal()

    in_play = True
    deck =  Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range (2):
        deal_to(player_hand)
        deal_to(dealer_hand)

    outcome = "Game on"
    player_prompt = "Hit or Stand?"

def hit():
    global score, outcome, player_prompt, in_play
    if in_play:
        deal_to(player_hand)
        if player_hand.get_value() > BLACKJACK:
            outcome = "Plater Busted  U Lost"
            player_prompt = "New Deal?"
            in_play = False
            score -= 1

def stand():
    global outcome, in_play, score
    if player_hand.is_busted() or not in_play:
        return
    in_play = False
    while dealer_hand.get_value() < 17:
        deal_to(dealer_hand)

    if dealer_hand.is_busted():
        outcome = "Dealer Busted U Won"
        score += 1
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "Dealer Won"
        score -= 1
    else:
        outcome = "Player Won"
        score += 1

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global score
    # draw the board + score
    canvas.draw_text("BlackJack", (50, 50), 32, 'Black')
    canvas.draw_text("Score : %s" % score, (400, 50), 32, 'Black')

    # draw the dealer
    canvas.draw_text("Dealer", (50, 100), 24, 'Black')
    canvas.draw_text(outcome, (250, 100), 22, 'Black')
    dealer_hand.draw(canvas, (50, 130), in_play)

    # draw the player
    canvas.draw_text("Player", (50, 300), 24, 'Black')
    canvas.draw_text(player_prompt, (250, 300), 22, 'Black')
    player_hand.draw(canvas, (50, 330))


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
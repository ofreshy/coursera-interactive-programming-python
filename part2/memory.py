# codeskulptor http://www.codeskulptor.org/#user40_FeU3Un2bXXxKAqq.py
# implementation of card game - Memory
import simplegui
import random

FRAME_WIDTH = 800
FRAME_HEIGHT = 100

OFF = 0
FLIPPED = 1
MATCHED = 2

NUM_CARDS = 16
cards = []
flipped_cards = []
num_matched = 0
num_turns = 0

# helper function to initialize globals
def new_game():
    global cards, num_matched, num_turns, flipped_cards
    cards = [{"val" : "%s" % ((i % 8) + 1),
              "state" : OFF,
             }
             for i in range(NUM_CARDS)]
    random.shuffle(cards)
    flipped_cards = []
    num_turns = 0
    num_matched = 0


# define event handlers
def mouseclick(pos):
    global num_turns, num_matched, flipped_cards, label
    clicked_card = cards[pos[0] // 50]

    if clicked_card["state"] in (FLIPPED, MATCHED):
        return

    clicked_card["state"] = FLIPPED
    if len(flipped_cards) == 0:
        num_turns += 1
    if len(flipped_cards) == 1:
        # we already have one flipped card, so check for a match
        flipped_card = flipped_cards[0]
        if flipped_card["val"] == clicked_card["val"]:
            flipped_card["state"] = MATCHED
            clicked_card["state"] = MATCHED
            num_matched += 1
            print num_matched
    elif len(flipped_cards) == 2:
        # we got two cards flipped already
        # so unless they were matched, turn them off
        flipped_card_a, flipped_card_b = flipped_cards
        if flipped_card_a["state"] != MATCHED:
            flipped_card_a["state"] = OFF
            flipped_card_b["state"] = OFF
        flipped_cards = []
        num_turns += 1

    label.set_text('Turns = %s' % num_turns)
    flipped_cards.append(clicked_card)



# cards are logically 50x100 pixels in size
def draw(canvas):
    if num_matched == 8:
        if num_turns < 13:
            canvas.draw_text("KABOOM Broke Joes Record", (0, 100), 66, 'Green')
        elif num_turns == 13:
            canvas.draw_text("Well Done Matched Joes Record", (0, 100), 60, 'Green')
        elif num_turns < 20:
            canvas.draw_text("Not Bad Improve by %s" % (num_turns-13), (0, 90), 66, 'Green')
        else:
            canvas.draw_text("Give it up man" % num_turns, (0, 100), 66, 'Green')
        return

    for i, card in enumerate(cards):
        xs, xe = 50*i, 50*(i+1)
        if card["state"] in (FLIPPED, MATCHED):
            canvas.draw_polygon([(xs, 0), (xe, 0), (xe, FRAME_HEIGHT), (xs, FRAME_HEIGHT)], 12, 'Green', 'White')
            canvas.draw_text(card["val"], (xs+15, 65), 48, 'Green')
        else:
            canvas.draw_polygon([(xs, 0), (xe, 0), (xe, FRAME_HEIGHT), (xs, FRAME_HEIGHT)], 12, 'Green', 'Blue')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", FRAME_WIDTH, FRAME_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
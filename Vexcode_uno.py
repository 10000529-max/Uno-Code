#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_1 = Motor(Ports.PORT1, False)
motor_5 = Motor(Ports.PORT5, True)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
#   Project:      VEXcode Project
#   Author:       VEX
#   Created:
#   Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

# Create events
FWD = Event()
RT = Event()
LT = Event()

# Functions
def when_started():
    FWD.broadcast_and_wait()
    LT.broadcast_and_wait()
    FWD.broadcast_and_wait()
    RT.broadcast_and_wait()
    FWD.broadcast_and_wait()

def motor1_move_forward():
    motor_1.spin_for(FORWARD, 425, DEGREES)
def motor5_move_forward():
    motor_5.spin_for(FORWARD, 425, DEGREES)
def motor1_turn_right():
    motor_1.spin_for(FORWARD, 220, DEGREES)
def motor5_turn_right():
    motor_5.spin_for(REVERSE, 220, DEGREES)
def motor1_turn_left():
    motor_1.spin_for(REVERSE, 220, DEGREES)
def motor5_turn_left():
    motor_5.spin_for(FORWARD, 220, DEGREES)

# Register the callback functions to the events
FWD(motor1_move_forward)
FWD(motor5_move_forward)
RT(motor1_turn_right)
RT(motor5_turn_right)
LT(motor1_turn_left)
LT(motor5_turn_left)
wait(15, MSEC)

# ==========================================
# UNO DECK & HAND SYSTEM
# ==========================================

def build_uno_deck():
    colors = ["Red", "Yellow", "Green", "Blue"]
    action_cards = ["Skip", "Reverse", "+2"]
    deck = []
    
    for color in colors:
        # One '0' card per color
        deck.append(color + " 0")
        
        # Two of each number 1 through 9 per color
        for num in range(1, 10):
            deck.append(color + " " + str(num))
            deck.append(color + " " + str(num))
            
        # Two of each action card (+2, Skip, Reverse) per color
        for action in action_cards:
            deck.append(color + " " + action)
            deck.append(color + " " + action)
            
    # Four Wild and four +4 cards
    for _ in range(4):
        deck.append("Wild")
        deck.append("+4")
        
    return deck

def shuffle_deck(deck):
    # Fisher-Yates shuffle algorithm using VEX's urandom generator
    for i in range(len(deck) - 1, 0, -1):
        j = urandom.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def draw_card(deck):
    if len(deck) > 0:
        return deck.pop(0)
    return None

def deal_hand(deck, hand_size=7):
    hand = []
    for _ in range(hand_size):
        card = draw_card(deck)
        if card:
            hand.append(card)
    return hand

# NEW FUNCTION 1: Converts card names into compact labels to fit 16 columns
def abbreviate_card(card):
    if card == "Wild":
        return "WLD"
    if card == "+4":
        return "W+4"
    
    parts = card.split(" ")
    if len(parts) == 2:
        color_code = parts[0][0]  # Takes 'R', 'Y', 'G', or 'B'
        value = parts[1]
        if value == "Skip":
            value = "SK"
        elif value == "Reverse":
            value = "RV"
        return color_code + value
    return card[:4]

# NEW FUNCTION 2: Displays all 7 cards across a 2-column grid on 1 single screen
def render_compact_hand(hand, deck_count):
    brain.screen.clear_screen()
    
    # Row 1: Header summary line
    brain.screen.set_cursor(1, 1)
    brain.screen.print("HND:7 | DECK:" + str(deck_count))
    
    # Row 2: Cards 1 and 2
    c1 = "1:" + abbreviate_card(hand[0])
    c2 = "2:" + abbreviate_card(hand[1])
    brain.screen.set_cursor(2, 1)
    brain.screen.print((c1 + " " * (8 - len(c1)) + c2)[:16])
    
    # Row 3: Cards 3 and 4
    c3 = "3:" + abbreviate_card(hand[2])
    c4 = "4:" + abbreviate_card(hand[3])
    brain.screen.set_cursor(3, 1)
    brain.screen.print((c3 + " " * (8 - len(c3)) + c4)[:16])
    
    # Row 4: Cards 5 and 6
    c5 = "5:" + abbreviate_card(hand[4])
    c6 = "6:" + abbreviate_card(hand[5])
    brain.screen.set_cursor(4, 1)
    brain.screen.print((c5 + " " * (8 - len(c5)) + c6)[:16])
    
    # Row 5: Card 7
    c7 = "7:" + abbreviate_card(hand[6])
    brain.screen.set_cursor(5, 1)
    brain.screen.print(c7[:16])

def print_hand_to_console(hand, deck):
    print("=== STARTING HAND (7 Cards) ===")
    for position, card in enumerate(hand, start=1):
        print("Card " + str(position) + ": " + str(card))
    print("Cards remaining in deck: " + str(len(deck)))

# Generate initial deck, shuffle, and deal starting hand
uno_deck = build_uno_deck()
shuffle_deck(uno_deck)
player_hand = deal_hand(uno_deck, 7)

# Print full details to console and render all 7 cards on 1 screen
print_hand_to_console(player_hand, uno_deck)
render_compact_hand(player_hand, len(uno_deck))

# Main Execution Loop: Press physical Checkmark button to deal a new 7-card hand
while True:
    if brain.buttonCheck.pressing():
        uno_deck = build_uno_deck()
        shuffle_deck(uno_deck)
        player_hand = deal_hand(uno_deck, 7)
        
        print_hand_to_console(player_hand, uno_deck)
        render_compact_hand(player_hand, len(uno_deck))
        
        # Debounce button press
        while brain.buttonCheck.pressing():
            wait(20, MSEC)
            
    wait(20, MSEC)
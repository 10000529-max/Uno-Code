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

# Generating and setting random seed
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
#   Project:      VEXcode EXP UNO - Persistent Game Loop & Compact View
#   Author:       VEX
#   Description:  Compact hand console view & deck persistence across turns
# 
# ------------------------------------------

# Library imports
from vex import *

# Create events
FWD = Event()
RT = Event()
LT = Event()

# Motor callbacks
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

# Register callback functions
FWD(motor1_move_forward)
FWD(motor5_move_forward)
RT(motor1_turn_right)
RT(motor5_turn_right)
LT(motor1_turn_left)
LT(motor5_turn_left)
wait(15, MSEC)

# ==========================================
# PHASE 1: DECK & HAND CORE
# ==========================================

def build_uno_deck():
    colors = ["Red", "Yellow", "Green", "Blue"]
    action_cards = ["Skip", "Reverse", "+2"]
    deck = []
    
    for color in colors:
        deck.append(color + " 0")
        for num in range(1, 10):
            deck.append(color + " " + str(num))
            deck.append(color + " " + str(num))
        for action in action_cards:
            deck.append(color + " " + action)
            deck.append(color + " " + action)
            
    for _ in range(4):
        deck.append("Wild")
        deck.append("+4")
        
    return deck

def shuffle_deck(deck):
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

def abbreviate_card(card):
    if card == "Wild":
        return "WLD"
    if card == "+4":
        return "W+4"
    
    parts = card.split(" ")
    if len(parts) == 2:
        color_code = parts[0][0]
        value = parts[1]
        if value == "Skip":
            value = "SK"
        elif value == "Reverse":
            value = "RV"
        return color_code + value
    return card[:4]

# OPTION B: Compact One-Liner Console Display
def print_hand_to_console(hand, deck, current_top):
    print("\n--------------------------------------------------")
    print("TOP CARD: " + current_top + " | DECK REMAINING: " + str(len(deck)))
    formatted = " | ".join("[" + str(i + 1) + "] " + card for i, card in enumerate(hand))
    print("YOUR HAND (" + str(len(hand)) + "): " + formatted)
    print("--------------------------------------------------\n")

# ==========================================
# PHASE 2: MENU & TURN INTERACTION SYSTEM
# ==========================================

def select_menu_option(header_title, options):
    selected_index = 0
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print(header_title[:16])
        
        # Display current option on line 3
        brain.screen.set_cursor(3, 1)
        opt_text = "< " + options[selected_index] + " >"
        brain.screen.print(opt_text[:16])
        
        # Display control guide on line 5
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]Sel  [v]OK")
        
        while not (brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing()):
            wait(20, MSEC)
            
        if brain.buttonLeft.pressing():
            selected_index = (selected_index - 1) % len(options)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            selected_index = (selected_index + 1) % len(options)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return options[selected_index]

def display_hand_and_pause(hand, top_card, deck_count):
    brain.screen.clear_screen()
    
    # Row 1: Top card & remaining deck
    brain.screen.set_cursor(1, 1)
    hdr = "TOP:" + abbreviate_card(top_card) + "|DK:" + str(deck_count)
    brain.screen.print(hdr[:16])
    
    # Rows 2 to 4: Cards in hand
    slots = [[2, 1], [2, 9], [3, 1], [3, 9], [4, 1], [4, 9]]
    for idx in range(min(6, len(hand))):
        row = slots[idx][0]
        col = slots[idx][1]
        brain.screen.set_cursor(row, col)
        lbl = str(idx + 1) + ":" + abbreviate_card(hand[idx])
        brain.screen.print(lbl[:7])
        
    # Row 5: Navigation prompt
    brain.screen.set_cursor(5, 1)
    if len(hand) >= 7:
        brain.screen.print("7:" + abbreviate_card(hand[6]) + "  [v]Next")
    else:
        brain.screen.print("   [v]Next Turn")
        
    while not brain.buttonCheck.pressing():
        wait(20, MSEC)
    while brain.buttonCheck.pressing():
        wait(20, MSEC)

def input_discard_pile():
    categories = ["Red", "Yellow", "Green", "Blue", "Wild", "+4"]
    chosen_cat = select_menu_option("DISCARD COLOR:", categories)
    
    if chosen_cat == "Wild":
        chosen_color = select_menu_option("WILD COLOR:", ["Red", "Yellow", "Green", "Blue"])
        return chosen_color + " Wild"
    elif chosen_cat == "+4":
        chosen_color = select_menu_option("+4 COLOR:", ["Red", "Yellow", "Green", "Blue"])
        return chosen_color + " +4"
    else:
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]
        chosen_val = select_menu_option(chosen_cat + " VALUE:", values)
        return chosen_cat + " " + chosen_val

def process_player_turn(discard_card, hand, deck):
    # Check for initial forced draw cards on discard pile
    if "+2" in discard_card:
        drawn_1 = draw_card(deck)
        drawn_2 = draw_card(deck)
        if drawn_1: hand.append(drawn_1)
        if drawn_2: hand.append(drawn_2)
        select_menu_option("FORCED DRAW +2", ["Draw 2 Cards"])
        return discard_card
        
    elif "+4" in discard_card:
        for _ in range(4):
            drawn = draw_card(deck)
            if drawn:
                hand.append(drawn)
        select_menu_option("FORCED DRAW +4", ["Draw 4 Cards"])
        return discard_card
        
    else:
        action = select_menu_option("YOUR TURN:", ["Play Card", "Draw 1 Card"])
        
        if action == "Draw 1 Card":
            drawn = draw_card(deck)
            if drawn:
                hand.append(drawn)
                print(">>> YOU DREW: " + drawn)
                select_menu_option("YOU DREW:", [drawn])
            else:
                select_menu_option("DECK EMPTY!", ["No Cards Left"])
            return discard_card
            
        else:
            hand_options = []
            for idx, card in enumerate(hand):
                hand_options.append(str(idx + 1) + ":" + abbreviate_card(card))
                
            selected_str = select_menu_option("SELECT CARD:", hand_options)
            card_idx = int(selected_str.split(":")[0]) - 1
            played_card = hand.pop(card_idx)
            
            if "Wild" in played_card or "+4" in played_card:
                chosen_color = select_menu_option("CHOOSE COLOR:", ["Red", "Yellow", "Green", "Blue"])
                played_card = chosen_color + " " + played_card
                
            print(">>> YOU PLAYED: " + played_card)
            return played_card

# ==========================================
# MAIN GAME EXECUTION
# ==========================================

# 1. Initialize deck and deal starting hand ONCE per match
uno_deck = build_uno_deck()
shuffle_deck(uno_deck)
player_hand = deal_hand(uno_deck, 7)

print("==================================")
print("=== NEW UNO GAME STARTED ===")

# 2. Select initial top discard card
discard_top = input_discard_pile()

# 3. Continuous turn loop (hand persists across all turns)
while len(player_hand) > 0:
    print_hand_to_console(player_hand, uno_deck, discard_top)
    
    # Process single player turn
    discard_top = process_player_turn(discard_top, player_hand, uno_deck)
    
    # Display current hand on brain screen and pause until Checkmark is pressed
    display_hand_and_pause(player_hand, discard_top, len(uno_deck))

print("\nGAME OVER - Hand Empty!")
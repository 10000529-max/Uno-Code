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
#   Project:     VEXcode EXP UNO - Complete Game Loop (Version 2.3)
#   Author:      VEX
#   Description: Version 2.3 Updates:
#                - Removed unnecessary "START DISCARD" prompt
#                - Startup sequence fixed: Hand -> Incoming Attack Check -> Opponent Played Card
#                - Printed full shuffled deck & starting hand to console
#                - Enforces UNO forced draw (+2 / +4) turn-skip rule
#                - Phase 4 Effects: SoundType.SIREN2 + "UNO!" on second-to-last card
#                - Victory Celebration: SoundType.ALARM2 + "WINNER!" + victory_dance()
#                - Formatted strictly for 5-Row x 16-Column VEX EXP Screen
# 
# ------------------------------------------

# Library imports
from vex import *

# Create events for robot movement
FWD = Event()
RT = Event()
LT = Event()

# Motor callbacks for 90-degree turns and forward movement
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
# GRAPHICAL CARD DISPLAY FUNCTION
# ==========================================

def draw_card_full_screen(card_str, color_code):
    brain.screen.clear_screen()
    if color_code == 'R': brain.screen.set_fill_color(Color.RED)
    elif color_code == 'G': brain.screen.set_fill_color(Color.GREEN)
    elif color_code == 'B': brain.screen.set_fill_color(Color.BLUE)
    elif color_code == 'Y': brain.screen.set_fill_color(Color.YELLOW)
    else: brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    for i in range(5):
        brain.screen.draw_rectangle(0+i, 0+i, 159-(i*2), 107-(i*2))
   
    card = card_str[1:]
    if card == "0":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
    elif card == "8":
        for i in range(15):
            brain.screen.draw_rectangle(20+i, 20+i, 119-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(72+i, 20, 72+i, 85)
    elif card == "1":
        for i in range(15):
            brain.screen.draw_line(20, 47+i, 139, 47+i)
    elif card == "3":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
    elif card == "2":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "5":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "6":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
            brain.screen.draw_line(72, 73+i, 139, 73+i)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "9":
        for i in range(15):
            brain.screen.draw_line(20+i, 20, 20+i, 87)
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
            brain.screen.draw_line(125+i, 20, 125+i, 87)
        for i in range(3):
            brain.screen.draw_line(145+i, 20, 145+i, 87)
    elif card == "4" and "D" not in card_str:
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 72, 20+i)
            brain.screen.draw_line(20, 73+i, 72, 73+i)
            brain.screen.draw_line(72+i, 20, 72+i, 87)
            brain.screen.draw_line(72, 20+i, 139, 20+i)
    elif card == "7":
        for i in range(15):
            brain.screen.draw_line(20, 20+i, 139, 20+i)
            brain.screen.draw_line(20+i, 20, 20+i, 87)
    elif card == "Rv":
        for i in range(15):
            brain.screen.draw_line(62+i, 30, 62+i, 87)
            brain.screen.draw_line(69, 20, 52+i, 40)
            brain.screen.draw_line(69, 20, 82-i, 40)
            brain.screen.draw_line(82+i, 20, 82+i, 77)
            brain.screen.draw_line(89, 87, 74+i, 67)
            brain.screen.draw_line(89, 87, 104-i, 67)
    elif card == "S":
        for i in range(15):
            brain.screen.draw_rectangle(40+i, 20+i, 82-(i*2), 67-(i*2))
        for i in range(15):
            brain.screen.draw_line(52+i, 20, 92+i, 80)
    elif card == "D2":
        brain.screen.set_fill_color(Color.WHITE)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+(i/2), 30)
        if color_code == 'R': brain.screen.set_fill_color(Color.RED)
        elif color_code == 'G': brain.screen.set_fill_color(Color.GREEN)
        elif color_code == 'B': brain.screen.set_fill_color(Color.BLUE)
        elif color_code == 'Y': brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(47, 32, 40, 25)
        brain.screen.draw_rectangle(73, 52, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10+i, 66, 10+i, 79)
            brain.screen.draw_line(10, 66+i, 20, 66+i)
            brain.screen.draw_line(18+i, 66, 18+i, 79)
            brain.screen.draw_line(20, 75+i, 30, 75+i)
            brain.screen.draw_line(26+i, 66, 26+i, 79)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10-i, 107-66, 159-10-i, 107-79)
            brain.screen.draw_line(159-10, 107-66-i, 159-20, 107-66-i)
            brain.screen.draw_line(159-18-i, 107-66, 159-18-i, 107-79)
            brain.screen.draw_line(159-20, 107-75-i, 159-30, 107-75-i)
            brain.screen.draw_line(159-26-i, 107-66, 159-26-i, 107-79)
    elif card_str == "W":
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(50, 20, 30, 32)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(50, 52, 30, 32)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(80, 20, 30, 32)
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(80, 52, 30, 32)
        brain.screen.set_fill_color(Color.TRANSPARENT)
        brain.screen.set_pen_width(3)
        for i in range(15):
            brain.screen.draw_circle(80, 52, 30-(i/5))
        brain.screen.set_pen_color(Color.BLACK)
        for i in range(65):
            brain.screen.draw_circle(80, 52, 31+(i/5))
        brain.screen.set_pen_width(1)
    elif card_str == "D4":
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(78, 42, 40, 25)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(60, 28, 40, 25)
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(42, 42, 40, 25)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(60, 56, 40, 25)
        for i in range(5):
            brain.screen.draw_line(18+i, 85, 18+i, 95)
            brain.screen.draw_line(14, 88+i, 26, 88+i)
            brain.screen.draw_line(10, 75+i, 20, 75+i)
            brain.screen.draw_line(16+i, 75, 16+i, 66)
            brain.screen.draw_line(10, 66+i, 30, 66+i)

            brain.screen.draw_line(159-18-i, 107-85, 159-18-i, 107-95)
            brain.screen.draw_line(159-14, 107-88-i, 159-26, 107-88-i)
            brain.screen.draw_line(159-10, 107-75-i, 159-20, 107-75-i)
            brain.screen.draw_line(159-16-i, 107-75, 159-16-i, 107-66)
            brain.screen.draw_line(159-10, 107-66-i, 159-30, 107-66-i)
    else:
        # UNO Card Back Display
        brain.screen.set_fill_color(Color.RED)
        brain.screen.set_pen_color(Color.RED)
        for i in range(40):
            brain.screen.draw_circle(60+i, 42+(i/2), 30)
        brain.screen.set_pen_color(Color.YELLOW)
        for i in range(5):
            brain.screen.draw_line(75, 50+i-5, 85, 50+i-5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i+5)
            brain.screen.draw_line(75, 50+i+5, 85, 50+i-5)

            brain.screen.draw_line(75, 50+i-15, 85, 50+i-15)
            brain.screen.draw_line(75+(i/2), 50-15, 75+(i/2), 50-25)
            brain.screen.draw_line(83+(i/2), 50-15, 83+(i/2), 50-25)
            brain.screen.draw_line(75, 50+i-25, 85, 50+i-25)

            brain.screen.draw_line(75, 50+i+15, 85, 50+i+15)
            brain.screen.draw_line(83+(i/2), 50+15, 83+(i/2), 50+25)
            brain.screen.draw_line(75, 50+i+25, 85, 50+i+25)

    # Always reset screen colors back to standard default
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)


def card_to_gfx_args(card_name):
    """
    Translates card text string into (card_str, color_code) tuple
    for draw_card_full_screen().
    """
    parts = card_name.split(" ")
    color_char = parts[0][0] if len(parts) > 1 and parts[0] in ["Red", "Green", "Blue", "Yellow"] else 'N'

    if "Wild" in card_name and "+4" not in card_name:
        return ("W", color_char)
    elif "+4" in card_name:
        return ("D4", color_char)
    
    val = parts[1] if len(parts) > 1 else ""

    if val == "Skip": val = "S"
    elif val == "Reverse": val = "Rv"
    elif val == "+2": val = "D2"

    return (color_char + val, color_char)


def flash_uno_card_back(count=1):
    """
    Flashes the UNO Card Back full-screen 'count' times when drawing cards.
    """
    for _ in range(count):
        draw_card_full_screen("BACK", "N")
        wait(600, MSEC)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        wait(200, MSEC)

# ==========================================
# PHASE 1: ROBOT MOVEMENT & DANCE FUNCTIONS
# ==========================================

def robot_drive_forward_2():
    """
    Drives forward 2 units to reach center table.
    """
    for _ in range(2):
        FWD.broadcast()
        wait(800, MSEC)


def robot_turn_90_right():
    """
    Executes 90-degree right turn using RT event broadcast.
    """
    RT.broadcast()
    wait(600, MSEC)


def robot_turn_180():
    """
    Executes 180-degree turn around (two 90-degree turns).
    """
    robot_turn_90_right()
    robot_turn_90_right()


def robot_deliver_card(msg="ROBOT DELIVERING"):
    """
    Hides hand, drives 2 units forward to deliver card face-up,
    spins 180 degrees, and returns to player.
    """
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    brain.screen.print(msg[:16])
    robot_drive_forward_2()
    robot_turn_180()
    robot_drive_forward_2()
    robot_turn_180()


def robot_fetch_card():
    """
    Hides hand, drives 2 units forward to draw pile at center,
    spins 180 degrees, and returns to deliver drawn card.
    """
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    brain.screen.print("ROBOT FETCHING"[:16])
    robot_drive_forward_2()
    robot_turn_180()
    robot_drive_forward_2()
    robot_turn_180()


def victory_dance():
    """
    VICTORY CELEBRATION FUNCTION: Plays SoundType.ALARM2, displays "WINNER!",
    and uses motion broadcasts (RT, LT, FWD) to perform a victory dance.
    """
    brain.play_sound(SoundType.ALARM2)
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("WINNER!"[:16])
    
    # Motion broadcasts victory dance sequence
    RT.broadcast()
    wait(400, MSEC)
    LT.broadcast()
    wait(400, MSEC)
    LT.broadcast()
    wait(400, MSEC)
    RT.broadcast()
    wait(400, MSEC)
    FWD.broadcast()
    wait(500, MSEC)

# ==========================================
# PHASE 2: DECK & HAND CORE
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

def print_hand_to_console(hand, deck, current_top):
    print("\n--------------------------------------------------")
    print("TOP CARD: " + str(current_top) + " | DECK REMAINING: " + str(len(deck)))
    formatted = " | ".join("[" + str(i + 1) + "] " + card for i, card in enumerate(hand))
    print("YOUR HAND (" + str(len(hand)) + "): " + formatted)
    print("--------------------------------------------------\n")

# ==========================================
# PHASE 3: GAME STATE & RULE FUNCTIONS
# ==========================================

def get_legal_moves(hand, top_card):
    """
    Returns list of hand indices for cards that are legal to play.
    """
    legal_indices = []
    top_parts = top_card.split(" ")
    top_color = top_parts[0] if len(top_parts) > 0 else ""
    top_val = top_parts[1] if len(top_parts) > 1 else top_parts[0]

    for idx, card in enumerate(hand):
        if "Wild" in card or "+4" in card:
            legal_indices.append(idx)
        else:
            card_parts = card.split(" ")
            card_color = card_parts[0] if len(card_parts) > 0 else ""
            card_val = card_parts[1] if len(card_parts) > 1 else card_parts[0]

            if card_color == top_color or card_val == top_val:
                legal_indices.append(idx)

    return legal_indices


def check_game_over(hand):
    """
    Checks if player's hand is empty.
    If empty, triggers victory_dance() and returns True to end game loop.
    """
    if len(hand) == 0:
        victory_dance()
        return True
    return False

# ==========================================
# PHASE 4: MENU & SCREEN INTERACTION SYSTEM
# ==========================================

def select_menu_option(header_title, options):
    """
    Standard menu renderer for 5-row x 16-col VEX EXP Screen.
    Controls: buttonLeft, buttonRight, buttonCheck.
    """
    selected_index = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        
        # Row 1: Header Title
        brain.screen.set_cursor(1, 1)
        brain.screen.print(header_title[:16])
        
        # Row 3: Current Selection Option
        brain.screen.set_cursor(3, 1)
        opt_text = "< " + str(options[selected_index]) + " >"
        brain.screen.print(opt_text[:16])
        
        # Row 5: Controls Prompt
        brain.screen.set_cursor(5, 1)
        brain.screen.print("[L/R]Sel  [v]OK"[:16])
        
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


def view_full_hand(hand, top_card):
    """
    Multi-page viewer for full hand using TC (Top Card) and HS (Hand Size).
    Press Check button to confirm/exit hand view.
    """
    page = 0
    while True:
        max_page = (len(hand) - 1) // 6 if len(hand) > 0 else 0
        if page > max_page:
            page = max_page

        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        
        # Row 1: Header displaying TC, HS, P
        brain.screen.set_cursor(1, 1)
        hdr = "TC:" + abbreviate_card(top_card) + " HS:" + str(len(hand)) + " P" + str(page + 1) + "/" + str(max_page + 1)
        brain.screen.print(hdr[:16])
        
        # Rows 2 to 4: Hand Grid (6 cards per page)
        slots = [[2, 1], [2, 9], [3, 1], [3, 9], [4, 1], [4, 9]]
        start_idx = page * 6
        end_idx = min(start_idx + 6, len(hand))
        
        if not hand:
            brain.screen.set_cursor(3, 1)
            brain.screen.print("(HAND IS EMPTY)"[:16])
        else:
            for i in range(start_idx, end_idx):
                slot = slots[i - start_idx]
                brain.screen.set_cursor(slot[0], slot[1])
                lbl = str(i + 1) + ":" + abbreviate_card(hand[i])
                brain.screen.print(lbl[:7])
                
        # Row 5: Page / Return prompt
        brain.screen.set_cursor(5, 1)
        if max_page > 0:
            brain.screen.print("[L/R]Pg [v]Done"[:16])
        else:
            brain.screen.print("   [v]Continue"[:16])
            
        while not (brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing()):
            wait(20, MSEC)
            
        if brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            break
        elif brain.buttonLeft.pressing() and max_page > 0:
            page = (page - 1) % (max_page + 1)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing() and max_page > 0:
            page = (page + 1) % (max_page + 1)
            while brain.buttonRight.pressing():
                wait(20, MSEC)


def input_discard_pile(prompt_label="OPPONENT PLAYED:"):
    """
    Function to record initial discard or opponent played card.
    Displays graphical card face-up after entry.
    """
    categories = ["Red", "Yellow", "Green", "Blue", "Wild", "+4"]
    chosen_cat = select_menu_option(prompt_label, categories)
    
    if chosen_cat == "Wild":
        chosen_color = select_menu_option("WILD COLOR:", ["Red", "Yellow", "Green", "Blue"])
        card_res = chosen_color + " Wild"
    elif chosen_cat == "+4":
        chosen_color = select_menu_option("+4 COLOR:", ["Red", "Yellow", "Green", "Blue"])
        card_res = chosen_color + " +4"
    else:
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]
        chosen_val = select_menu_option(chosen_cat + " VAL:", values)
        card_res = chosen_cat + " " + chosen_val

    # Render card graphically face-up
    gfx_args = card_to_gfx_args(card_res)
    draw_card_full_screen(gfx_args[0], gfx_args[1])
    wait(1200, MSEC)

    return card_res


def process_player_turn(discard_card, hand, deck):
    """
    Handles turn choices for 'My Turn'.
    - Detects second-to-last card play (1 card remaining): plays SoundType.SIREN2 & displays "UNO!".
    - Detects last card play (0 cards remaining): displays "WINNING CARD!" before victory celebration.
    """
    while True:
        turn_menu_title = "YOUR MOVE:"
        options = ["View Hand", "Play Card", "Draw 1 Card"]

        choice = select_menu_option(turn_menu_title, options)

        # 1. View Hand option
        if choice == "View Hand":
            view_full_hand(hand, discard_card)
            continue

        # 2. Draw 1 Card option
        elif choice == "Draw 1 Card":
            flash_uno_card_back(1)
            robot_fetch_card()
            drawn = draw_card(deck)
            if drawn:
                hand.append(drawn)
                print(">>> YOU DREW: " + drawn)
            else:
                select_menu_option("DECK EMPTY!", ["No Cards Left"])
            return discard_card

        # 3. Play Card option
        elif choice == "Play Card":
            legal_indices = get_legal_moves(hand, discard_card)

            if not legal_indices:
                select_menu_option("NO LEGAL MOVES!", ["Draw 1 Card"])
                flash_uno_card_back(1)
                robot_fetch_card()
                drawn = draw_card(deck)
                if drawn:
                    hand.append(drawn)
                    print(">>> NO PLAYABLE CARDS! YOU DREW: " + drawn)
                else:
                    select_menu_option("DECK EMPTY!", ["No Cards Left"])
                return discard_card

            hand_options = ["< Back"]
            for idx in legal_indices:
                card = hand[idx]
                hand_options.append(str(idx + 1) + ":" + abbreviate_card(card))

            select_header = "LP:" + abbreviate_card(discard_card) + " SEL CARD:"
            selected_str = select_menu_option(select_header, hand_options)

            if selected_str == "< Back":
                continue

            card_idx = int(selected_str.split(":")[0]) - 1
            played_card = hand.pop(card_idx)

            if "Wild" in played_card or "+4" in played_card:
                chosen_color = select_menu_option("CHOOSE COLOR:", ["Red", "Yellow", "Green", "Blue"])
                if "+4" in played_card:
                    played_card = chosen_color + " +4"
                else:
                    played_card = chosen_color + " Wild"

            print(">>> YOU PLAYED: " + played_card)

            # Display played card face-up full-screen before delivering
            gfx_args = card_to_gfx_args(played_card)
            draw_card_full_screen(gfx_args[0], gfx_args[1])
            wait(1000, MSEC)

            # PHASE 4 EFFECT & VICTORY CHECKS
            if len(hand) == 1:
                # Second-to-last card play (leaves 1 card in hand)
                brain.play_sound(SoundType.SIREN2)
                robot_deliver_card(msg="UNO!")
            elif len(hand) == 0:
                # Last card played
                robot_deliver_card(msg="FINAL CARD!")
            else:
                robot_deliver_card()

            return played_card


# ==========================================
# MAIN GAME EXECUTION (VERSION 2.3)
# ==========================================

# 1. Initialize deck, shuffle deck, and PRINT SHUFFLED DECK TO CONSOLE
uno_deck = build_uno_deck()
shuffle_deck(uno_deck)
print("=== SHUFFLED DECK ===")
print(uno_deck)

# 2. Deal starting hand and PRINT STARTING HAND TO CONSOLE IMMEDIATELY
player_hand = deal_hand(uno_deck, 7)
print("\n=== STARTING HAND (7 CARDS) ===")
print(player_hand)

print("\n==================================")
print("=== NEW UNO GAME STARTED (v2.3) ===")

# 3. EXACT STARTUP FLOW:
# 3A. Display Starting Hand on Screen
view_full_hand(player_hand, "STARTING HAND")

# 3B. Incoming Attack Check
attack_choice = select_menu_option("INCOMING ATTACK?", ["None", "+2", "+4"])
if attack_choice in ["+2", "+4"]:
    penalty = 2 if attack_choice == "+2" else 4
    flash_uno_card_back(penalty)
    robot_fetch_card()
    for _ in range(penalty):
        drawn = draw_card(uno_deck)
        if drawn:
            player_hand.append(drawn)
    view_full_hand(player_hand, "AFTER ATTACK")

# 3C. Prompt for Opponent's First Played Card (Initial Discard)
discard_top = input_discard_pile("OPPONENT PLAYED:")
print(">>> OPPONENT PLAYED: " + str(discard_top))

# Check if opponent played +2 or +4
if "+2" in discard_top or "+4" in discard_top:
    penalty = 2 if "+2" in discard_top else 4
    select_menu_option("ATTACK! DRAW " + str(penalty), ["Draw " + str(penalty) + " Cards"])
    flash_uno_card_back(penalty)
    robot_fetch_card()
    for _ in range(penalty):
        drawn = draw_card(uno_deck)
        if drawn:
            player_hand.append(drawn)
    discard_top = discard_top.replace("+2", "2").replace("+4", "Wild")
    view_full_hand(player_hand, discard_top)

# 4. Continuous Turn Loop
while True:
    if check_game_over(player_hand):
        break

    # 4A. Player Turn ("My Turn")
    discard_top = process_player_turn(discard_top, player_hand, uno_deck)

    if check_game_over(player_hand):
        break

    # 4B. View remaining hand after robot delivers and returns to player
    view_full_hand(player_hand, discard_top)

    # 4C. Opponent Turn Entry
    print_hand_to_console(player_hand, uno_deck, discard_top)
    discard_top = input_discard_pile("OPPONENT PLAYED:")
    print(">>> OPPONENT PLAYED: " + str(discard_top))

    # 4D. Check if opponent played +2 or +4 against player
    if "+2" in discard_top or "+4" in discard_top:
        penalty = 2 if "+2" in discard_top else 4
        select_menu_option("ATTACK! DRAW " + str(penalty), ["Draw " + str(penalty) + " Cards"])
        flash_uno_card_back(penalty)
        robot_fetch_card()
        for _ in range(penalty):
            drawn = draw_card(uno_deck)
            if drawn:
                player_hand.append(drawn)
        discard_top = discard_top.replace("+2", "2").replace("+4", "Wild")
        view_full_hand(player_hand, discard_top)

print("\nGAME OVER - All cards played!")
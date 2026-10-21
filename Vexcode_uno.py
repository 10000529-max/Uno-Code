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
#   Project:     VEXcode EXP UNO - Version 5.5 (4v4 Clear Player Indicator)
#   Author:      VEX
#   Description: - Clean screen displays for 4v4 mode (P1, P2, P3, P4).
#                - Immediate loading response and center-pivot rotation.
# 
# ------------------------------------------

from vex import *

# ==========================================
# MOVEMENT CALIBRATION & SETUP
# ==========================================

DRIVE_SPEED = 40          # Straight driving percentage speed
TURN_SPEED = 30           # Precise turning percentage speed
FORWARD_DEGREES = 850    # Distance between Center and Player stations
TURN_90_DEGREES = 228    # Standard 90-degree turn calibration
ALIGN_RIGHT_DEGREES = 2   # Micro 2 degree adjustment to prevent drift

# Tracks robot cardinal orientation at center: 
# 0 = P1 (North), 1 = P2 (East), 2 = P3 (South), 3 = P4 (West)
current_robot_heading = 0

def configure_motors():
    motor_1.set_stopping(HOLD)
    motor_5.set_stopping(HOLD)
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)

configure_motors()

# ==========================================
# GLOBAL CUSTOM RULES & GAME MODE SETUP
# ==========================================

custom_rules = {
    "stack_similar": False,        # Play matching rank cards together
    "stack_draw2": False,          # Stack +2 when attacked with a +2
    "draw_until_playable": False   # Draw cards until finding a playable card
}

game_mode = "Unchanged"


def show_loading_screen(status_msg="LOADING 4v4..."):
    """Displays immediate feedback to prevent menu screen freezes."""
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.YELLOW)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print("=================")
    brain.screen.set_cursor(3, 1)
    brain.screen.print(status_msg[:16])
    brain.screen.set_cursor(4, 1)
    brain.screen.print("=================")
    wait(100, MSEC)


def setup_custom_rules_menu():
    rule_keys = ["stack_similar", "stack_draw2", "draw_until_playable"]
    rule_names = ["Stack Similar", "Stack +2s", "Draw Till Play"]
    
    current_idx = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        
        brain.screen.set_cursor(1, 1)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.print("CUSTOM RULES MENU"[:16])
        
        brain.screen.set_cursor(3, 1)
        
        if current_idx < len(rule_keys):
            key = rule_keys[current_idx]
            is_on = custom_rules[key]
            status = "ON" if is_on else "OFF"
            
            if is_on:
                brain.screen.set_pen_color(Color.GREEN)
            else:
                brain.screen.set_pen_color(Color.RED)
                
            opt_str = rule_names[current_idx] + ":" + status
            brain.screen.print(("< " + opt_str + " >")[:16])
            
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[L/R]Sel [v]Toggle"[:16])
        else:
            brain.screen.set_pen_color(Color.GREEN)
            brain.screen.print("< Done >"[:16])
            
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(5, 1)
            brain.screen.print("[L/R]Sel [v]Confirm"[:16])
            
        while not (brain.buttonLeft.pressing() or brain.buttonRight.pressing() or brain.buttonCheck.pressing()):
            wait(20, MSEC)
            
        if brain.buttonLeft.pressing():
            current_idx = (current_idx - 1) % (len(rule_keys) + 1)
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
        elif brain.buttonRight.pressing():
            current_idx = (current_idx + 1) % (len(rule_keys) + 1)
            while brain.buttonRight.pressing():
                wait(20, MSEC)
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            if current_idx == len(rule_keys):
                break
            else:
                key = rule_keys[current_idx]
                custom_rules[key] = not custom_rules[key]


def start_main_menu():
    global game_mode
    while True:
        choice = select_menu_option("UNO MAIN MENU", ["Play Game", "Rules", "4v4"])
        if choice == "Rules":
            setup_custom_rules_menu()
        elif choice == "Play Game":
            version_choice = select_menu_option("SELECT VERSION:", ["Unchanged", "Chaotic", "AI"])
            game_mode = version_choice
            break
        elif choice == "4v4":
            game_mode = "4v4"
            show_loading_screen("DEALING CARDS...")
            break

# ==========================================
# COLOR HELPER & GRAPHICAL CARD RENDERER
# ==========================================

def set_color_by_card(card_name):
    card_s = str(card_name)
    if "Red" in card_s:
        brain.screen.set_pen_color(Color.RED)
    elif "Green" in card_s:
        brain.screen.set_pen_color(Color.GREEN)
    elif "Blue" in card_s:
        brain.screen.set_pen_color(Color.BLUE)
    elif "Yellow" in card_s:
        brain.screen.set_pen_color(Color.YELLOW)
    else:
        brain.screen.set_pen_color(Color.WHITE)


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
    
    card = card_str[1:] if len(card_str) > 1 else card_str
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
    elif card_str == "D4" or card_str == "D8":
        brain.screen.set_fill_color(Color.YELLOW)
        brain.screen.draw_rectangle(78, 42, 40, 25)
        brain.screen.set_fill_color(Color.GREEN)
        brain.screen.draw_rectangle(60, 28, 40, 25)
        brain.screen.set_fill_color(Color.BLUE)
        brain.screen.draw_rectangle(42, 42, 40, 25)
        brain.screen.set_fill_color(Color.RED)
        brain.screen.draw_rectangle(60, 56, 40, 25)
        
        brain.screen.set_cursor(3, 8)
        brain.screen.set_pen_color(Color.WHITE)
        if card_str == "D8":
            brain.screen.print("+8")
        else:
            brain.screen.print("+4")
    elif card_str == "M2":
        brain.screen.set_fill_color(Color.PURPLE)
        brain.screen.draw_rectangle(30, 20, 100, 67)
        brain.screen.set_cursor(3, 8)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.print("-2")
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

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)


def card_to_gfx_args(card_name):
    card_s = str(card_name)
    parts = card_s.split(" ")
    color_char = parts[0][0] if len(parts) > 1 and parts[0] in ["Red", "Green", "Blue", "Yellow"] else 'N'

    if "+8" in card_s:
        return ("D8", color_char)
    elif "-2" in card_s:
        return ("M2", color_char)
    elif "Wild" in card_s and "+4" not in card_s:
        return ("W", color_char)
    elif "+4" in card_s:
        return ("D4", color_char)
    
    val = parts[1] if len(parts) > 1 else ""

    if val == "Skip": val = "S"
    elif val == "Reverse": val = "Rv"
    elif val == "+2": val = "D2"

    return (color_char + val, color_char)


def flash_uno_card_back(count=1):
    for _ in range(count):
        draw_card_full_screen("BACK", "N")
        wait(600, MSEC)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        wait(200, MSEC)

# ==========================================
# ROBOT MOVEMENT & SHARED CENTER NAVIGATION
# ==========================================

def robot_drive_forward_2():
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)
    motor_1.spin_for(FORWARD, FORWARD_DEGREES, DEGREES, False)
    motor_5.spin_for(FORWARD, FORWARD_DEGREES, DEGREES, True)
    wait(150, MSEC)


def robot_turn_90_right():
    motor_1.set_velocity(TURN_SPEED, PERCENT)
    motor_5.set_velocity(TURN_SPEED, PERCENT)
    motor_1.spin_for(FORWARD, TURN_90_DEGREES, DEGREES, False)
    motor_5.spin_for(REVERSE, TURN_90_DEGREES, DEGREES, True)
    wait(150, MSEC)
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)


def robot_turn_90_left():
    motor_1.set_velocity(TURN_SPEED, PERCENT)
    motor_5.set_velocity(TURN_SPEED, PERCENT)
    motor_1.spin_for(REVERSE, TURN_90_DEGREES, DEGREES, False)
    motor_5.spin_for(FORWARD, TURN_90_DEGREES, DEGREES, True)
    wait(150, MSEC)
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)


def robot_turn_180():
    robot_turn_90_right()
    wait(100, MSEC)
    robot_turn_90_right()
    wait(100, MSEC)
    if ALIGN_RIGHT_DEGREES > 0:
        motor_1.set_velocity(TURN_SPEED, PERCENT)
        motor_5.set_velocity(TURN_SPEED, PERCENT)
        motor_1.spin_for(FORWARD, ALIGN_RIGHT_DEGREES, DEGREES, False)
        motor_5.spin_for(REVERSE, ALIGN_RIGHT_DEGREES, DEGREES, True)
        wait(100, MSEC)
    motor_1.set_velocity(DRIVE_SPEED, PERCENT)
    motor_5.set_velocity(DRIVE_SPEED, PERCENT)


def turn_to_player_position(target_p_idx):
    """
    Pivots at Center Deck to face active Player Station:
    0 = P1 (North), 1 = P2 (East), 2 = P3 (South), 3 = P4 (West)
    """
    global current_robot_heading
    diff = (target_p_idx - current_robot_heading) % 4

    if diff == 1:
        robot_turn_90_right()
    elif diff == 2:
        robot_turn_180()
    elif diff == 3:
        robot_turn_90_left()

    current_robot_heading = target_p_idx


def move_from_center_to_player(p_idx):
    """
    Pivots at Center toward player `p_idx` and drives outward to player station.
    """
    turn_to_player_position(p_idx)
    robot_drive_forward_2()


def play_card_from_player_to_center(played_card, player_lbl="P1", is_uno=False, is_final=False):
    """
    Robot starts at Player Station:
    1. Turns 180° and drives to the SHARED CENTER.
    2. Displays card graphics and drops card on Center pile.
    3. Turns 180° and drives BACK to Player Station.
    4. Turns 180° and returns to CENTER to prepare for next player's turn.
    """
    robot_turn_180()
    robot_drive_forward_2()

    gfx_args = card_to_gfx_args(played_card)
    draw_card_full_screen(gfx_args[0], gfx_args[1])

    if is_uno:
        brain.play_sound(SoundType.SIREN2)
        brain.screen.set_cursor(1, 1)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.print("     UNO!     ")
    elif is_final:
        brain.screen.set_cursor(1, 1)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.print("  FINAL CARD! ")

    wait(1200, MSEC)

    robot_turn_180()
    robot_drive_forward_2()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    msg = (player_lbl + " PLAYED") if player_lbl else "CARD PLAYED"
    brain.screen.print(msg[:16])
    wait(1000, MSEC)

    robot_turn_180()
    robot_drive_forward_2()
    robot_turn_180()


def robot_fetch_card(count=1):
    robot_turn_180()
    robot_drive_forward_2()

    flash_uno_card_back(count)

    robot_turn_180()
    robot_drive_forward_2()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    brain.screen.print("    CARD ADDED   ")
    wait(1000, MSEC)


def robot_fetch_until_playable(hand, deck, top_card):
    robot_turn_180()
    robot_drive_forward_2()

    drawn_count = 0
    while True:
        drawn = draw_card(deck)
        if not drawn:
            break
        hand.append(drawn)
        drawn_count += 1
        flash_uno_card_back(1)

        legal = get_legal_moves(hand, top_card)
        if legal:
            break

    robot_turn_180()
    robot_drive_forward_2()

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(3, 1)
    msg = str(drawn_count) + " CARDS DREW"
    brain.screen.print(msg[:16])
    wait(1200, MSEC)


def victory_dance(winner_name="WINNER!"):
    brain.play_sound(SoundType.ALARM2)
    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    brain.screen.print(winner_name[:16])
    
    robot_turn_90_right()
    robot_turn_90_right()
    robot_drive_forward_2()

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

    if game_mode in ["Chaotic", "AI", "4v4"]:
        for _ in range(4):
            deck.append("+8")
            deck.append("-2")
        
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
    card_s = str(card)
    if card_s == "Wild":
        return "WLD"
    if card_s == "+4":
        return "W+4"
    if card_s == "+8":
        return "W+8"
    if card_s == "-2":
        return "M-2"
    
    parts = card_s.split(" ")
    if len(parts) == 2:
        color_code = parts[0][0]
        value = parts[1]
        if value == "Skip":
            value = "SK"
        elif value == "Reverse":
            value = "RV"
        return color_code + value
    return card_s[:4]

def get_card_rank(card_str):
    parts = str(card_str).split(" ")
    if len(parts) > 1:
        return parts[1]
    return parts[0]

def print_hand_to_console(hand, deck, current_top):
    print("TOP: " + str(current_top) + " | DECK: " + str(len(deck)) + " | HAND: " + str(len(hand)))

# ==========================================
# PHASE 3: GAME STATE & RULE FUNCTIONS
# ==========================================

def get_legal_moves(hand, top_card):
    legal_indices = []
    top_s = str(top_card)
    top_parts = top_s.split(" ")
    top_color = top_parts[0] if len(top_parts) > 0 else ""
    top_val = top_parts[1] if len(top_parts) > 1 else top_parts[0]

    for idx, card in enumerate(hand):
        card_s = str(card)
        if "Wild" in card_s or "+4" in card_s or "+8" in card_s or "-2" in card_s:
            legal_indices.append(idx)
        else:
            card_parts = card_s.split(" ")
            card_color = card_parts[0] if len(card_parts) > 0 else ""
            card_val = card_parts[1] if len(card_parts) > 1 else card_parts[0]

            if card_color == top_color or card_val == top_val:
                legal_indices.append(idx)

    return legal_indices


def check_game_over(hand, winner_label="WINNER!"):
    if len(hand) == 0:
        victory_dance(winner_label)
        return True
    return False

def get_ai_best_color(hand):
    color_counts = {"Red": 0, "Yellow": 0, "Green": 0, "Blue": 0}
    for card in hand:
        card_s = str(card)
        for c in color_counts:
            if c in card_s:
                color_counts[c] += 1
    best_color = "Red"
    max_c = -1
    for c, count in color_counts.items():
        if count > max_c:
            max_c = count
            best_color = c
    return best_color

# ==========================================
# PHASE 4: MENU & SCREEN INTERACTION SYSTEM
# ==========================================

def select_menu_option(header_title, options, option_color=Color.GREEN):
    selected_index = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        
        brain.screen.set_cursor(1, 1)
        brain.screen.print(header_title[:16])
        
        brain.screen.set_cursor(3, 1)
        brain.screen.set_pen_color(option_color)
        opt_text = "< " + str(options[selected_index]) + " >"
        brain.screen.print(opt_text[:16])
        
        brain.screen.set_pen_color(Color.WHITE)
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


def select_menu_option_indexed(header_title, options, option_color=Color.GREEN):
    selected_index = 0
    
    while True:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        
        brain.screen.set_cursor(1, 1)
        brain.screen.print(header_title[:16])
        
        brain.screen.set_cursor(3, 1)
        brain.screen.set_pen_color(option_color)
        opt_text = "< " + str(options[selected_index]) + " >"
        brain.screen.print(opt_text[:16])
        
        brain.screen.set_pen_color(Color.WHITE)
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
            return (selected_index, options[selected_index])


def view_full_hand(hand):
    page = 0
    while True:
        max_page = (len(hand) - 1) // 8 if len(hand) > 0 else 0
        if page > max_page:
            page = max_page

        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.clear_screen()
        
        slots = [[1, 1], [1, 9], [2, 1], [2, 9], [3, 1], [3, 9], [4, 1], [4, 9]]
        start_idx = page * 8
        end_idx = min(start_idx + 8, len(hand))
        
        if not hand:
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(3, 1)
            brain.screen.print("(HAND EMPTY)"[:16])
        else:
            for i in range(start_idx, end_idx):
                slot = slots[i - start_idx]
                card_item = hand[i]
                set_color_by_card(card_item)
                
                brain.screen.set_cursor(slot[0], slot[1])
                lbl = str(i + 1) + ":" + abbreviate_card(card_item)
                brain.screen.print(lbl[:7])
                
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_cursor(5, 1)
        if max_page > 0:
            brain.screen.print("[L/R]Pg  [v]OK"[:16])
        else:
            brain.screen.print("   [v] Continue"[:16])
            
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


def input_top_card():
    top_options = ["Red", "Yellow", "Green", "Blue", "Wild"]
    chosen_color = select_menu_option("TOP CARD COLOR:", top_options)
    
    if chosen_color == "Wild":
        wild_options = ["Wild", "+4"]
        if game_mode in ["Chaotic", "AI", "4v4"]:
            wild_options.extend(["+8", "-2"])
        wild_type = select_menu_option("WILD TYPE:", wild_options)
        
        if wild_type in ["+4", "+8", "-2"]:
            eff_color = select_menu_option("EFFECT COLOR:", ["Red", "Yellow", "Green", "Blue"])
            card_res = eff_color + " " + wild_type
        else:
            eff_color = select_menu_option("EFFECT COLOR:", ["Red", "Yellow", "Green", "Blue"])
            card_res = eff_color + " Wild"
    else:
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]
        chosen_val = select_menu_option("TOP CARD VALUE:", values)
        card_res = chosen_color + " " + chosen_val

    return card_res


def handle_draw_action(hand, deck, top_card):
    if custom_rules["draw_until_playable"]:
        robot_fetch_until_playable(hand, deck, top_card)
    else:
        robot_fetch_card(count=1)
        drawn = draw_card(deck)
        if drawn:
            hand.append(drawn)
        else:
            select_menu_option("DECK EMPTY!", ["No Cards Left"])


# ==========================================
# AUTONOMOUS PLAYER TURN ENGINE (4v4 / AI)
# ==========================================

def process_autonomous_turn(discard_card, hand, deck, player_lbl="P1"):
    legal_indices = get_legal_moves(hand, discard_card)

    if not legal_indices:
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        brain.screen.set_cursor(3, 1)
        brain.screen.print((player_lbl + " DRAWING...")[:16])
        wait(800, MSEC)
        handle_draw_action(hand, deck, discard_card)
        return discard_card

    chosen_idx = legal_indices[0]
    for idx in legal_indices:
        card_s = str(hand[idx])
        if not any(w in card_s for w in ["Wild", "+4", "+8", "-2"]):
            chosen_idx = idx
            break

    played_card = hand.pop(chosen_idx)

    # Automatic Stack Similar Rule
    if custom_rules["stack_similar"]:
        played_rank = get_card_rank(played_card)
        matching_indices = [i for i, c in enumerate(hand) if get_card_rank(c) == played_rank]
        if matching_indices:
            stacked_group = [played_card]
            for m_idx in sorted(matching_indices, reverse=True):
                stacked_group.append(hand.pop(m_idx))
            played_card = stacked_group.pop(-1)

    # Automatic Wild Color Selection
    played_card_s = str(played_card)
    if any(w in played_card_s for w in ["Wild", "+4", "+8", "-2"]):
        chosen_color = get_ai_best_color(hand)
        if "+8" in played_card_s:
            played_card = chosen_color + " +8"
        elif "+4" in played_card_s:
            played_card = chosen_color + " +4"
        elif "-2" in played_card_s:
            played_card = chosen_color + " -2"
        else:
            played_card = chosen_color + " Wild"

    played_final_s = str(played_card)

    if "-2" in played_final_s:
        for _ in range(2):
            if hand:
                discarded = hand.pop(0)
                deck.append(discarded)

    if len(hand) == 1:
        play_card_from_player_to_center(played_card, player_lbl=player_lbl, is_uno=True)
    elif len(hand) == 0:
        play_card_from_player_to_center(played_card, player_lbl=player_lbl, is_final=True)
    else:
        play_card_from_player_to_center(played_card, player_lbl=player_lbl)

    return played_card


# ==========================================
# HUMAN PLAYER INTERACTIVE TURN ENGINE
# ==========================================

def process_player_turn(discard_card, hand, deck):
    while True:
        turn_menu_title = "YOUR MOVE:"
        options = ["Play Card", "Draw 1 Card", "View Hand"]

        choice = select_menu_option(turn_menu_title, options)

        if choice == "Play Card":
            legal_indices = get_legal_moves(hand, discard_card)

            if not legal_indices:
                select_menu_option("NO LEGAL MOVES!", ["Draw Cards"])
                handle_draw_action(hand, deck, discard_card)
                return discard_card

            hand_options = ["Back"]
            for idx in legal_indices:
                card = hand[idx]
                hand_options.append(abbreviate_card(card))

            select_header = "Select Move"
            sel_idx, selected_str = select_menu_option_indexed(select_header, hand_options)

            if selected_str == "Back" or sel_idx == 0:
                continue

            card_idx = legal_indices[sel_idx - 1]
            played_card = hand.pop(card_idx)

            if custom_rules["stack_similar"]:
                played_rank = get_card_rank(played_card)
                matching_indices = [i for i, c in enumerate(hand) if get_card_rank(c) == played_rank]
                
                if matching_indices:
                    stack_choice = select_menu_option("STACK CARDS?", ["Yes", "No"])
                    if stack_choice == "Yes":
                        stacked_group = [played_card]
                        for m_idx in sorted(matching_indices, reverse=True):
                            stacked_group.append(hand.pop(m_idx))
                        
                        top_options = [abbreviate_card(c) for c in stacked_group]
                        top_idx, _ = select_menu_option_indexed("WHICH ON TOP?", top_options)
                        played_card = stacked_group.pop(top_idx)
                else:
                    brain.screen.set_fill_color(Color.BLACK)
                    brain.screen.set_pen_color(Color.YELLOW)
                    brain.screen.clear_screen()
                    brain.screen.set_cursor(3, 1)
                    brain.screen.print(" NO STACK AVAIL ")
                    wait(1000, MSEC)

            played_card_s = str(played_card)
            if any(w in played_card_s for w in ["Wild", "+4", "+8", "-2"]):
                chosen_color = select_menu_option("CHOOSE COLOR:", ["Red", "Yellow", "Green", "Blue"])
                if "+8" in played_card_s:
                    played_card = chosen_color + " +8"
                elif "+4" in played_card_s:
                    played_card = chosen_color + " +4"
                elif "-2" in played_card_s:
                    played_card = chosen_color + " -2"
                else:
                    played_card = chosen_color + " Wild"

            played_final_s = str(played_card)

            if "-2" in played_final_s and game_mode in ["Chaotic", "AI", "4v4"]:
                brain.screen.set_fill_color(Color.BLACK)
                brain.screen.set_pen_color(Color.PURPLE)
                brain.screen.clear_screen()
                brain.screen.set_cursor(3, 1)
                brain.screen.print(" DISCARD 2 CARDS ")
                wait(1000, MSEC)
                
                for _ in range(2):
                    if hand:
                        discarded = hand.pop(0)
                        deck.append(discarded)

            if len(hand) == 1:
                play_card_from_player_to_center(played_card, player_lbl="YOU", is_uno=True)
            elif len(hand) == 0:
                play_card_from_player_to_center(played_card, player_lbl="YOU", is_final=True)
            else:
                play_card_from_player_to_center(played_card, player_lbl="YOU")

            return played_card

        elif choice == "Draw 1 Card":
            handle_draw_action(hand, deck, discard_card)
            return discard_card

        elif choice == "View Hand":
            view_full_hand(hand)
            continue


# ==========================================
# MAIN GAME EXECUTION (VERSION 5.5)
# ==========================================

start_main_menu()

uno_deck = build_uno_deck()
shuffle_deck(uno_deck)

discard_top = ""

# ==========================================
# 4v4 AUTONOMOUS SHARED-CENTER MODE
# ==========================================

if game_mode == "4v4":
    show_loading_screen("DEALING CARDS...")
    hands = [deal_hand(uno_deck, 7) for _ in range(4)]
    player_names = ["P1-NORTH", "P2-EAST", "P3-SOUTH", "P4-WEST"]

    drawn_start = draw_card(uno_deck)
    while drawn_start and any(w in str(drawn_start) for w in ["Wild", "+4", "+8", "-2", "+2", "Skip", "Reverse"]):
        uno_deck.append(drawn_start)
        shuffle_deck(uno_deck)
        drawn_start = draw_card(uno_deck)
    discard_top = drawn_start if drawn_start else "Red 5"

    current_p = 0
    direction = 1

    while True:
        p_lbl = player_names[current_p]

        # 1. Clear display and explicitly print player label
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.clear_screen()
        brain.screen.set_cursor(2, 1)
        brain.screen.print((p_lbl + " TURN")[:16])
        brain.screen.set_cursor(4, 1)
        brain.screen.print(("TOP: " + abbreviate_card(discard_top))[:16])
        wait(100, MSEC)

        # 2. Drive from Center OUT to target Player Station (P1=0, P2=1, P3=2, P4=3)
        move_from_center_to_player(current_p)

        discard_str = str(discard_top)

        # 3. Handle pending draw penalties
        if any(attack in discard_str for attack in ["+2", "+4", "+8"]):
            if "+2" in discard_str: pen = 2
            elif "+4" in discard_str: pen = 4
            elif "+8" in discard_str: pen = 8
            else: pen = 0

            if "+2" in discard_str and custom_rules["stack_draw2"]:
                p2_idx = [i for i, c in enumerate(hands[current_p]) if "+2" in str(c)]
                if p2_idx:
                    played_2 = hands[current_p].pop(p2_idx[0])
                    brain.screen.set_fill_color(Color.BLACK)
                    brain.screen.set_pen_color(Color.GREEN)
                    brain.screen.clear_screen()
                    brain.screen.set_cursor(3, 1)
                    brain.screen.print((p_lbl + " STACK +2")[:16])
                    wait(800, MSEC)
                    play_card_from_player_to_center(played_2, player_lbl=p_lbl)
                    discard_top = played_2
                    pen = 0

            if pen > 0:
                robot_fetch_card(count=pen)
                for _ in range(pen):
                    d = draw_card(uno_deck)
                    if d: hands[current_p].append(d)

        # 4. Execute player turn (Player Station -> Center -> Player Station -> Resets to Center)
        discard_top = process_autonomous_turn(discard_top, hands[current_p], uno_deck, player_lbl=p_lbl)

        # 5. Check victory state
        if check_game_over(hands[current_p], winner_label=p_lbl + " WINS!"):
            break

        # 6. Direction & Skip handling (Cycles 0 -> 1 -> 2 -> 3)
        discard_final_s = str(discard_top)
        if "Skip" in discard_final_s:
            current_p = (current_p + 2 * direction) % 4
        elif "Reverse" in discard_final_s:
            direction *= -1
            current_p = (current_p + direction) % 4
        else:
            current_p = (current_p + direction) % 4

# ==========================================
# HUMAN VS AI GAME MODE
# ==========================================

elif game_mode == "AI":
    player_hand = deal_hand(uno_deck, 7)
    ai_hand = deal_hand(uno_deck, 7)

    drawn_start = draw_card(uno_deck)
    while drawn_start and any(w in str(drawn_start) for w in ["Wild", "+4", "+8", "-2", "+2", "Skip", "Reverse"]):
        uno_deck.append(drawn_start)
        shuffle_deck(uno_deck)
        drawn_start = draw_card(uno_deck)
    discard_top = drawn_start if drawn_start else "Red 5"

    while True:
        # --- 1. AI TURN ---
        move_from_center_to_player(2)
        discard_str = str(discard_top)
        
        if any(attack in discard_str for attack in ["+2", "+4", "+8"]):
            if "+2" in discard_str: pen = 2
            elif "+4" in discard_str: pen = 4
            elif "+8" in discard_str: pen = 8
            else: pen = 0
            
            if "+2" in discard_str and custom_rules["stack_draw2"]:
                p2_idx = [i for i, c in enumerate(ai_hand) if "+2" in str(c)]
                if p2_idx:
                    played_2 = ai_hand.pop(p2_idx[0])
                    play_card_from_player_to_center(played_2, player_lbl="AI")
                    discard_top = played_2
                    pen = 0
            
            if pen > 0:
                robot_fetch_card(count=pen)
                for _ in range(pen):
                    d = draw_card(uno_deck)
                    if d: ai_hand.append(d)

        discard_top = process_autonomous_turn(discard_top, ai_hand, uno_deck, player_lbl="AI")
        if check_game_over(ai_hand, winner_label="AI WINS!"):
            break

        # --- 2. HUMAN PLAYER TURN ---
        move_from_center_to_player(0)
        discard_str = str(discard_top)
        
        if any(attack in discard_str for attack in ["+2", "+4", "+8"]):
            if "+2" in discard_str: pen = 2
            elif "+4" in discard_str: pen = 4
            elif "+8" in discard_str: pen = 8
            else: pen = 0

            if "+2" in discard_str and custom_rules["stack_draw2"]:
                p2_idx = [i for i, c in enumerate(player_hand) if "+2" in str(c)]
                if p2_idx:
                    st_opt = select_menu_option("AI ATTACK! STACK?", ["Stack +2", "Take Cards"])
                    if st_opt == "Stack +2":
                        played_2 = player_hand.pop(p2_idx[0])
                        play_card_from_player_to_center(played_2, player_lbl="YOU")
                        discard_top = played_2
                        pen = 0

            if pen > 0:
                select_menu_option("TAKE + " + str(pen) + " CARDS", ["Confirm"])
                robot_fetch_card(count=pen)
                for _ in range(pen):
                    d = draw_card(uno_deck)
                    if d: player_hand.append(d)

        print_hand_to_console(player_hand, uno_deck, discard_top)
        discard_top = process_player_turn(discard_top, player_hand, uno_deck)
        
        if check_game_over(player_hand, winner_label="YOU WIN!"):
            break

# ==========================================
# CLASSIC HUMAN GAME MODES ("Unchanged", "Chaotic")
# ==========================================

else:
    player_hand = deal_hand(uno_deck, 7)

    while True:
        if check_game_over(player_hand, winner_label="WINNER!"):
            break

        view_full_hand(player_hand)

        attack_options = ["None", "Draw 2", "Draw 4"]
        if game_mode == "Chaotic":
            attack_options.append("Draw 8")

        attack_choice = select_menu_option("INCOMING ATTACK?", attack_options)
        if attack_choice != "None":
            if attack_choice == "Draw 2": penalty = 2
            elif attack_choice == "Draw 4": penalty = 4
            elif attack_choice == "Draw 8": penalty = 8
            else: penalty = 0
            
            if attack_choice == "Draw 2" and custom_rules["stack_draw2"]:
                plus2_indices = [i for i, c in enumerate(player_hand) if "+2" in str(c)]
                if plus2_indices:
                    stack_opt = select_menu_option("STACK +2?", ["Stack", "Take Cards"])
                    if stack_opt == "Stack":
                        plus2_idx = plus2_indices[0]
                        played_2 = player_hand.pop(plus2_idx)
                        
                        brain.screen.set_fill_color(Color.BLACK)
                        brain.screen.set_pen_color(Color.GREEN)
                        brain.screen.clear_screen()
                        brain.screen.set_cursor(3, 1)
                        brain.screen.print("   STACKED +2!   ")
                        wait(1000, MSEC)
                        
                        play_card_from_player_to_center(played_2, player_lbl="YOU")
                        penalty = 0
                else:
                    brain.screen.set_fill_color(Color.BLACK)
                    brain.screen.set_pen_color(Color.RED)
                    brain.screen.clear_screen()
                    brain.screen.set_cursor(3, 1)
                    brain.screen.print(" NO STACK AVAIL ")
                    wait(1000, MSEC)
                    
            if penalty > 0:
                robot_fetch_card(count=penalty)
                for _ in range(penalty):
                    drawn = draw_card(uno_deck)
                    if drawn:
                        player_hand.append(drawn)
                view_full_hand(player_hand)

            continue

        discard_top = input_top_card()
        print_hand_to_console(player_hand, uno_deck, discard_top)

        discard_top = process_player_turn(discard_top, player_hand, uno_deck)

        if check_game_over(player_hand, winner_label="WINNER!"):
            break

print("GAME OVER")
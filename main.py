from threading import Thread
import pyautogui
import random
import time
import string
import numpy as np
import cv2 as cv
from PIL import ImageGrab, Image
import sys

#Immutables
TIME_PER_PLACEMENT = 6
CHECK_FOR_SPELL_RATIO = [0.15, 10]

#Dynamic, mutable
current_card_position = 1
stop_card_thread = False

def locate_on_screen(method, image_name):
    game_over_image_cv = cv.imread(image_name)
    img = ImageGrab.grab()
    img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    res = cv.matchTemplate(img_cv, game_over_image_cv, method)

    # print(res)
    return (res >= 0.8).any()


def check_for_spell():
    print("Checking if card is a spell...")

    # Presses the card in the deck for two seconds
    pyautogui.press(str(current_card_position))
    # During the press, continously checks if a symbol associated with the card being a spell appears
    for _ in range(CHECK_FOR_SPELL_RATIO[1]):
        if stop_card_thread:
            break

        if not locate_on_screen(cv.TM_CCOEFF_NORMED, "spell.png"):
            # Does not appear
            pass
        else:
            # Appears
            print("The card is a spell.")
            return True
        time.sleep(CHECK_FOR_SPELL_RATIO[0])
    print("The card is not a spell.")
    return False

def card_loop():
    while True:
        global current_card_position

        # Checks if thread "check_loop" detects the game finishes
        if stop_card_thread:
            # Game is finished
            time.sleep(1.5)
        else:
            # Game is not finished
            # The maximum cards in a hand is 4, if it has surpasses that reset.
            if current_card_position == 5:
                current_card_position = 1
            
            print(f"Attemping to place card {current_card_position}.")

            # Checks if the card is a spell.
            if check_for_spell():
                # The card is a spell, click tower.
                tower_selection = random.choice(["c", "d"])
                print(f"Attacking {'left' if tower_selection == 'a' else 'right'} tower!")
                pyautogui.press(tower_selection)
            else:
                # The card is not a spell, click in a random location in our turf.
                pyautogui.press(str(random.randint(6, 9)))
            print("___________________")

            # Goes to the next card in the hand/
            current_card_position += 1

            # Waits for the specified time to place another card, while waiting; checks if game finishes.
            for i in range(TIME_PER_PLACEMENT * 2):
                if stop_card_thread:
                    time.sleep(3)
                    break
                time.sleep(0.5)



def check_loop():
    global stop_card_thread
    while True:
        time.sleep(0.25)
        if locate_on_screen(cv.TM_CCOEFF_NORMED, 'trophy.png'):
            stop_card_thread = True

            for i in range(100):
                if not locate_on_screen(cv.TM_CCOEFF_NORMED, "okO.png"):
                    # Is not found
                    pass
                else:
                    print("OK button found.")
                    break

                if i == 99:
                    print("Did not go to 'OK' screen... aborting...")
                    exit()
                time.sleep(0.1)

            pyautogui.press("a")
            # Searches for the "B" in battle.
            for i in range(1000):
                if not locate_on_screen(cv.TM_CCOEFF_NORMED, "battleB.png"):
                    # Is not found
                    pass
                else:
                    # Is found
                    print("Found battle button.")
                    pyautogui.press("b")
                    stop_card_thread = False
                    break
                time.sleep(0.1)

                if i == 999:
                    print("Did not go to title... aborting...")
                    exit()

                time.sleep(0.11)




        else:
            stop_card_thread = False

thread1 = Thread(target=check_loop).start()
thread2 = Thread(target=card_loop).start()
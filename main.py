import time
import os
import file_handling
import scheduler
import sys

DI_DICT = {
    "again": 0,
    "hard": 1,
    "good": 2,
    "easy": 3
}

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def rate_card(card, skip=False):
    if skip:
        card["rating"] = DI_DICT["hard"]
        return card

    print("Rate the difficulty of that question.")
    user_rating = input("Again\nHard\nGood\nEasy\n").lower()
    card["rating"] += DI_DICT.get(user_rating, 1)

    return card

try:
    cards = scheduler.filter_by_due_date(file_handling.load_progress())
    if not cards:
        print("Well done! You've caught up with all pending cards!")

    for card in cards:
        card_id = card["id"]
        funcs_dict = file_handling.QUESTION_TYPES[card_id]

        vars = funcs_dict["vars"]()
        answer = funcs_dict["solve"](**vars)

        question_text = card["question"].format(**vars)

        print(question_text)
        user_ans = float(input())

        if user_ans == answer:
            print("CORRECT")
            rate_card(card)
        else:
            print("INCORRECT")
            print(f"\n\nCorrect answer was: {answer}")
            rate_card(card, True)
            input() # stall until user wants to continue

        scheduler.update_card_due_date(card)
        clear_terminal()

    file_handling.save_progress(cards)
    print("Bye!")
except KeyboardInterrupt:
    print("Ctrl+C")
    try:
        file_handling.save_progress(cards)
        print("Bye!")
    except NameError:
        pass # cards isn't loaded yet

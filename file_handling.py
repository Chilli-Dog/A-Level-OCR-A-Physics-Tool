import json
import os
from datetime import datetime
from email.utils import parsedate_to_datetime
import question_types


QUESTION_TYPES = question_types.QUESTION_TYPES

def make_default_card(card_id):
    return {
        "id": card_id,
        "rating": 0,
        "next_review_date": datetime.now().date(),
        "question": QUESTION_TYPES[card_id]["question"]
    }

# main file handling
FILENAME = "flashcard_info.json"
SUPERSCRIPTS = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")

def sci(x, digits=2):
    mantissa, exp = f"{x:.{digits}e}".split("e")
    return f"{mantissa}×10{str(int(exp)).translate(SUPERSCRIPTS)}"

def fmt_num(x, low=1e-3, high=9999):
    if isinstance(x, (int, float)) and x != 0 and (abs(x) > high or abs(x) < low):
        return sci(x)
    return str(x)

def save_progress(cards, filename=FILENAME):
    with open(filename, "w") as f:
        # default=str automatically converts date objects to strings safely
        json.dump(cards, f, indent=4, default=str)
    print("Progress saved successfully!")


def load_progress(filename=FILENAME):
    cards = []

    if os.path.exists(filename):
        with open(filename, "r") as f:
            cards = json.load(f)

        for card in cards:
            if isinstance(card["next_review_date"], str):
                date_str = card["next_review_date"]
                try:
                    card["next_review_date"] = datetime.fromisoformat(date_str).date()
                except ValueError:
                    try:
                        card["next_review_date"] = parsedate_to_datetime(date_str).date()
                    except Exception:
                        pass
        print("Loaded previous session progress.")
    else:
        print("No saved file found!")

    cards = [c for c in cards if c["id"] in QUESTION_TYPES]

    existing_ids = {c["id"] for c in cards}
    for card_id in QUESTION_TYPES:
        if card_id not in existing_ids:
            cards.append(make_default_card(card_id))

    for card in cards:
        card["question"] = QUESTION_TYPES[card["id"]]["question"]

    return cards

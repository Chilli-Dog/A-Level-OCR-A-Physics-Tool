from datetime import datetime, timedelta

# score: days until next review
RATING_INTERVALS = {
    0: 0,
    1: 1,
    2: 2,
    3: 4,
    4: 8,
    5: 12,
    6: 15,
    7: 20,
    8: 23,
    9: 27,
    10: 30
}

def update_card_due_date(card):
    user_rating = card["rating"]

    days_interval = RATING_INTERVALS.get(user_rating, 1)
    if user_rating > 10:
        days_interval = 30
        card["rating"] = 10

    next_due_date = datetime.now().date() + timedelta(days=days_interval)
    card["next_review_date"] = next_due_date.isoformat()

def filter_by_due_date(cards):
    today_date = datetime.now().date()
    new_cards = []
    for card in cards:
        card_date = card["next_review_date"]
        if card_date <= today_date:
            new_cards.append(card)

    return new_cards

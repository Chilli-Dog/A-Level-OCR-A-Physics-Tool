from flask import Flask, jsonify, request, render_template
import file_handling
import scheduler

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/cards", methods=["GET"])
def get_due_cards():
    cards = scheduler.filter_by_due_date(file_handling.load_progress())
    prepared_cards = []

    for card in cards:
        card_id = card["id"]
        funcs_dict = file_handling.QUESTION_TYPES[card_id]

        vars_dict = funcs_dict["vars"]()
        answer = funcs_dict["solve"](**vars_dict)

        display_vars = {k: file_handling.fmt_num(v) for k, v in vars_dict.items()}
        formatted_question = card["question"].format(**display_vars)

        display_answer = file_handling.fmt_num(answer)

        prepared_cards.append({
            "id": card_id,
            "question": formatted_question,
            "correct_answer": answer,
            "display_answer": display_answer,
            "rating": card["rating"],
            "next_review_date": card["next_review_date"]
        })

    # TODO: Could add shuffle to the prepared_cards
    return jsonify(prepared_cards)

@app.route("/api/save", methods=["POST"])
def save_cards():
    updated_cards = request.json

    minimal_cards = []
    for card in updated_cards:
        scheduler.update_card_due_date(card)
        minimal_cards.append({
            "id": card["id"],
            "rating": card["rating"],
            "next_review_date": card["next_review_date"]
        })

    file_handling.save_progress(minimal_cards)
    return jsonify({"status": "success", "message": "Progress Saved."})

if __name__ == "__main__":
    app.run(debug=False, port=5000)

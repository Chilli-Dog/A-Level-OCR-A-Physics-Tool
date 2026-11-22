let due_cards = [];
let current_idx = 0;
const DI_DICT = {
    "again": 0,
    "hard": 1,
    "good": 2,
    "easy": 3
};
let current_rating = null;
let resolve_rating_promise = null;

const TOLERANCE = 0.01; // 1% relative tolerance

function is_correct(userVal, correct) {
  if (Number.isNaN(userVal)) return false;
  const allowed = Math.max(Math.abs(correct) * TOLERANCE, 1e-9);
  return Math.abs(userVal - correct) <= allowed;
}

async function fetch_cards() {
  try {
    let response = await fetch('/api/cards');
    due_cards = await response.json();

    if (due_cards.length > 0) {
      show_card();
      document.getElementById('inputs').style.display = 'block';
    } else {
      document.getElementById("question-text").innerText = "No cards due today, well done!";
      document.getElementById('inputs').style.display = 'none';
    }
  }
  catch (error) {
    console.error("Failed to load cards: ", error);
    document.getElementById('question-text').innerText = "Error connecting to Python";
  }
}

async function save_to_backend() {
    await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(due_cards)
    });
}

function rate_card(d) {
    let ratingVal = 0;
    if (d === 'again') {
        ratingVal = 1;
    } else if (d === 'hard') {
        ratingVal = 2;
    } else if (d === 'good') {
        ratingVal = 3;
    } else if (d === 'easy') {
        ratingVal = 4;
    }

  document.getElementById('btn-container').style.display = 'none';
  document.getElementById('user-answer').value = '';

    if (resolve_rating_promise) {
        resolve_rating_promise(ratingVal);
        resolve_rating_promise = null;
    }
}

async function rate_card_backend(card, skip = false) {
    if (skip) {
        card.rating += DI_DICT.again;
        return card;
    }

    let btn_div = document.getElementById('btn-container');
    btn_div.style.display = 'block';

    let userRating = await new Promise((resolve) => {
        resolve_rating_promise = resolve;
    });

    card.rating += userRating;
    return card;
}

function show_card() {
  let card = due_cards[current_idx];
  document.getElementById('question-text').innerText = card.question;
}

async function check_answer() {
  let card = due_cards[current_idx];
  let userVal = parseFloat(document.getElementById('user-answer').value);
  let out = document.getElementById('js-output');

  if (is_correct(userVal, card.correct_answer)) {
    out.innerText = "CORRECT!";
    card = await rate_card_backend(card);
  } else {
    // TODO: temporary fix for the allowed value being somewhat faulty for small numbers
    let notes = "";
    if (card.correct_answer < 1e-9) {
      notes = "\nThis 'incorrect' answer could've been caused by a known bug in the code. Please contact me to fix it.";
    }
    out.innerText = "INCORRECT. The correct answer was: " + card.display_answer;
    card = await rate_card_backend(card, true);
  }

  await save_to_backend();

  current_idx++;
  if (current_idx < due_cards.length) {
      show_card();
  } else {
      document.getElementById('question-text').innerText = "Session complete!";
      document.getElementById('inputs').style.display = 'none';
  }
}

fetch_cards();

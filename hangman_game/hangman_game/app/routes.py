from flask import Blueprint, render_template, request, jsonify, session
import random

bp = Blueprint('main', __name__)

# Categories and words
data = {
    'Animals': ['elephant', 'giraffe', 'kangaroo', 'alligator', 'dolphin', 'penguin', 'rhinoceros', 'chimpanzee'],
    'Fruits': ['banana', 'strawberry', 'pineapple', 'watermelon', 'blueberry', 'mango', 'pomegranate', 'apricot'],
    'Countries': ['brazil', 'germany', 'australia', 'canada', 'japan', 'nigeria', 'sweden', 'portugal'],
    'Sports': ['football', 'basketball', 'cricket', 'badminton', 'baseball', 'hockey', 'volleyball', 'tennis']
}

difficulty_guesses = {
    'easy': 10,
    'medium': 7,
    'hard': 5
}

@bp.route('/')
def index():
    return render_template('index.html', categories=list(data.keys()))

@bp.route('/start_game', methods=['POST'])
def start_game():
    category = request.json.get('category')
    difficulty = request.json.get('difficulty')
    word = random.choice(data[category])
    session['word'] = word
    session['guesses_left'] = difficulty_guesses[difficulty]
    session['guessed_letters'] = []
    session['score'] = session.get('score', 0)
    return jsonify({'word_length': len(word), 'guesses_left': session['guesses_left'], 'score': session['score']})

@bp.route('/guess', methods=['POST'])
def guess():
    letter = request.json.get('letter').lower()
    word = session['word']
    guessed_letters = session['guessed_letters']
    if letter in guessed_letters:
        return jsonify({'status': 'already_guessed'})
    guessed_letters.append(letter)
    session['guessed_letters'] = guessed_letters
    if letter in word:
        if all(l in guessed_letters for l in word):
            session['score'] += 1
            return jsonify({'status': 'win', 'word': word, 'score': session['score']})
        else:
            return jsonify({'status': 'correct', 'guessed_letters': guessed_letters})
    else:
        session['guesses_left'] -= 1
        if session['guesses_left'] <= 0:
            session['score'] = 0
            return jsonify({'status': 'lose', 'word': word, 'score': session['score']})
        else:
            return jsonify({'status': 'incorrect', 'guesses_left': session['guesses_left'], 'guessed_letters': guessed_letters})

@bp.route('/get_state', methods=['GET'])
def get_state():
    word = session.get('word', '')
    guessed_letters = session.get('guessed_letters', [])
    display = [l if l in guessed_letters else '_' for l in word]
    return jsonify({
        'display': display,
        'guesses_left': session.get('guesses_left', 0),
        'guessed_letters': guessed_letters,
        'score': session.get('score', 0)
    })

@bp.route('/hint', methods=['POST'])
def hint():
    word = session.get('word', '')
    guessed_letters = session.get('guessed_letters', [])
    unguessed = [l for l in set(word) if l not in guessed_letters]
    if not unguessed or session['guesses_left'] <= 0:
        return jsonify({'status': 'no_hint'})
    hint_letter = random.choice(unguessed)
    guessed_letters.append(hint_letter)
    session['guessed_letters'] = guessed_letters
    session['guesses_left'] -= 1
    if all(l in guessed_letters for l in word):
        session['score'] += 1
        return jsonify({'status': 'win', 'word': word, 'score': session['score'], 'hint': hint_letter})
    if session['guesses_left'] <= 0:
        session['score'] = 0
        return jsonify({'status': 'lose', 'word': word, 'score': session['score'], 'hint': hint_letter})
    return jsonify({'status': 'hint', 'hint': hint_letter, 'guesses_left': session['guesses_left'], 'guessed_letters': guessed_letters})
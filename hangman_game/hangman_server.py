from flask import Flask, render_template, request, jsonify, session
import random
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'hangman_secret_key'
CORS(app)

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

@app.route('/')
def index():
    return render_template('index.html', categories=list(data.keys()))

@app.route('/start_game', methods=['POST'])
def start_game():
    category = request.json.get('category')
    difficulty = request.json.get('difficulty')
    word = random.choice(data[category])
    session['word'] = word
    session['guesses_left'] = difficulty_guesses[difficulty]
    session['guessed_letters'] = []
    session['score'] = session.get('score', 0)
    return jsonify({'word_length': len(word), 'guesses_left': session['guesses_left'], 'score': session['score']})

@app.route('/guess', methods=['POST'])
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

@app.route('/get_state', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/hint', methods=['POST'])
def hint():
    word = session.get('word', '')
    session['score'] = 0
    session['guesses_left'] = 0
    session['guessed_letters'] = list(set(word))
    # Always reveal the answer and end the game as a loss
    return jsonify({'status': 'lose', 'word': word, 'score': session['score'], 'hint': word})
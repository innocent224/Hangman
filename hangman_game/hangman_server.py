from flask import Flask, render_template, request, jsonify, session
import random
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'hangman_secret_key'
CORS(app)

# Categories and words
data = {
    "Animals": [
        "ant", "antelope", "ape", "armadillo", "baboon", "badger", "bat", "bear", "beaver", "bison",
        "boar", "buffalo", "butterfly", "camel", "cat", "caterpillar", "cheetah", "chicken", "chimpanzee", "chinchilla",
        "cobra", "cougar", "cow", "coyote", "crab", "crocodile", "crow", "deer", "dog", "donkey",
        "dove", "duck", "eagle", "eel", "elephant", "falcon", "ferret", "fish", "flamingo", "fox",
        "frog", "gazelle", "gecko", "giraffe", "goat", "goose", "gorilla", "grasshopper", "guinea pig", "hamster",
        "hawk", "hedgehog", "heron", "hippopotamus", "horse", "hyena", "iguana", "jackal", "jaguar", "jellyfish",
        "kangaroo", "kingfisher", "kiwi", "koala", "komodo dragon", "lemur", "leopard", "lion", "lizard", "llama",
        "lobster", "lynx", "macaw", "magpie", "manatee", "meerkat", "mole", "monkey", "moose", "mosquito",
        "mouse", "mule", "narwhal", "newt", "octopus", "opossum", "orangutan", "ostrich", "otter", "owl",
        "ox", "panda", "panther", "parrot", "peacock", "pelican", "penguin", "pig", "pigeon", "platypus",
        "puma", "quail", "rabbit", "raccoon", "rat", "reindeer", "rooster", "salamander", "scorpion", "seal",
        "seahorse", "shark", "sheep", "shrimp", "skunk", "snail", "snake", "sparrow", "spider", "squid",
        "squirrel", "starfish", "stork", "swan", "tapir", "tarantula", "termite", "tiger", "toad", "tortoise",
        "turkey", "turtle", "vulture", "walrus", "wasp", "weasel", "whale", "wildcat", "wolf", "wombat",
        "woodpecker", "worm", "yak", "zebra", "ibis", "pangolin", "okapi", "oryx", "dugong", "porcupine",
        "gnat", "cicada", "locust", "sloth", "stoat", "weevil", "beetle", "centipede", "millipede", "dragonfly"
    ],
    "Fruits": [
        "apple", "apricot", "avocado", "banana", "blackberry", "blackcurrant", "blueberry", "boysenberry", "breadfruit", "cantaloupe",
        "cherry", "clementine", "cloudberry", "coconut", "cranberry", "currant", "custard apple", "date", "dragonfruit", "durian",
        "elderberry", "fig", "goji berry", "gooseberry", "grape", "grapefruit", "guava", "honeydew", "jackfruit", "jambul",
        "jujube", "kiwi", "kumquat", "lemon", "lime", "longan", "loquat", "lychee", "mandarin", "mango",
        "mangosteen", "melon", "mulberry", "nectarine", "olive", "orange", "papaya", "passionfruit", "peach", "pear",
        "persimmon", "pineapple", "plum", "pomegranate", "pomelo", "prickly pear", "quince", "raspberry", "redcurrant", "rhubarb",
        "salak", "sapodilla", "sapote", "satsuma", "starfruit", "strawberry", "surinam cherry", "tamarillo", "tamarind", "tangerine",
        "ugli fruit", "watermelon", "white currant", "yuzu", "ackee", "bilberry", "camu camu", "cactus pear", "carambola", "cherimoya",
        "feijoa", "finger lime", "gac fruit", "horned melon", "jabuticaba", "kei apple", "langsat", "mamoncillo", "medlar", "miracle fruit",
        "nashi pear", "pequi", "pitanga", "pulasan", "rambutan", "santol", "soursop", "sugar apple", "velvet apple", "wood apple",
        "abiu", "atemoya", "bignay", "calamansi", "chokeberry", "emblic", "grumichama", "imbe", "lucuma", "muntingia",
        "nance", "orangelo", "pitahaya", "safou", "saskatoon berry", "shipova", "white sapote", "yangmei", "ziziphus", "pluot"
    ],
    "Countries": [
        "afghanistan", "albania", "algeria", "andorra", "angola", "antigua and barbuda", "argentina", "armenia", "australia", "austria",
        "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bhutan",
        "bolivia", "bosnia and herzegovina", "botswana", "brazil", "brunei", "bulgaria", "burkina faso", "burundi", "cambodia", "cameroon",
        "canada", "cape verde", "central african republic", "chad", "chile", "china", "colombia", "comoros", "congo", "costa rica",
        "croatia", "cuba", "cyprus", "czech republic", "denmark", "djibouti", "dominica", "dominican republic", "ecuador", "egypt",
        "el salvador", "equatorial guinea", "eritrea", "estonia", "eswatini", "ethiopia", "fiji", "finland", "france", "gabon",
        "gambia", "georgia", "germany", "ghana", "greece", "grenada", "guatemala", "guinea", "guinea-bissau", "guyana",
        "haiti", "honduras", "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland", "israel",
        "italy", "ivory coast", "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati", "kosovo", "kuwait",
        "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho", "liberia", "libya", "liechtenstein", "lithuania", "luxembourg",
        "madagascar", "malawi", "malaysia", "maldives", "mali", "malta", "marshall islands", "mauritania", "mauritius", "mexico",
        "micronesia", "moldova", "monaco", "mongolia", "montenegro", "morocco", "mozambique", "myanmar", "namibia", "nauru",
        "nepal", "netherlands", "new zealand", "nicaragua", "niger", "nigeria", "north korea", "north macedonia", "norway", "oman",
        "pakistan", "palau", "panama", "papua new guinea", "paraguay", "peru", "philippines", "poland", "portugal", "qatar"
    ],
    "Sports": [
        "archery", "athletics", "badminton", "baseball", "basketball", "biathlon", "billiards", "bmx", "bobsleigh", "bodybuilding",
        "bowling", "boxing", "canoeing", "car racing", "cheerleading", "chess", "climbing", "cricket", "croquet", "curling",
        "cycling", "darts", "diving", "dragon boat racing", "equestrian", "fencing", "field hockey", "figure skating", "football", "formula 1",
        "freestyle skiing", "gaelic football", "golf", "gymnastics", "handball", "hang gliding", "heptathlon", "hockey", "horse racing", "ice hockey",
        "ice skating", "javelin", "judo", "karate", "kayaking", "kickboxing", "lacrosse", "luge", "marathon", "mixed martial arts",
        "modern pentathlon", "motocross", "mountain biking", "netball", "paddleboarding", "paintball", "paragliding", "parkour", "polo", "powerlifting",
        "racquetball", "rafting", "rhythmic gymnastics", "roller skating", "rowing", "rugby", "sailing", "sambo", "scuba diving", "shooting",
        "skateboarding", "skiing", "snowboarding", "soccer", "softball", "speed skating", "squash", "sumo wrestling", "surfing", "swimming",
        "synchronized swimming", "taekwondo", "tennis", "track and field", "trampoline", "triathlon", "tug of war", "ultimate frisbee", "volleyball", "water polo",
        "weightlifting", "windsurfing", "wrestling", "yoga as sport", "zorbing", "capoeira", "muay thai", "aikido", "kendo", "arm wrestling",
        "underwater hockey", "pickleball", "sepaktakraw", "snowshoeing", "inline skating", "sandboarding", "longboarding", "bouldering", "disc golf", "spearfishing"
    ]
}

# Difficulty settings
difficulty_guesses = {
    'easy': 10,
    'medium': 7,
    'hard': 5
}

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    """Serve the main game page with categories."""
    return render_template('index.html', categories=list(data.keys()))

@app.route('/start_game', methods=['POST'])
def start_game():
    """Start a new game with chosen category and difficulty."""
    category = request.json.get('category')
    difficulty = request.json.get('difficulty')

    if not category or not difficulty:
        return jsonify({'error': 'Category and difficulty required'}), 400

    word = random.choice(data[category])
    session['word'] = word
    session['guesses_left'] = difficulty_guesses.get(difficulty, 7)
    session['guessed_letters'] = []
    session['score'] = session.get('score', 0)

    return jsonify({
        'word_length': len(word),
        'guesses_left': session['guesses_left'],
        'score': session['score']
    })

@app.route('/guess', methods=['POST'])
def guess():
    """Handle a player's guess."""
    letter = request.json.get('letter', '').lower()

    if not letter or len(letter) != 1:
        return jsonify({'error': 'Invalid guess'}), 400

    word = session.get('word', '')
    guessed_letters = session.get('guessed_letters', [])

    # Already guessed
    if letter in guessed_letters:
        return jsonify({'status': 'already_guessed'})

    guessed_letters.append(letter)
    session['guessed_letters'] = guessed_letters

    # Correct guess
    if letter in word:
        if all(l in guessed_letters for l in word):
            session['score'] += 1
            return jsonify({'status': 'win', 'word': word, 'score': session['score']})
        else:
            return jsonify({'status': 'correct', 'guessed_letters': guessed_letters})

    # Incorrect guess
    session['guesses_left'] -= 1
    if session['guesses_left'] <= 0:
        session['score'] = 0
        return jsonify({'status': 'lose', 'word': word, 'score': session['score']})
    else:
        return jsonify({
            'status': 'incorrect',
            'guesses_left': session['guesses_left'],
            'guessed_letters': guessed_letters
        })

@app.route('/get_state', methods=['GET'])
def get_state():
    """Get the current state of the game."""
    word = session.get('word', '')
    guessed_letters = session.get('guessed_letters', [])
    display = [l if l in guessed_letters else '_' for l in word]

    return jsonify({
        'display': display,
        'guesses_left': session.get('guesses_left', 0),
        'guessed_letters': guessed_letters,
        'score': session.get('score', 0)
    })

@app.route('/hint', methods=['POST'])
def hint():
    """Reveal the word and end the game as a loss."""
    word = session.get('word', '')
    session['score'] = 0
    session['guesses_left'] = 0
    session['guessed_letters'] = list(set(word))

    return jsonify({
        'status': 'lose',
        'word': word,
        'score': session['score'],
        'hint': word
    })

# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
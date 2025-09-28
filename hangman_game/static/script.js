
let categories = [];

window.onload = function() {
    fetchCategories();
    document.getElementById('startBtn').onclick = startGame;
    document.getElementById('restartBtn').onclick = function() {
        // Hide game area, show menu
        document.getElementById('game').style.display = 'none';
        document.getElementById('menu').style.display = '';
        // Hide the button again
        document.getElementById('restartBtn').style.display = 'none';
        // Reset result, word, keyboard, hangman, fact, hint
        document.getElementById('result').textContent = '';
        document.getElementById('word').innerHTML = '';
        document.getElementById('keyboard').innerHTML = '';
        document.getElementById('hangman-drawing').innerHTML = '';
        document.getElementById('fact').textContent = '';
        document.getElementById('hintBtn').style.display = 'none';
    };
    updateHighScoreDisplay();
    document.getElementById('hintBtn').onclick = useHint;
};

function fetchCategories() {
    fetch('/')
        .then(() => {
            // Categories are rendered server-side, so just populate the select
            const catSelect = document.getElementById('category');
            catSelect.innerHTML = '';
            // These should match backend
            categories = ['Animals', 'Fruits', 'Countries', 'Sports'];
            categories.forEach(cat => {
                let opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                catSelect.appendChild(opt);
            });
        });
}

function startGame() {
    const category = document.getElementById('category').value;
    const difficulty = document.getElementById('difficulty').value;
    fetch('/start_game', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({category, difficulty})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('menu').style.display = 'none';
        document.getElementById('game').style.display = '';
        document.getElementById('score').textContent = 'Score: ' + data.score;
        document.getElementById('guessesLeft').textContent = data.guesses_left;
        document.getElementById('result').textContent = '';
        document.getElementById('result').className = 'progress';
        createWordDisplay(data.word_length);
        createKeyboard();
    document.getElementById('hintBtn').style.display = '';
    document.getElementById('hintBtn').disabled = false;
    });
}

function useHint() {
    document.getElementById('hintBtn').disabled = true;
    fetch('/hint', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'lose' && data.hint) {
            // Show the answer as a hint and end the game
            showResult('Hint: The answer is "' + data.hint.toUpperCase() + '". The word was: ' + data.word, false, data.score);
            playSound('lose');
            document.getElementById('hintBtn').disabled = true;
        } else if (data.status === 'hint') {
            updateState();
            document.getElementById('result').textContent = 'Hint: The letter "' + data.hint.toUpperCase() + '" has been revealed!';
            document.getElementById('hintBtn').disabled = false;
        } else if (data.status === 'win') {
            showResult('You Win! The word was: ' + data.word, true, data.score);
            playSound('win');
            document.getElementById('hintBtn').disabled = true;
        } else if (data.status === 'no_hint') {
            document.getElementById('result').textContent = 'No hints available!';
            document.getElementById('hintBtn').disabled = true;
        } else {
            document.getElementById('hintBtn').disabled = true;
        }
    });
}

function createWordDisplay(length) {
    const wordDiv = document.getElementById('word');
    wordDiv.innerHTML = '';

    for (let i = 0; i < length; i++) {
        let span = document.createElement('span');
        span.textContent = '_ ';
        span.className = 'letter';
        wordDiv.appendChild(span);
    }
}

function createKeyboard() {
    const keyboard = document.getElementById('keyboard');
    keyboard.innerHTML = '';
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let l of letters) {
        let btn = document.createElement('button');
        btn.textContent = l;
        btn.className = 'key';
        btn.onclick = () => guessLetter(l);
        keyboard.appendChild(btn);
    }
}

function guessLetter(letter) {
    playSound('click');
    fetch('/guess', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({letter})
    })
    .then(res => res.json())
    .then(data => {
        updateState();
        if (data.status === 'win') {
            showResult('You Win! The word was: ' + data.word, true, data.score);
            playSound('win');
        } else if (data.status === 'lose') {
            showResult('You Lose! The word was: ' + data.word, false, data.score);
            playSound('lose');
        } else if (data.status === 'already_guessed') {
            // Optionally show a message
        }
    });
    disableKey(letter);
}

function updateState() {
    fetch('/get_state')
        .then(res => res.json())
        .then(data => {
            const wordDiv = document.getElementById('word');
            wordDiv.innerHTML = '';
            data.display.forEach(l => {
                let span = document.createElement('span');
                span.textContent = l + ' ';
                span.className = 'letter';
                wordDiv.appendChild(span);
            });
            document.getElementById('guessesLeft').textContent = data.guesses_left;
            document.getElementById('score').textContent = 'Score: ' + data.score;
            drawHangman(data.guesses_left);
            // Color for progress
            document.getElementById('result').className = 'progress';
        });
}

// Draw a simple hangman using SVG based on guesses left
function drawHangman(guessesLeft) {
    const maxParts = 6; // base, pole, beam, rope, head, body+limbs
    const totalGuesses = 8; // max guesses for easy
    const wrongGuesses = totalGuesses - guessesLeft;
    let svg = '<svg width="120" height="120">';
    // base
    if (wrongGuesses > 0) svg += '<line x1="10" y1="110" x2="110" y2="110" stroke="#444" stroke-width="4" />';
    // pole
    if (wrongGuesses > 1) svg += '<line x1="30" y1="110" x2="30" y2="20" stroke="#444" stroke-width="4" />';
    // beam
    if (wrongGuesses > 2) svg += '<line x1="30" y1="20" x2="80" y2="20" stroke="#444" stroke-width="4" />';
    // rope
    if (wrongGuesses > 3) svg += '<line x1="80" y1="20" x2="80" y2="35" stroke="#444" stroke-width="3" />';
    // head
    if (wrongGuesses > 4) svg += '<circle cx="80" cy="45" r="10" stroke="#444" stroke-width="3" fill="none" />';
    // body
    if (wrongGuesses > 5) svg += '<line x1="80" y1="55" x2="80" y2="80" stroke="#444" stroke-width="3" />';
    // left arm
    if (wrongGuesses > 6) svg += '<line x1="80" y1="60" x2="70" y2="70" stroke="#444" stroke-width="3" />';
    // right arm
    if (wrongGuesses > 7) svg += '<line x1="80" y1="60" x2="90" y2="70" stroke="#444" stroke-width="3" />';
    // left leg
    if (wrongGuesses > 8) svg += '<line x1="80" y1="80" x2="70" y2="100" stroke="#444" stroke-width="3" />';
    // right leg
    if (wrongGuesses > 9) svg += '<line x1="80" y1="80" x2="90" y2="100" stroke="#444" stroke-width="3" />';
    svg += '</svg>';
    document.getElementById('hangman-drawing').innerHTML = svg;
}


function disableKey(letter) {
    const keys = document.getElementsByClassName('key');
    for (let btn of keys) {
        if (btn.textContent === letter) {
            btn.disabled = true;
            break;
        }
    }
}

const facts = [
    "Did you know? The longest English word without a true vowel is 'rhythms'.",
    "Keep going! Every mistake is a step closer to success.",
    "Fun fact: Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs!",
    "Motivation: Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Did you know? Octopuses have three hearts!",
    "Stay positive! Every letter guessed is progress.",
    "Fun fact: Bananas are berries, but strawberries aren't!",
    "Motivation: The only way to do great work is to love what you do.",
    "Did you know? The dot over the letters 'i' and 'j' is called a tittle.",
    "Keep it up! Learning never exhausts the mind."
];

function showResult(msg, win, score) {
    console.log('showResult called', msg, win, score);
    // Failsafe: always show the Play Again button and game area
    document.getElementById('restartBtn').style.display = 'block';
    document.getElementById('game').style.display = '';
    // Ensure the game area is visible so the restart button can be seen
    document.getElementById('game').style.display = '';
    // Show a custom message above the button
    let customMsg = '';
    if (win) {
        customMsg = '🎉 Congratulations! You won! Want to challenge yourself again?';
    } else {
        customMsg = '😢 Game over! Don\'t give up, try again!';
    }
    document.getElementById('result').innerHTML = customMsg + '<br>' + msg;
    document.getElementById('score').textContent = 'Score: ' + score;
    document.getElementById('restartBtn').style.display = 'block';
    document.getElementById('hintBtn').disabled = true;
    // Animate word reveal
    fetch('/get_state')
        .then(res => res.json())
        .then(data => {
            const wordDiv = document.getElementById('word');
            wordDiv.innerHTML = '';
            let word = msg.match(/The word was: (.+)$/);
            let revealWord = word ? word[1] : '';
            for (let i = 0; i < revealWord.length; i++) {
                let span = document.createElement('span');
                span.textContent = revealWord[i] + ' ';
                span.className = 'letter reveal';
                wordDiv.appendChild(span);
            }
        });
    // High score logic
    let highScore = parseInt(localStorage.getItem('hangmanHighScore') || '0');
    if (score > highScore) {
        highScore = score;
        localStorage.setItem('hangmanHighScore', highScore);
    }
    updateHighScoreDisplay();
    // Show a random fun fact or quote
    const factDiv = document.getElementById('fact');
    factDiv.textContent = facts[Math.floor(Math.random() * facts.length)];
    // Color for win/lose
    document.getElementById('result').className = win ? 'win' : 'lose';
    // Disable all keys
    const keys = document.getElementsByClassName('key');
    for (let btn of keys) btn.disabled = true;
}

function updateHighScoreDisplay() {
    let highScore = parseInt(localStorage.getItem('hangmanHighScore') || '0');
    document.getElementById('highscore').textContent = 'High Score: ' + highScore;
}

function playSound(type) {
    let sound;
    if (type === 'win') sound = document.getElementById('winSound');
    else if (type === 'lose') sound = document.getElementById('loseSound');
    else sound = document.getElementById('clickSound');
    if (sound) {
        sound.currentTime = 0;
        sound.play();
    }
}
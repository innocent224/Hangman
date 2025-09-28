document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('category');
    const difficultySelect = document.getElementById('difficulty');
    const startButton = document.getElementById('start-button');
    const guessInput = document.getElementById('guess-input');
    const guessButton = document.getElementById('guess-button');
    const hintButton = document.getElementById('hint-button');
    const displayWord = document.getElementById('display-word');
    const guessesLeft = document.getElementById('guesses-left');
    const guessedLetters = document.getElementById('guessed-letters');
    const scoreDisplay = document.getElementById('score');

    startButton.addEventListener('click', function() {
        const category = categorySelect.value;
        const difficulty = difficultySelect.value;
        fetch('/start_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category, difficulty })
        })
        .then(response => response.json())
        .then(data => {
            displayWord.textContent = '_ '.repeat(data.word_length);
            guessesLeft.textContent = data.guesses_left;
            guessedLetters.textContent = '';
            scoreDisplay.textContent = data.score;
        });
    });

    guessButton.addEventListener('click', function() {
        const letter = guessInput.value;
        fetch('/guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ letter })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'correct') {
                updateDisplay(data.guessed_letters);
            } else if (data.status === 'incorrect') {
                guessesLeft.textContent = data.guesses_left;
                updateDisplay(data.guessed_letters);
            } else if (data.status === 'already_guessed') {
                alert('You already guessed that letter!');
            } else if (data.status === 'win') {
                alert('Congratulations! You guessed the word: ' + data.word);
                resetGame();
            } else if (data.status === 'lose') {
                alert('Game over! The word was: ' + data.word);
                resetGame();
            }
        });
        guessInput.value = '';
    });

    hintButton.addEventListener('click', function() {
        fetch('/hint', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'hint') {
                updateDisplay(data.guessed_letters);
                guessesLeft.textContent = data.guesses_left;
            } else if (data.status === 'no_hint') {
                alert('No hints available!');
            } else if (data.status === 'lose') {
                alert('Game over! The word was: ' + data.word);
                resetGame();
            } else if (data.status === 'win') {
                alert('Congratulations! You guessed the word: ' + data.word);
                resetGame();
            }
        });
    });

    function updateDisplay(guessedLettersArray) {
        const word = displayWord.textContent.split(' ').join('');
        const display = word.split('').map(letter => 
            guessedLettersArray.includes(letter) ? letter : '_'
        ).join(' ');
        displayWord.textContent = display;
        guessedLetters.textContent = guessedLettersArray.join(', ');
    }

    function resetGame() {
        displayWord.textContent = '';
        guessesLeft.textContent = '';
        guessedLetters.textContent = '';
        scoreDisplay.textContent = '';
    }
});
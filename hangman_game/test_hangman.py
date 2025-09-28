import unittest
import json
from hangman_server import app

class HangmanAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_start_game(self):
        response = self.app.post('/start_game', json={
            'category': 'Animals',
            'difficulty': 'easy'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('word_length', data)
        self.assertEqual(data['guesses_left'], 8)

    def test_guess_correct_and_win(self):
        # Start a new game
        self.app.post('/start_game', json={
            'category': 'Animals',
            'difficulty': 'easy'
        })
        # Get the word from the session (simulate guessing all letters)
        with self.app.session_transaction() as sess:
            word = sess['word']
        for letter in set(word):
            response = self.app.post('/guess', json={'letter': letter})
        data = response.get_json()
        self.assertIn(data['status'], ['win', 'correct'])
        if data['status'] == 'win':
            self.assertEqual(data['word'], word)

    def test_guess_incorrect_and_lose(self):
        self.app.post('/start_game', json={
            'category': 'Animals',
            'difficulty': 'hard'
        })
        # Guess wrong letters
        wrong_letters = ['z', 'x', 'q', 'v']
        for letter in wrong_letters:
            response = self.app.post('/guess', json={'letter': letter})
        data = response.get_json()
        self.assertIn(data['status'], ['lose', 'incorrect'])
        if data['status'] == 'lose':
            self.assertIn('word', data)

    def test_get_state(self):
        self.app.post('/start_game', json={
            'category': 'Fruits',
            'difficulty': 'medium'
        })
        response = self.app.get('/get_state')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('display', data)
        self.assertIn('guesses_left', data)
        self.assertIn('score', data)

if __name__ == '__main__':
    unittest.main()
"""
It's just a sketch for hangman app, with using structured approach.
Based on chapter from book of Kurt Nørmarks "Object-oriented Programming in C# - for C and Java programmers"
https://people.cs.aau.dk/~normark/oop-csharp/html/notes/intro-oop_themes-from-structured-prog-to-oop-sect.html
"""

import os
import string
import random

MAX_WRONG_GUESSES = 3
PUZZLE_FILE = 'puzzles'


def main():
    player_name = get_player_name()
    init_game()
    is_start, again = True, False
    while is_start or again:
        is_start = False
        play_hangman(player_name)
        again = ask_user('Do you want to play again')
    os.unlink(PUZZLE_FILE)


def get_player_name():
    return input('What is your name?\n')


def init_game():
    puzzles = ['sequence', 'selection', 'repetition']
    print('\n'.join(puzzles))
    with open(PUZZLE_FILE, 'w') as fl:
        fl.write('\n'.join(puzzles))

    with open(PUZZLE_FILE, 'w') as fl:
        fl.write('\n'.join(puzzles))


def ask_user(question):
    answer = input(f'{question} [y/n]? ')
    return answer in {'yes', 'y'}


def play_hangman(player):
    state = {}
    init_state(player, state)
    puzzle = get_puzzle()

    while is_continues(state, puzzle):
        present_puzzle_outline(state, puzzle)
        present_remaining_alphabet(state)
        players_guess = get_users_guess()
        os.system('clear')
        update_game_state(state, puzzle, players_guess)
    present_result(won_or_lost(state, puzzle))


def is_continues(state, puzzle):
    return (state['wrong_guesses'] < MAX_WRONG_GUESSES and
            state['correct_guesses'] < puzzle['letters2guess'])


def update_game_state(state, puzzle, players_guess):
    if players_guess not in puzzle['word']:
        state['wrong_guesses'] += 1
    else:
        state['correct_guesses'] += 1
    state['remaining_letters'].remove(players_guess)


def won_or_lost(state, puzzle):
    return bool(set(puzzle['word']) - set(state['remaining_letters']))


def present_result(won_game):
    print('You are won' if won_game else 'You are lose')


def present_puzzle_outline(state, puzzle):
    puzzle_word = puzzle['word']
    for letter in puzzle_word:
        if letter in state['remaining_letters']:
            puzzle_word = puzzle_word.replace(letter, '*')
    print(puzzle_word)


def present_remaining_alphabet(state):
    print(' '.join(state['remaining_letters']))


def get_users_guess():
    return input('Input letter: ')


def init_state(player, state):
    state['player'] = player
    state['wrong_guesses'] = 0
    state['correct_guesses'] = 0
    state['remaining_letters'] = list(string.ascii_lowercase)
    os.system('clear')


def get_puzzle():
    with open(PUZZLE_FILE) as puzzle_file:
        puzzles = puzzle_file.readlines()
    puzzle = random.choice(puzzles).strip()
    return {'word': puzzle, 'letters2guess': len(set(puzzle))}


if __name__ == '__main__':
    main()

# Wordle game for Python CLI

import random


def get_secret_word() -> str:
    """Chooses a secret 5-letter word randomly from options"""
    words: list = ["hello", "claim", "crane", "snail", "peach", "brown"]
    return random.choice(words)

def get_word_hint(secret: str, guess: str) -> str:
    """Checks guess against correct word and returns a string get_word_hint"""
    hint: str = ""
    for char in range(len(guess)):
        if guess[char] == secret[char]:
            hint = hint + "🟩"
        elif guess[char] in secret:
            # Only add a yellow once per instance of letter in secret word
            if guess[0:char].count(guess[char]) < secret.count(guess[char]):
                hint = hint + "🟨"
            else:
                hint = hint + "🟥"
        else:
            hint = hint + "🟥"
    return hint

def main():
    secret_word: str = get_secret_word()
    guess_word: str = ""
    count: int = 0
    guessed: bool = False

    while not guessed and count < 6:
        while len(guess_word) != 5:
            guess_word = input("Enter your guess: ")
        result: str = get_word_hint(secret_word, guess_word)
        print("\t" + result)
        if result == "🟩🟩🟩🟩🟩":
            guessed = True
        else:
            count += 1
            guess_word = ""

    if guessed == True:
        print("Congrats!")
    else:
        print(f"The word was \"{secret_word}\", better luck next time")

if __name__ == "__main__":
    main()

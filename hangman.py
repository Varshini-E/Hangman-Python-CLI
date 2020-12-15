import random
import sqlite3

def get_word():
    conn = sqlite3.connect("hangman_words.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT * FROM words_list ORDER BY RANDOM() LIMIT 1;")
    rows = cur.fetchall()
    word=""
    for row in rows:
        word=row[0]
    return word.upper()

def play_hangman(word):

    curr_word = '_' * len(word)
    guessed_letters = []
    guessed_words = []
    tries = 8
    guessed = False

    print("\nLet's play Hangman!")
    print(display_hangman(tries))
    for letter in curr_word:
        print(letter,"",end="")
    print("\n")

    #looping as long as word is not fully guessed or tries are available
    while not guessed and tries>0:
        guess = input("Guess a letter or a word: ")
        guess = guess.upper()

        if len(guess)==1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter ",guess)
            elif guess not in word:
                print("Sorry! The letter ",guess,"is not in the word")
                tries-=1
                guessed_letters.append(guess)
            else:
                print("Yay! The letter ",guess,"is in the word")
                guessed_letters.append(guess)

                word_as_list = list(curr_word)
                for i,letter in enumerate(word):
                    if letter==guess:
                        word_as_list[i]=guess

                curr_word="".join(word_as_list)
                if "_" not in curr_word:
                    guessed = True
        elif len(guess)==len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word ",guess)
            elif guess!=word:
                print("Sorry! The word is not ",guess,".")
                tries-=1
                guessed_words.append()
            else:
                guessed = True
                curr_word = word
        else:
            print("Not a valid guess")

        print(display_hangman(tries))
        for letter in curr_word:
            print(letter,"",end="")
        print("\n\nNumber of incorrect attempts left: ",tries)
        print("\n\n")

    if guessed is True:
        print("Congrats! You guessed the word!")
    else:
        print("You ran out of tries! The word is",word,". Try again next time!")

def display_hangman(tries):
    stages = [  # final state: done
                """
                   --------
                   |      |
                   |      X
                   |     \\|/
                   |      |
                   |     / \\
                   |
                   |
                   -
                """,
                # pre-final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   |
                   |
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     /
                   |
                   |
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |
                   |
                   |
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |
                   |
                   |
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |
                   |
                   |
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |
                   |
                   |
                   |
                   |
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |
                   |
                   |
                   |
                   |
                   |
                   -
                """,
                # initial without any rope
                """
                   --------
                   |
                   |
                   |
                   |
                   |
                   |
                   |
                   -
                """
    ]
    return stages[tries]

def main():
    word = get_word()
    play_hangman(word)

    while input("\nPlay Again? (Y/N): ").upper() == 'Y':
        print("\n")
        word = get_word()
        play_hangman(word)

if __name__ == '__main__':
    main()

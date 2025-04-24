#!/usr/bin/env python3
import random
import os # clear terminal

words = [
    "abroad",
    "absence",
    "absolute",
    "absolutely",
    "absorb",
    "abuse",
    "academic",
    "accept",
    "access",
    "accident",
]


def validate_input(input_char, tried):
    # dummy check
    char = input_char.lower()
    if len(char) != 1:
        return (False, tried)
    if char in tried:
        return (False, tried)
    tried.update(char)
    return (True, tried)


def replace_placeholder(char, word, placeholder):
    new_placeholder = placeholder
    for i in range(len(word)):
        if word[i] == char:
            new_placeholder[i] = char
    return new_placeholder


def check_char_in_word(tries, char, word, placeholder):
    if char in word:
        placeholder = replace_placeholder(char, word, placeholder)
        return (tries, placeholder)
    else:
        tries -= 1
        return (tries, placeholder)


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    word = random.choice(words) # word to guess
    print(word)
    tried = set() # tried characters
    tries = 6 # total number of tries
    placeholder = ["_" for i in range(len(word))] # display placeholder
    while tries > 0:
        print("".join(placeholder))
        print(f"Please enter a character, you have {tries} tries left")
        char = input().lower()
        state, tried = validate_input(char, tried)
        if not state:
            # this does not call the clear method
            print("Your input is invalid, please check and enter again")
            print("Note: you cannot enter a previously entered character")
            continue
        tries, placeholder = check_char_in_word(tries, char, word, placeholder)
        if "_" not in placeholder:
            print(f"You won! The word is {word}")
            return
        clear_terminal()
        # word check
    print(f"You failed! The word is {word}")

if __name__ == "__main__":
    main()

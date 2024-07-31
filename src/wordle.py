import json
import math

def load_word_list(filename):
    # Load a list of 5-letter words from a file.
    with open(filename, 'r') as file:
        words = [line.strip().lower() for line in file if len(line.strip()) == 5]
    return words

def filter_words(input_list, feedback, current_guess):
    # Filter words based on feedback for each letter and position.
    output = input_list
    for i, f in enumerate(feedback):
        if f == 'g':
            output = [word for word in output if word[i] == current_guess[i]]
        elif f == 'y':
            output = [word for word in output if current_guess[i] in word and word[i] != current_guess[i]]
        elif f == 'b':
            output = [word for word in output if current_guess[i] not in word or current_guess.count(current_guess[i]) > word.count(current_guess[i])]
    return output

def get_feedback():
    # Get feedback from the user.
    while True:
        feed = input("Feedback: (g/y/b) ")
        if len(feed) == 5 and all(c in 'gyb' for c in feed):
            return feed
        print("Error! Feedback must include only g/y/b and must be 5 letters long.")

def find_best_guess(possible, data):
    # Find the best guess based on frequency map.
    max_value = float('-inf')
    best_guess = None
    for word in possible:
        if data.get(word, 0) > max_value:
            max_value = data[word]
            best_guess = word
    return best_guess

def wordle_solver():
    # Main function to solve Wordle.
    # Load word lists and frequency map
    possible = load_word_list('data/allowed_words.txt')
    guess = ["crane"]
    
    with open('data/freq_map.json', 'r') as file:
        data = json.load(file)
    
    result = False
    guess_number = 0
    
    while not result:
        current_guess = guess[guess_number]
        print("Guess:", current_guess)
        
        feedback = get_feedback()
        
        if feedback == "ggggg":
            print("Wordle solved.")
            result = True
        else:
            possible = filter_words(possible, feedback, current_guess)
        
        next_guess = find_best_guess(possible, data)
        guess.append(next_guess)
        guess_number += 1

if __name__ == "__main__":
    wordle_solver()
    

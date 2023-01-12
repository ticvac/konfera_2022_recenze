from nltk.tokenize import word_tokenize
import math
import json

def tokenize(data):
    data = data.replace("<br />", " ")
    data = data.lower()
    punctuation = ['"', "!", "?", ".", ",", ":", ";", "(", ")", "[", "]", "{", "}", "_", "/", "\\", "|", ">", "<", "=", "+", "*", "&", "^", "%", "$", "#", "@", "~"]
    data = data.translate(str.maketrans({character: " " for character in punctuation}))
    return  word_tokenize(data)

def guess_rating(rewiew):

    words_in_text = tokenize(rewiew)
    words_in_text = set(words_in_text)

    total_rating = 0
    total_words = 0

    for w in words_in_text:
        word_rating = words_pos_probability.get(w, 0.5)
        if abs(word_rating - 0.5) > 0.0:
            total_rating += (math.tanh(4*(word_rating - 0.5)) + 1 ) / 2
            total_words += 1
    if total_words == 0:
        return 0.5
    print(total_rating / total_words)
    return round(total_rating / total_words)
    

rewiewBad = "Really bad film was making me sick, never watching this shit again, best"
rewiewGreat = ""

with open('data.json', 'r') as file:
    words_pos_probability = json.load(file)

while True:
    rewiew = input("write: ")
    rating = guess_rating(rewiew)
    print("positive" if rating==1 else "negative")
    print("---")
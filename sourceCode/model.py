from datasets import load_dataset
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import math
import string
import json
import nltk

dataset = load_dataset("imdb")
dataset = dataset.shuffle(seed=0)

words_count_pos = defaultdict(int)
words_count_neg = defaultdict(int)
words_count_total = defaultdict(int)
words_pos_probability = defaultdict(float)

def tokenize(data):
    data = data.replace("<br />", " ")
    data = data.lower()
    punctuation = ['"', "!", "?", ".", ",", ":", ";", "(", ")", "[", "]", "{", "}", "_", "/", "\\", "|", ">", "<", "=", "+", "*", "&", "^", "%", "$", "#", "@", "~"]
    data = data.translate(str.maketrans({character: " " for character in punctuation}))
    
    return word_tokenize(data)

# TRAIN
for i in range(0, len(dataset["train"])):
    rewiew = dataset["train"][i]
    words_in_text = tokenize(rewiew["text"])
    words_in_text = set(words_in_text)

    for w in words_in_text:
        words_count_total[w] += 1
        if rewiew["label"] == 0:
            words_count_neg[w] += 1
        else:
            words_count_pos[w] += 1
            
        
# for w in words_count_pos:
#     if words_count_neg[w] < 10 and words_count_pos[w] > 10:
#         print(w)

#calculate words_pos_probability
for w in words_count_total:
    if words_count_total[w] > 0:
        #words_pos_probability[w] = words_count_pos[w] / words_count_total[w]
        pb = words_count_total[w] / len(dataset["train"])
        pa = 0.5
        pba = words_count_pos[w] / (len(dataset["train"]) * pa)
        words_pos_probability[w] = pba * pa / pb

# CATEGORISE (unused)
negative, positive = [], []
for w in words_count_pos:
    if words_pos_probability[w] > 0.8 and words_count_pos[w] > 50:
        positive.append(w)
        
    if words_pos_probability[w] < 0.2 and words_count_neg[w] > 50:
        negative.append(w)

# REMOVE STOPWORDS
for stopword in stopwords.words('english'):
    try:
        del(words_count_total[stopword])
        del(words_count_neg[stopword])
        del(words_count_pos[stopword])
        del(words_pos_probability[stopword])
    except KeyError:
        pass

print(words_count_total)

#print("POSITIVE\n",positive)
#print("\n\nNEGATIVE\n", negative)

#print(sorted(words_pos_probability.items(), key=lambda x: x[1]))

#print(words_count_total['yokai'])


def guess_rating(rewiew):
    words_in_text = tokenize(rewiew)
    words_in_text = set(words_in_text)

    total_rating = 0
    total_words = 0

    idkcotonzvat = 0.5 #(pa)

    for w in words_in_text:
        word_rating = words_pos_probability.get(w, 0.5)

        if abs(word_rating - 0.5) > 0.1 and words_count_total.get(w, 0) > 0:
            # (math.sin(word_rating * math.pi - 0.5*math.pi) + 1 ) / 2
            total_rating += (math.tanh(4*(word_rating - 0.5)) + 1 ) / 2
            # (1.6 * (word_rating - 0.5))**3 +0.5   --- spatne
            # total_rating += word_rating * ((words_count_total[w]**0.1) * abs(word_rating - 0.5))
            # total_words += (words_count_total[w]**0.1) * abs(word_rating - 0.5)

            total_words += 1      

            # pb = words_count_total[w] / len(dataset["train"])
            # pa = 0.5
            # pba = words_count_pos[w] / (len(dataset["train"]) * pa)
            
            # if (pba / pb) > 1:
            #     print("DEBUG")
            #     print(pba)
            #     print(pb)
            #     print(words_count_total[w])
            #     print(words_count_pos[w])
            #     print(w)
            #     print("--------")

            #idkcotonzvat *= pba / pb
        
    if total_words == 0:
        #print("no words found")
        return 0
    
    #print(idkcotonzvat)
    return round(total_rating / total_words)
    return round(idkcotonzvat)

# TEST
TrainSetError = 0
testDataLenght = 25000
for i in range(5000, testDataLenght):
    rating = guess_rating(dataset["test"][i]["text"])
    if rating != dataset["test"][i]["label"]:
        TrainSetError += 1

print("error:")
print(TrainSetError / 20000)
print("correctness:")
print(1-(TrainSetError / 20000))

# POSITIVE
#  ['excellent', 'Highly', 'beautifully', 'wonderfully', 'Sullivan', 'hit-man', 'conveys', 'friendship', 'perfection', 'haunting', 'Carla', 'Von', 'wonderful', 'delight', 'Bourne', 'superb', 'brilliantly', 'amazing', 'gritty', 'Powell', 'Ruby', 'Shanghai', 'September', '10/10', 'Chavez', 'Mol', 'Paula', 'soccer', 'outstanding', 'Victoria', 'noir', '7/10', 'Christy', 'unforgettable', 'timeless', 'Cowboy', 'Ratso', 'Voight', 'captures', 'terrific', 'Polanski', 'Edie', 'gripping', 'Gilliam', 'Truman', 'Dressed', 'Palma', 'Ramones', 'tremendous', 'delicate', 'heartwarming', 'delightful', 'fantastic', 'must-see', 'finest', 'underrated', 'refreshing', 'Purple', 'Nancy', 'heartfelt', 'extraordinary', 'marvelous', '8/10', 'Dirty', 'MacArthur', 'Through', 'Wonderful', 'Bakshi', 'Gandhi', 'mesmerizing', 'Kline', 'Biko', 'captivating', 'heartbreaking', 'stark', 'Gerard', 'superbly', 'flawless', 'layers', 'Gundam', 'Wing', 'Wang', 'sons', 'Antwone', 'portrait', 'Fisher', 'Stanwyck', 'Corbett', 'Flynn', 'Chamberlain', 'Carell', 'Mann', 'favorites', 'excellently', 'sadness', 'Watson', 'Welles', 'darker', 'Othello', 'touching', 'Harriet', 'Andrews', 'Tierney', 'Excellent', 'Sox', 'Iran', 'Darren', 'Sidney', 'Lumet', 'Masterson', 'Hawke', 'Lily', 'Hyde', 'Recommended', 'McLaglen', 'Ruth', 'Enjoy', 'breathtaking', 'Raines', 'Lincoln', '1945', 'Jackie', 'Chan', 'Grayson', 'Always', 'freedom', 'Bud', 'Malone', '9/10', 'Burns', 'Fontaine', 'Nathan', 'Alvin', 'magnificent', 'Lemmon', 'Homer', 'Hidden', 'Sinatra', 'Simmons', 'Dickens', 'Scrooge', 'Stewart', 'McCoy', 'Fuller', 'exceptional', 'Widmark', 'Peters', 'Ritter', 'splendid', 'Paulie', 'pleasantly', 'Davies', 'Andre', 'poignant', 'Reeve', 'Actress', 'Kidman', 'Hartley', 'Marie', 'masterful', 'affection', 'gem', 'gentle', 'Visconti', 'Season', 'Stargate', 'Novak', 'cleverly', 'Matthau', 'Einstein', 'Brosnan', 'Spock', 'Macy', 'Liu', 'astonishing', 'understated', 'Sabrina', 'chilling', 'Felix', 'Kazan', 'Pickford', 'Kolchak', 'Capote', 'Georges', 'Trier', 'Winchester', 'Kinnear', 'Braveheart', 'elegant', 'chess', 'top-notch', 'Iturbi', 'Castle', 'Early', 'Nina', 'uplifting', 'Astaire', 'Walsh', 'Fido', 'Gypo', 'tender', '9/11', 'Goldsworthy', 'Montana', 'Hayworth', 'Elvira', 'Sirk', 'Sopranos', 'Heart', 'Steele', 'Gunga', 'Din', 'Kurosawa', 'Rukh', 'Stack', 'Miyazaki', 'Technicolor', 'explores', 'Dixon', 'Cheadle', 'Mildred', 'Deanna', 'Blunt', 'Mathieu', 'Vance', 'Kitty', 'Cypher']
# NEGATIVE
#  ['worst', 'boring', 'stupid', 'stupidity', 'lame', 'muddled', 'costs', 'terrible', 'junk', 'uninteresting', 'non-existent', 'worse', 'crap', 'Rambo', 'miserably', 'redeeming', 'mess', 'bother', 'insult', 'ashamed', 'dull', 'ridiculously', 'idiotic', 'ridiculous', 'wasting', 'zero', 'pathetic', 'horrible', '0', 'excuse', 'badly', 'embarrassed', 'dumb', 'vampires', 'waste', 'dreadful', 'incomprehensible', 'worthless', 'camcorder', 'Seriously', 'Gore', 'cardboard', 'nonsensical', 'atrocious', 'downhill', 'unimaginative', 'plastic', 'forgettable', 'topless', 'dude', 'shark', 'wasted', 'tedious', 'F', 'inane', 'WTF', 'Unless', 'whatsoever', 'Attack', 'unoriginal', 'pile', 'poorly', 'garbage', 'horribly', 'lousy', 'Worst', 'Godzilla', 'suck', 'appalling', 'Gray', 'rubber', 'awful', 'ripped', 'lackluster', 'Claus', 'remotely', 'sucks', 'dire', 'WORST', 'laughable', 'crappy', 'dinosaur', 'Simpson', 'rubbish', 'Zombies', 'idiots', 'wooden', '<', 'amateurish', 'embarrassment', 'dreck', 'Alone', 'tripe', 'unlikeable', 'Awful', 'hideous', 'BAD', 'embarrassing', 'flop', 'obnoxious', 'turkey', 'Omen', 'incompetent', 'tasteless', 'pointless', 'unbelievably', 'insulting', 'Rangers', 'Worse', 'Ariel', 'Plan', 'unconvincing', 'lifeless', 'moronic', 'NO', 'barrel', 'dud', 'Lundgren', 'horrid', 'Fulci', 'tiresome', 'inept', 'stinks', 'abysmal', 'horrendous', 'hackneyed', 'fest', 'Timberlake', '3/10', 'alright', '4/10', 'Boring', '2/10', 'Carlito', '1/10', 'rip-off', 'useless', 'porno', 'shoddy', 'werewolf', 'Naschy', 'Save', 'boredom', 'unfunny', 'stinker', 'blah', 'whale', 'Springer', 'NOTHING', 'Scary', 'uninspired', 'Uwe', 'Boll', 'laughably', 'Terrible', 'Horrible', 'pitiful', 'drivel', 'sub-par', 'unwatchable', 'Seed', 'Arquette', 'flimsy', 'wretched', 'unintentional', 'Damme', 'Baldwin', 'Stupid', 'Prom', 'Seagal', 'MST3K', 'insipid', 'Gamera', 'incoherent', 'Avoid', 'crocodile', 'Beowulf', 'Dahmer', 'Gadget', 'Thunderbirds']
# 0.18904
# 0.81096


# 2 pokus (lowercase)
# error:
# 0.18868
# correctness:
# 0.81132

# 3 pokus - zahozeni neutralnich slov 20%
# error:
# 0.17
# correctness:
# 0.83
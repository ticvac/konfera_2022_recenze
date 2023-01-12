from collections import defaultdict
import json

counts = defaultdict(int)

with open('count.json', 'r') as file:
    counts = json.load(file)

while True:
    print(counts.get(input("enter word: "), "0"))
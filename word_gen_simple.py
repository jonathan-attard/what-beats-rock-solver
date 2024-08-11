import random

import requests


class WordGenerator:
    def __init__(self, initial_list=None):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        self.WORDS = response.content.splitlines()
        self.initial_list = initial_list

    def get_word(self):
        while True:
            w = random.choice(self.WORDS)
            w = w.decode('utf-8')

            if w in self.initial_list:
                continue

            return w

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.WORDS[item]

    def reset(self):
        pass


if __name__ == "__main__":
    wg = WordGenerator()
    word = wg.get_word()
    print(word)

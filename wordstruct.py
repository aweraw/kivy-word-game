from collections import defaultdict
from random import sample
from itertools import combinations


def rdict():
    return defaultdict(rdict)


class WordStruct(object):

    def __init__(self, fh):
        self.wdict = rdict()
        self.wset = set()
        for line in fh:
            word = line.strip()
            self.wset.add(word.lower())
            d = self.get_substruct(word)
            if 'words' in d:
                d['words'].append(word)
            else:
                d['words'] = [word]

    def get_substruct(self, word):
        d = self.wdict
        for c in self.key(word):
            d = d[c]
        return d

    def key(self, word):
        return sorted(word.lower())

    def collect(self, word):
        d = self.wdict
        words = list()
        for c in self.key(word):
            d = d[c]
            if 'words' in d:
                words.extend(d['words'])
        return words

    def make_grid_game(self, seed_word=None, alpha_word_len=9):
        if (seed_word and len(seed_word) > 9) or alpha_word_len > 9:
            raise ValueError("Maximum len(seed_word) and alpha_word_len value is 9")
        if seed_word:
            parent = seed_word
        else:
            parent = sample(tuple(w for w in self.wset if len(w) == alpha_word_len), 1)[0]

        if len(parent) < 9:
            # create a set of candidate characters to take number up to 9,
            # culling characters from parent word
            candidates = set("abcdefghijklmnopqrstuvwxyz")
            parent_chars = set(parent)
            candidates.difference_update(parent_chars)
            remaining = 9 - len(parent)
            winners = sample(candidates, remaining)
            parent += ''.join(winners)

        # choose which letter will be in the centre, no vowels or cruddy letters
        centre_char = sample([c for c in parent if c not in "aeiouxyzqjk"], 1)[0]
        # create a list for the letter that will surround the centre
        rest = list(parent)
        rest.remove(centre_char)
        # collect all the words in our dictionary
        words = self.collect(parent)
        for i in range(3, 8):
            for k in (centre_char+''.join(x) for x in combinations(rest, i)):
                words.extend(self.collect(k))

        # cull words that do not contain the centre character, and sort the rest
        usable_words = sorted(set(w for w in words if centre_char in w), key=lambda x: (len(x), x))

        return centre_char, parent, usable_words

if __name__ == '__main__':
    ws = WordStruct(open('words.txt'))
    print(ws.make_grid_game())
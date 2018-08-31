from random import shuffle

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    NumericProperty, ObjectProperty, BooleanProperty,
    DictProperty, StringProperty)
from kivy.clock import Clock
from kivy.core.window import Window

from wordstruct import WordStruct
from grid import GameGrid, GridCell
from word_row import WordRow, WordCell
from labels import DynamicLabel, Timer
from found_area import FoundArea, FoundLabel
from constants import letter_vals, green, red

Window.size = (480, 800)


class WordGame(FloatLayout):
    # UI objects
    grid = ObjectProperty(None)
    word_row = ObjectProperty(None)
    progress = ObjectProperty(None)
    timer = ObjectProperty(None)
    found_area = ObjectProperty(None)

    # Game objects
    word_struct = ObjectProperty(None)
    words_remaining = ObjectProperty(None)
    words_found = DictProperty(None)
    words_total = NumericProperty(0)
    words_found_n = NumericProperty(0)
    score = NumericProperty(0)

    # State flags
    flashing = BooleanProperty(False)

    def update(self, dt):
        match = self.check_match()
        if match:
            self.word_row.flash(reset=True)

        self.timer.update_time(dt)

    def init(self):
        if not self.word_struct:
            with open('words.txt') as word_list:
                self.word_struct = WordStruct(word_list)

        middle, grid_seed, words = self.word_struct.make_grid_game()

        grid_seed = list(grid_seed)
        grid_seed.remove(middle)
        shuffle(grid_seed)
        grid_seed = ''.join(grid_seed)
        grid_seed = grid_seed[:4] + middle + grid_seed[4:]
        self.grid.set_chars(grid_seed.upper())

        self.words_remaining = set(words)
        self.words_total = len(self.words_remaining)
        self.words_found.clear()

    def check_match(self):
        word = self.word_row.string_value()

        if word in self.words_remaining:
            fl = self.found_area.add_word(word)
            self.words_found[word] = fl
            self.words_found_n += 1
            self.words_remaining.remove(word)
            self.score += self.score_word(word)
            return word
        elif (word in self.words_found and not self.flashing and
                not self.word_row.highlit):
            self.word_row.highlit = True
            self.word_row.set_color(red)
            self.found_area.highlight_label(self.words_found[word])
        # we're already red, but adding an extra character finds
        # another already found word
        elif (word in self.words_found and
                word != self.found_area.highlit_text() and
                self.word_row.highlit):
            self.word_row.set_color(red)
            self.found_area.lowlight_label()
            self.found_area.highlight_label(self.words_found[word])
        # it's probably not a word, so turn green again
        elif (word not in self.words_found and
                not self.flashing and self.word_row.highlit):
            self.word_row.highlit = False
            self.word_row.set_color(green)
            self.found_area.lowlight_label()

        return None

    def score_word(self, word):
        score = 0
        ln = len(word)
        for c in word:
            score += letter_vals[c] * ln
        return score


class WordApp(App):
    def build(self):
        game = WordGame()
        game.init()
        game.word_row.bind(pos=game.word_row.realign_cells)
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    WordApp().run()

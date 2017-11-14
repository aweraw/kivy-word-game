__author__ = 'aidan'

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty, ObjectProperty

from constants import white, black, grey, yellow


class Cell(Button):

    def set_char(self, c):
        self.text = c


class GridCell(Cell):
    used = BooleanProperty(False)
    is_middle = BooleanProperty(False)
    word_ref = ObjectProperty(None)

    def on_press(self):
        if not self.used:
            self.background_color = white
            self.color = black

    def on_release(self):
        if not self.used:
            self.background_color = grey
            self.send_char()
            self.used = True
        else:
            self.parent.undo_char(self.word_ref)

    def reset(self):
        self.background_color = black
        if self.is_middle:
            self.color = (1, 1, 0, 1)
        else:
            self.color = white
        self.used = False

    def send_char(self):
        self.parent.send_char(self)


class GameGrid(GridLayout):

    def send_char(self, cell):
        self.parent.word_row.set_char(cell)

    def undo_char(self, cell):
        cell.disappear()

    def set_chars(self, chars):
        for c, cell in zip(chars, self.children):
            cell.set_char(c)

        middle = self.children[4]
        middle.color = yellow
        middle.is_middle = True

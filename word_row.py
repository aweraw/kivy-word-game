__author__ = 'aidan'

from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation

from grid import Cell
from constants import green, blue, black, white


class WordCell(Cell):
    index = NumericProperty(0)
    grid_ref = ObjectProperty(None)

    def on_press(self):
        self.background_color = blue

    def on_release(self):
        self.background_color = green
        self.disappear()

    def shift_left(self, n=1):
        anim = Animation(x=self.x - ((self.width / 2) * n), duration=0.1)
        anim.start(self)
        return anim

    def shift_right(self, n=1):
        anim = Animation(x=self.x + ((self.width / 2) * n), duration=0.1)
        anim.start(self)
        return anim

    def appear(self):
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self)
        anim.bind(on_complete=self.realign)
        return anim

    def disappear(self):
        anim = Animation(opacity=0, duration=0.05)
        anim.bind(on_complete=self.remove)
        anim.start(self)
        return anim

    def remove(self, anim=None, widget=None):
        if self.parent:
            self.realign()
            self.parent.remove_cell(self)

    def realign(self, anim=None, widget=None):
        if self.parent:
            self.parent.realign_cells(self, self.parent.pos)


class WordRow(FloatLayout):

    highlit = BooleanProperty(False)

    def set_char(self, char):
        cell = WordCell()
        cell.set_char(char.text.lower())
        cell.grid_ref = char
        char.word_ref = cell
        cell.index = len(self.children)
        cell.background_color = green
        cell.opacity = 0
        cell.size = self.height, self.height
        for child in self.children:
            child.shift_left()
        cell.y = self.y
        if cell.index == 0:
            cell.center_x = self.center_x
        else:
            cell.x = self.center_x + (cell.width / 2) * (len(self.children)-1)
        self.add_widget(cell)
        cell.appear()

    def remove_cell(self, cell, animate=True):
        cell.grid_ref.reset()
        if animate:
            cell.background_color = black
            for c in (x for x in self.children if x.index < cell.index):
                c.shift_right()
            for c in (x for x in self.children if x.index > cell.index):
                c.shift_left()
                c.index -= 1
        self.remove_widget(cell)

    def reset(self, anim=None, widget=None):
        for cell in self.children[:]:
            self.remove_cell(cell, animate=False)
        self.stop_flashing()

    def stop_flashing(self):
        self.parent.flashing = False

    def flash(self, reset=False):
        self.parent.flashing = True
        self.set_color(green)
        anim = Animation(background_color=white, duration=0.1) + \
            Animation(background_color=black, duration=0.05) + \
            Animation(background_color=white, duration=0.05)
        if reset:
            anim.bind(on_complete=self.reset)
        else:
            anim.bind(on_complete=self.stop_flashing)

        for cell in self.children:
            anim.start(cell)

    def set_color(self, color):
        for cell in self.children:
            cell.background_color = color

    def realign_cells(self, ins, val):
        x, y = val
        offset = x + (self.height / 2) * (9 - len(self.children))
        for cell in self.children:
            cell.size = self.height, self.height
            cell.y = y
            cell.x = offset + (cell.width * cell.index)

    def string_value(self):
        return ''.join(c.text for c in self.children)[::-1]

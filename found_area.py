__author__ = 'aidan'

from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.animation import Animation

from constants import red, white


class FoundLabel(Label):
    pulsing = BooleanProperty(False)

    def set_text(self, text):
        self.text = text

    def highlight(self):
        anim = Animation(color=red, duration=0.2)
        anim.start(self)

    def lowlight(self):
        anim = Animation(color=white, duration=0.2)
        anim.start(self)


class FoundArea(StackLayout):
    highlit = ObjectProperty(None)

    def add_word(self, word):
        fl = FoundLabel()
        fl.set_text(word)
        self.add_widget(fl)
        return fl

    def highlight_label(self, label):
        self.highlit = label
        label.highlight()

    def lowlight_label(self):
        if self.highlit:
            self.highlit.lowlight()

    def highlit_text(self):
        if self.highlit:
            return self.highlit.text
        else:
            return ""

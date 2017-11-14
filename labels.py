__author__ = 'aidan'

from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty


class DynamicLabel(Label):
    def on_texture_size(self, ins, val):
        self.size = val


class Timer(DynamicLabel):
    time = NumericProperty(0.0)
    time_str = StringProperty("0s")

    def update_time(self, dt):
        self.time += dt
        self.time_str = self.format_time()

    def format_time(self):
        minutes, seconds = divmod(self.time, 60)
        hours, minutes = divmod(minutes, 60)
        t_dict = {"seconds": seconds, "minutes": int(minutes), "hours": int(hours)}
        s_fmt = "{seconds:.1f}s"
        m_fmt = "{minutes}m"
        h_fmt = "{hours}h"
        if hours:
            fmt_string = " ".join((h_fmt, m_fmt, s_fmt))
        elif minutes:
            fmt_string = " ".join((m_fmt, s_fmt))
        else:
            fmt_string = s_fmt

        return fmt_string.format(**t_dict)

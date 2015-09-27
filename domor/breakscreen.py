__author__ = 'dzung_nguyen'
try:
    from gi.repository import Gtk, Gdk, GObject
except ImportError:
    import gtk as Gtk
    import gtk.gdk as Gdk
    import gobject as GObject

import utils


class BreakScreen(object):
    def __init__(self, skip_handler):
        builder = Gtk.Builder()
        builder.add_from_file(utils.to_abs_path(utils.PoResources.UI_REST_SCREEN))
        builder.connect_signals(self)

        self.builder = builder
        self.windows = builder.get_object('break_window')
        self.lb_timer = builder.get_object('lb_timer')
        self.btn_skip = builder.get_object('btn_skip')
        self.reset()

        self.skip_handler = skip_handler

    def on_delete(self, *args):
        return True

    def on_btn_skip_clicked(self, button):
        self.skip_handler()

    def update_time(self, time_string):
        self.lb_timer.set_text(time_string)

    def reset(self):
        self.lb_timer.set_text('00:00')

    def show(self):
        setting = utils.Settings()
        if setting.break_mode == utils.Settings.MODE_BLOCK:
            self.windows.fullscreen()

        self.btn_skip.set_visible(setting.allow_skip)
        self.reset()
        self.windows.show()
        self.windows.present()
        self.windows.set_keep_above(True)

    def hide(self):
        self.windows.set_keep_above(False)
        self.windows.unfullscreen()
        self.windows.hide()

    def close(self):
        self.windows.close()
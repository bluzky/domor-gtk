__author__ = 'bluzky'
try:
    from gi.repository import Gtk, Gdk, GObject
except ImportError:
    import gtk as Gtk
    import gtk.gdk as Gdk
    import gobject as GObject

from utils import *
import style


class SettingDialog(object):
    def __init__(self):

        # build UI from glade file
        builder = Gtk.Builder()
        builder.add_from_file(to_abs_path(PoResources.UI_SETTING))
        builder.connect_signals(self)

        style.setStyle()

        # get some common used object
        self.builder = builder

        # 6 load config
        self.settings = settings = Settings()
        settings.load_config()

        self.dialog = builder.get_object('setting_dialog')
        self.cb_block_mode = builder.get_object('cb_block_input')
        self.cb_popup_mode = builder.get_object('cb_popup')
        self.sw_allow_skip = builder.get_object('swt_allow_skip')
        self.sw_sound_noti = builder.get_object('swt_enable_sound')
        self.txb_sound_file = builder.get_object('txb_sound_file')


    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Wav files")
        filter_text.add_pattern('*.wav')
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Mp3 files")
        filter_py.add_pattern('*.mp3')
        dialog.add_filter(filter_py)


    def show(self):
        if self.settings.break_mode is self.settings.MODE_BLOCK:
            self.cb_block_mode.set_active(True)
        else:
            self.cb_popup_mode.set_active(True)

        if self.settings.allow_skip:
            self.sw_allow_skip.set_active(True)
        else:
            self.sw_allow_skip.set_active(False)

        if self.settings.sound_notification:
            self.sw_sound_noti.set_active(True)
            self.txb_sound_file.set_text(self.settings.sound_path)
        else:
            self.sw_sound_noti.set_active(False)

        self.dialog.show()
        self.dialog.set_keep_above(True)
        self.dialog.set_keep_above(False)

    def on_close(self, *args):
        self.dialog.hide()
        return True

    def on_btn_select_sound_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Select sound file", self.dialog,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog.set_size_request(500,350)

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.txb_sound_file.set_text(dialog.get_filename())

        dialog.destroy()

    def on_btn_ok_clicked(self, button):
        self.settings.break_mode = Settings.MODE_BLOCK if self.cb_block_mode.get_active() else Settings.MODE_POP_UP
        self.settings.allow_skip = self.sw_allow_skip.get_active()

        self.settings.sound_notification = self.sw_sound_noti.get_active()

        if self.settings.sound_notification:
            sound_path = self.txb_sound_file.get_text()
            import os.path
            self.settings.sound_path = sound_path or get_sound(PoResources.SOUND_BELL)

        self.settings.save_config()
        self.dialog.hide()

    def on_btn_cancel_clicked(self, button):
        self.dialog.hide()

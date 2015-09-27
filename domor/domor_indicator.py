#!/usr/bin/env python
__author__ = 'bluzky'

try:
    from gi.repository import Gtk, Gdk, GObject
except ImportError:
    import gtk as Gtk
    import gobject as GObject

from utils import *
from breakscreen import BreakScreen
from main_window import MainWindow
from setting_dialog import SettingDialog
import pyglet
import style
from pkg_resources import resource_string


class DomorIndicator(object):

    def __init__(self):

        # build UI from glade file
        builder = Gtk.Builder()
        #builder.add_from_file(to_abs_path(PoResources.UI_TRAY))
        builder.add_from_file(to_abs_path(PoResources.UI_TRAY))
        builder.connect_signals(self)

        style.setStyle()

        # get some common used object
        self.builder = builder
        self.menu = builder.get_object('tray_menu')
        self.lb_clock = builder.get_object('mni_clock')
        self.lb_counter = builder.get_object('mni_archive_count')

        APPIND_SUPPORT = 1
        try:
            from gi.repository import AppIndicator3
        except:
            APPIND_SUPPORT = 0

        if APPIND_SUPPORT == 1:
            self.ind = AppIndicator3.Indicator.new_with_path("domor-indicator", 'app_icon_64',
                                                             AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
                                                             to_abs_path('img'))
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.ind.set_menu(self.menu)
        else:
            self.myStatusIcon = Gtk.StatusIcon()
            self.myStatusIcon.set_from_file(
                to_abs_path(PoResources.ICON_APP_64))
            self.myStatusIcon.connect(
                'popup-menu', self.right_click_event_statusicon)

        # 6 load config
        self.settings = settings = Settings()
        settings.load_config()

        # 7 init class state
        self.btn_state = State.STOP
        self.state = State.IDLE
        self.time = settings.short_work_time
        self.work_time = 0
        self.count = 0

        # create main screen
        self.main_window = MainWindow(self.on_mni_start_activate)
        self.main_window.update(self.state, self.btn_state)

        # create rest screen
        self.break_screen = BreakScreen(self.on_skip_break)

        self.reset()

        # register timer callback
        GObject.timeout_add_seconds(1, self.count_down)

    def reset(self):
        '''
        Reset to default state
        :return:
        '''
        self.state = State.IDLE
        self.time = self.settings.short_work_time
        self.btn_state = State.STOP

        self._update_item(
            'mni_start', get_resource(PoResources.ICON_START), 'Start')
        self._update_time()

        # hide break screen if showing
        self.break_screen.hide()
        if self.main_window:
            self.main_window.update(self.state, self.btn_state)

    def on_skip_break(self):
        if self.state == State.BREAK:
            # if time is counting and in break period and user click PAUSE button
            # reset timer and button state
            self.reset()

    def _update_item(self, item_id, img_path, label=None):
        """
        Update image for button
        :param button_id: id of button which is updated
        :param img_path: path to image
        :return: None
        """
        try:
            item = self.builder.get_object(item_id)
            img = Gtk.Image.new_from_file(img_path)
            item.set_image(img)
            if label:
                item.set_label(label)
        except Exception as e:
            print item_id
            print e.message

    def _update_time(self):
        """
        Update display time on UI
        :return:
        """
        time_string = "%02d:%02d" % (self.time / 60, self.time % 60)
        self.lb_clock.set_label(time_string)

        if self.state == State.BREAK:
            self.break_screen.update_time(time_string)

        if self.main_window:
            self.main_window.update_time(time_string)

    def _update_pomodoro_count(self):
        label = str(self.count) + \
            (" pomodoro" if self.count <= 1 else " pomodoros")
        self.lb_counter.set_label(label)

        if self.main_window:
            self.main_window.update_pomodoro_count(self.count)

    def count_down(self):
        if self.state != State.IDLE:

            if self.state == State.WORK:
                if self.time == 0:
                    self.count += 1

                    # long_work_time is the number of short working session
                    # between long break
                    if self.count % self.settings.long_work_time == 0:
                        self.start_break_period(self.settings.long_break_time)
                    else:
                        self.start_break_period(self.settings.short_break_time)
                    self._update_pomodoro_count()
                else:
                    self.time -= 1
                    self.work_time += 1

            else:
                if self.state == State.BREAK and self.time == 0:
                    # end of break period star new short work period
                    self.start_work_period()
                else:
                    self.time -= 1
            self._update_time()

        return True

    def start_break_period(self, break_time):
        self.state = State.BREAK
        self.time = break_time

        # play a sound
        song = pyglet.media.load(get_resource(self.settings.sound_path))
        song.play()

        self.break_screen.show()

        # change button to skip
        self._update_item(
            'mni_start', get_resource(PoResources.ICON_SKIP), 'Skip')
        self.main_window.update(self.state, self.btn_state)

    def start_work_period(self, with_sound=True):
        self.state = State.WORK
        self.btn_state = State.RUN
        self.time = self.settings.short_work_time

        # play a sound
        if with_sound:
            song = pyglet.media.load(get_resource(self.settings.sound_path))
            song.play()

        self.break_screen.hide()

        # # change button to play
        self._update_item(
            'mni_start', get_resource(PoResources.ICON_STOP), 'Stop')
        self.main_window.update(self.state, self.btn_state)

    def get_tray_menu(self):
        return self.menu

    def right_click_event_statusicon(self, icon, button, time):
        self.get_tray_menu()

        def pos(menu, aicon):
            return (Gtk.StatusIcon.position_menu(menu, aicon))

        self.menu.popup(None, None, pos, icon, button, time)

    def on_mni_start_activate(self, item=None):
        # if timer state is paused, start/resume counting
        if self.btn_state != State.RUN:
            self.start_work_period(False)
        else:
            self.reset()

    def mni_show_window_activate(self, item):
        self.main_window.show()

    def mni_setting_activate(self, item):
        if not hasattr(self, 'setting_dialog'):
            self.setting_dialog = SettingDialog()
        result = self.setting_dialog.show()
        print result

    def on_mni_quit_activate(self, item):
        Gtk.main_quit()


# if __name__ == '__main__':
#     indicator = DomorIndicator()
#     Gtk.main()

def start_app():
    indicator = DomorIndicator()
    Gtk.main()
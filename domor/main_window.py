from gi.repository import Gtk, GObject
from utils import *


class MainWindow(object):

    def __init__(self, click_callback):
        self.click_callback = click_callback

        self.builder = Gtk.Builder()
        self.builder.add_from_file(to_abs_path(PoResources.UI_MAIN))
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('wd_main')
        self.window.show_all()

        # 5 import control
        self.lb_timer = self.builder.get_object('lb_timer')
        self.btn_start = self.builder.get_object('btn_start')
        self.lb_pomodoro_counter = self.builder.get_object('lb_pomodoro_counter')


        # 6 load config
        self.settings = Settings()

        # 7 init class state
        self.btn_state = State.STOP
        self.state = State.IDLE

        self.reset()

    def reset(self):
        '''
        Reset to default state
        :return:
        '''
        self.state = State.IDLE
        self.btn_state = State.STOP

        self._update_button_image(
            'btn_start', get_resource(PoResources.IMG_PLAY))

    def _update_button_image(self, button_id, img_path):
        try:
            btn = self.builder.get_object(button_id)
            img = Gtk.Image.new_from_file(img_path)
            btn.set_image(img)
        except Exception as e:
            print e.message

    def update_time(self, time_string):
        self.lb_timer.set_text(time_string)

    def update_pomodoro_count(self, count):
        label = str(count) +  " pomodoro" if count <= 1 else " pomodoros"
        self.lb_pomodoro_counter.set_text(label)


    ## Event handler
    def on_wd_main_delete_event(self, *args):
        self.window.hide()
        return True

    def on_btn_start_clicked(self, button):
        # if timer state is paused, start/resume counting
        if self.btn_state != State.RUN:
            self._update_button_image(
                'btn_start', get_resource(PoResources.IMG_PAUSE))
        elif self.state == State.BREAK:
            # if time is counting and in break period and user click PAUSE button
            # reset timer and button state
            self.reset()
        else:  # if timer is counting, pause it
            self._update_button_image(
                'btn_start', get_resource(PoResources.IMG_PLAY))

        self.click_callback()


    def update_button_state(self, state):
        if state == State.RUN:
            self._update_button_image(
                'btn_start', get_resource(PoResources.IMG_PAUSE))
        elif state == State.STOP:
            self._update_button_image(
                'btn_start', get_resource(PoResources.IMG_PLAY))


    def show(self):
        self.window.present()

    def update(self, state, btn_state):
        self.update_button_state(btn_state)
        self.state = state

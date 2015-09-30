__author__ = 'bluzky'
import json
import sys
import os.path
import os

exe_path = ""
exe_dir = ""

if __name__ != '__main__':
    exe_dir = os.path.dirname(__file__)
elif hasattr(sys, 'frozen'):
    exe_path = sys.executable
    non_symbolic = os.path.realpath(sys.argv[0])
    exe_dir = os.path.dirname(non_symbolic)
else:
    exe_path = sys.argv[0]
    exe_dir = os.path.dirname(exe_path)

img_path = os.path.join(exe_dir, "img")
sound_path = os.path.join(exe_dir, "sound")


def get_image(img_name):
    return os.path.join(img_path, img_name)


def get_sound(sound_name):
    return os.path.join(sound_path, sound_name)

def to_abs_path(relative_path):
    return os.path.join(exe_dir, relative_path)

def get_resource(resource_name):
    return os.path.join(exe_dir, resource_name)

def get_config_file(file_name):
    try:
        config_dir = os.makedirs(os.path.expanduser("~/.config/domor"), 0755)
    except:
        config_dir= os.path.expanduser("~/.config/domor")
    return os.path.join(config_dir, file_name)


class Settings(object):

    (MODE_BLOCK, MODE_POP_UP) = xrange(0, 2)
    """
    Singleton class used to store all application setting
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.initialized = False
        return cls.__instance

    def __init__(self):
        if self.initialized:
            return
        self.initialized = True

        # default value
        self.short_work_time = 1500
        self.short_break_time = 300
        self.long_work_time = 4
        self.long_break_time = 900
        self.break_mode = self.MODE_BLOCK
        self.allow_skip = True
        self.sound_notification = True
        self.sound_path = get_resource(PoResources.SOUND_BELL)

    def to_json(self):
        return json.dumps(self.__dict__)

    def load_config(self):
        """
        load user config from file. If getting exception, use default setting
        :return:
        """
        try:
            with open(get_config_file(PoResources.FILE_CONFIG)) as config_file:
                conf_string = config_file.read()
                config = json.loads(conf_string)
                for key, value in config.iteritems():
                    if key in self.__dict__:
                        setattr(self, key, value)
        except Exception as e:
            print "Use default config"

    def save_config(self):
        """
        write setting to config file
        :return:
        """
        with open(get_config_file(PoResources.FILE_CONFIG) , mode="w") as config_file:
            config_str = self.to_json()
            config_file.write(config_str)


class PoResources(object):
    """
    Define all resource path
    """
    IMG_PLAY = 'img/play.png'
    IMG_PAUSE = 'img/pause.png'
    IMG_SKIP = 'img/skip.png'
    IMG_SETTING = 'img/setting.png'
    IMG_RESET = 'img/reset.png'
    SOUND_BELL = 'sound/bell.wav'
    FILE_CONFIG = 'domor.ini'
    UI_MAIN = 'ui/mainui.glade'
    UI_REST_SCREEN = 'ui/break_screen.glade'
    UI_TRAY = 'ui/tray_menu.glade'
    UI_SETTING = 'ui/option.glade'
    ICON_START = 'img/icon-play.png'
    ICON_STOP = 'img/icon-stop.png'
    ICON_SKIP = 'img/icon-skip.png'
    ICON_APP_64 = 'img/app_icon_64.png'
    ICON_APP_128 = 'img/app_icon_128.png'

class State:
    (RUN, STOP) = xrange(0, 2)
    (IDLE, WORK, BREAK) = xrange(0, 3)

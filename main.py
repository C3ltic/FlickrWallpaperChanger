import os
import sys

import flickr
from config import config
from change_wallpaper import change_wallpaper
from change_wallpaper import get_last_error
from SysTrayIcon import SysTrayIcon
from RepeatedTimer import RepeatedTimer

user_dir = os.path.join(os.environ["USERPROFILE"])
flickr_pic_dir = os.path.join(user_dir, '.flickr')
last_image = None
scheduler = None
scheduler_event = None


def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def set_wallpaper(sys_tray_icon=None):
    global last_image

    create_folder(flickr_pic_dir)
    delete_last_image()

    url = flickr.get_random_url()
    path = flickr.download_image(url, flickr_pic_dir)
    last_image = path

    if not change_wallpaper(path):
        return get_last_error()


def change_1min(sys_tray_icon):
    config.delay = 60
    scheduler.set_interval(config.delay)


def change_5min(sys_tray_icon):
    config.delay = 300
    scheduler.set_interval(config.delay)


def change_15min(sys_tray_icon):
    config.delay = 900
    scheduler.set_interval(config.delay)


def change_30min(sys_tray_icon):
    config.delay = 1800
    scheduler.set_interval(config.delay)


def change_1h(sys_tray_icon):
    config.delay = 3600
    scheduler.set_interval(config.delay)


def bye(sys_tray_icon):
    global scheduler
    scheduler.stop()
    delete_last_image()
    config.save_config()


def delete_last_image():
    global last_image
    if last_image:
        if os.path.exists(last_image):
            os.remove(last_image)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    if config.load_config():
        icon = resource_path('ico\\wallpaper.ico')
        hover_text = "Flickr Wallpaper Changer"

        menu_options = (
            ("Force change wallpaper", None, set_wallpaper),
            ('Delay', None, (
                ('1 min', None, change_1min),
                ('5 min', None, change_5min),
                ('15 min', None, change_15min),
                ('30 min', None, change_30min),
                ('1 h', None, change_1h))
             )
        )

        scheduler = RepeatedTimer(config.delay, set_wallpaper)
        scheduler.start()

        SysTrayIcon(icon, hover_text, menu_options, on_quit=bye, default_menu_index=1)
    else:
        print('Config file created. You need to complete it.')

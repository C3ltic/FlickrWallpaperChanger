import platform
import os
import sys

from PySide2 import QtWidgets, QtGui, QtCore

from package.api import flickr
from package.api.change_wallpaper import change_wallpaper
from package.api.change_wallpaper import get_last_error
from package.api.RepeatedTimer import RepeatedTimer
from package.api.config import config


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    app_resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'base')
    base_path = getattr(sys, '_MEIPASS', app_resource_path)
    return os.path.join(base_path, relative_path)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.width = 300
        self.height = 100

        # self.tray = None
        # self.lbl_title = None
        # self.btn_quit = None
        # self.btn_minimize = None
        # self.lbl_delay = None
        # self.cmb_delay = None
        # self.main_layout = None
        # self.layout_buttons = None
        # self.layout_delay = None
        # self.btn_force = None

        is_config = config.load_config()
        self.setup_ui()

        self.user_dir = os.path.join(os.environ["USERPROFILE"])
        self.flickr_pic_dir = os.path.join(self.user_dir, '.flickr')
        self.last_image = None
        self.scheduler = None
        self.scheduler_event = None

        if is_config:
            self.start_scheduler()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "The config file was not exists.\nIt has been created in "
                                                           "the executable directory.\nPlease, close application, "
                                                           "complete it and restart.")

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.setup_tray()

    def setup_tray(self):
        self.tray = QtWidgets.QSystemTrayIcon()

        icon = QtGui.QIcon(resource_path("icon.png"))

        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        self.tray.activated.connect(self.tray_icon_click)

    def create_widgets(self):
        self.lbl_title = QtWidgets.QLabel()
        self.btn_minimize = QtWidgets.QPushButton()
        self.btn_quit = QtWidgets.QPushButton()
        self.lbl_delay = QtWidgets.QLabel()
        self.cmb_delay = QtWidgets.QComboBox()
        self.btn_force = QtWidgets.QPushButton()

    def modify_widgets(self):
        self.main_layout.setContentsMargins(3, 3, 3, 3)
        self.main_layout.setSpacing(5)

        css_file = resource_path("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.lbl_title.setText('Flickr Wallpaper Changer  ')
        self.btn_minimize.setIcon(QtGui.QIcon(resource_path("minimize.png")))
        self.btn_quit.setIcon(QtGui.QIcon(resource_path("close.png")))

        self.lbl_delay.setText('Delay:')
        self.cmb_delay.addItem('1 min', userData=60)
        self.cmb_delay.addItem('5 min', userData=300)
        self.cmb_delay.addItem('15 min', userData=900)
        self.cmb_delay.addItem('30 min', userData=1800)
        self.cmb_delay.addItem('1 h', userData=3600)

        index = self.cmb_delay.findData(config.delay)
        self.cmb_delay.setCurrentIndex(index)

        self.btn_force.setText('Force Wallpaper change.')

        self.btn_minimize.setFixedSize(24, 24)
        self.btn_quit.setFixedSize(24, 24)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.layout_delay = QtWidgets.QHBoxLayout()

    def add_widgets_to_layouts(self):
        self.main_layout.addLayout(self.layout_buttons)
        self.layout_buttons.addWidget(self.lbl_title)
        self.layout_buttons.addStretch()
        self.layout_buttons.addWidget(self.btn_minimize)
        self.layout_buttons.addWidget(self.btn_quit)

        self.main_layout.addLayout(self.layout_delay)
        self.layout_delay.addWidget(self.lbl_delay)
        self.layout_delay.addWidget(self.cmb_delay)

        self.main_layout.addWidget(self.btn_force)

    def setup_connections(self):
        self.btn_minimize.clicked.connect(self.tray_icon_click)
        self.btn_quit.clicked.connect(self.on_quit_application)
        self.cmb_delay.currentIndexChanged.connect(self.on_change_delay)
        self.btn_force.clicked.connect(self.on_force_wallpaper)

    def center_under_tray(self):
        tray_x, tray_y, _, _ = self.tray.geometry().getCoords()
        w, h = self.sizeHint().toTuple()
        if platform.system() == 'Windows':
            self.move(tray_x - (w / 2), tray_y - h)
        else:
            self.move(tray_x - (w / 2), 25)

    def tray_icon_click(self):
        self.center_under_tray()

        if self.isHidden():
            self.showNormal()
        else:
            self.hide()

    def on_change_delay(self):
        delay = self.cmb_delay.currentData()
        config.delay = delay
        config.save_config()
        self.scheduler.set_interval(config.delay)

    def on_quit_application(self):
        if self.scheduler:
            self.scheduler.stop()
        self.delete_last_image()
        config.save_config()
        self.close()

    def on_force_wallpaper(self):
        self.btn_force.setStyleSheet('background-color: green;')
        self.btn_force.repaint()
        self.set_wallpaper()
        self.btn_force.setStyleSheet('background-color: #47A6E5;')

    def delete_last_image(self):
        if self.last_image:
            if os.path.exists(self.last_image):
                os.remove(self.last_image)

    def set_wallpaper(self):
        flickr.create_folder(self.flickr_pic_dir)
        self.delete_last_image()

        url = flickr.get_random_url()
        path = flickr.download_image(url, self.flickr_pic_dir)
        self.last_image = path

        if not change_wallpaper(path):
            return get_last_error()

    def start_scheduler(self):
        self.scheduler = RepeatedTimer(1, self.set_wallpaper)
        self.scheduler.start()
        self.scheduler.set_interval(config.delay)


if __name__ == '__main__':
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)
    # Create the Window
    win = MainWindow()
    # Run the main Qt loop
    sys.exit(app.exec_())

import struct
import ctypes


SPI_SET_DESKTOP_WALLPAPER = 20


def is_64_windows():
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper(image_path):
    sys_parameters_info = get_sys_parameters_info()
    return sys_parameters_info(SPI_SET_DESKTOP_WALLPAPER, 0, image_path, 3)


def get_last_error():
    # When the SPI_SET_DESKTOP_WALLPAPER flag is used,
    # SystemParametersInfo returns TRUE
    # unless there is an error (like when the specified file doesn't exist).
    return ctypes.WinError()

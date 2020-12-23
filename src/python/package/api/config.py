import os
import sys
import yaml


def get_sizes(maximum_size):
    if not maximum_size:
        maximum_size = 'HD'

    if maximum_size == 'VGA':  # 640x480
        return ["url_z", "url_c", "url_b"]
    elif maximum_size == 'SVGA':  # 800x600
        return ["url_c", "url_b", "url_h"]
    elif maximum_size == 'XGA':  # 1024x768
        return ["url_b", "url_h", "url_z"]
    elif maximum_size == 'UXGA':  # 1600x1200
        return ["url_h", "url_b", "url_k", "url_o"]
    elif maximum_size == 'HD':  # 1920x1080
        return ["url_k", "url_3k", "url_4k", "url_o"]
    elif maximum_size == '3K':  # 3072
        return ["url_3k", "url_4k", "url_f", "url_o"]
    elif maximum_size == '4K':  # 4096
        return ["url_4k", "url_f", "url_5k", "url_6k", "url_o"]
    elif maximum_size == '5K':  # 5120
        return ["url_5k", "url_6k", "url_o"]
    elif maximum_size == '6K':  # 6144
        return ["url_6k", "url_o"]


class Config(object):
    data = dict(
        api_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx',
        api_secret='XXXXXXXXXXXXX',
        max_image_pull=50,
        image_ratio=1.333333,
        horizontal=True,
        maximum_size='HD',
        delay=60
    )
    api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
    api_secret = 'XXXXXXXXXXXXX'
    max_image_pull = 50
    image_ratio = 1.333333
    horizontal = True
    maximum_size = 'HD'
    delay = 60
    sizes = ["url_k", "url_3k", "url_4k", "url_o"]

    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        elif __file__:
            self.base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
        self.config_file = os.path.join(self.base_dir, 'config.yml')

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='UTF-8') as f:
                cur_config = yaml.safe_load(f)

            self.api_key = cur_config.get('api_key')
            self.api_secret = cur_config.get('api_secret')
            self.max_image_pull = cur_config.get('max_image_pull')
            self.image_ratio = cur_config.get('image_ratio')
            self.horizontal = cur_config.get('horizontal')
            self.maximum_size = cur_config.get('maximum_size')
            self.sizes = get_sizes(self.maximum_size)
            self.delay = cur_config.get('delay')
            return True
        else:
            self.save_config()
            return False

    def save_config(self):
        self.data['api_key'] = self.api_key
        self.data['api_secret'] = self.api_secret
        self.data['max_image_pull'] = self.max_image_pull
        self.data['image_ratio'] = self.image_ratio
        self.data['horizontal'] = self.horizontal
        self.data['maximum_size'] = self.maximum_size
        self.data['delay'] = self.delay

        with open(self.config_file, 'w', encoding='UTF-8') as f:
            yaml.safe_dump(self.data, f)


config = Config()

# FlickrWallpaperChanger
**Flickr Wallpaper Changer** is a systray application to change automatically your desktop 
wallpaper with a dowloaded picture from **Flickr public images of the day**.

_Tested on Windows 10_

## Used modules
* [FlickrAPI](https://stuvel.eu/software/flickrapi/)
* [PyInstaller](https://www.pyinstaller.org/)
* [PyYAML](https://github.com/yaml/pyyaml)
* [pywin32](https://github.com/mhammond/pywin32)
* [pywin32-ctypes](https://github.com/enthought/pywin32-ctypes)
* [PySide2](https://wiki.qt.io/Qt_for_Python)

## Config file
The config file is named config.yml.
At the first launch of the application, it's automatically created.
The coontent of this file is :

```YAML
api_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
api_secret: XXXXXXXXXXXXX
delay: 60
horizontal: true
image_ratio: 1.333333
max_image_pull: 50
maximum_size: HD
```

```YAML
api_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
api_secret: XXXXXXXXXXXXX
```
API key & secret of the Flickr API can be found at this [link](https://www.flickr.com/services/api/keys/) (you need to have a valid account)

```YAML
delay: 60
```
Delay in seconds beetween the wallpaper change

```YAML
horizontal: true
```
Choose horizontal screen (if true) or vertical (if false)

```YAML
image_ratio: 1.333333
```
The minimum image ratio (4/3 by default)

```YAML
max_image_pull: 50
```
The number image pull from wwich we will choose

```YAML
maximum_size: HD
```
The maximum image resolution
```
VGA  ->   640
SVGA ->   800
XGA  ->  1024
UXGA ->  1200
HD   ->  1920
4K   ->  4096
6K   ->  6144
```

## Extra information
The downloaded current wallpaper is in the driectory `~\.flickr\`
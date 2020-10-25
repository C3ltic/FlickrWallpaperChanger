import os.path
import requests
from random import randrange

from flickrapi import FlickrAPI

from package.api.config import config

# api_key = u'28a24dd1e2782a45a92489a5ff3280cc'
# api_secret = u'283b4b6c9a5ba504'
MIN_SIZE_RATIO = 1.333333
# SIZES = ["url_o", "url_k", "url_h", "url_l"]  # in order of preference


def get_photos():
    extras = ','.join(config.sizes)
    flickr = FlickrAPI(config.api_key, config.api_secret, cache=True)
    photos = flickr.interestingness.getList(extras=extras,  # get the urls for each size we want
                                            privacy_filter=1,  # search only for public photos
                                            per_page=config.max_image_pull,
                                            sort='relevance')
    return photos[0]


def get_url(sel_photo, min_size_ratio=None):
    if not min_size_ratio:
        min_size_ratio = MIN_SIZE_RATIO
    attrib = sel_photo.attrib
    for i in range(len(config.sizes)):  # makes sure the loop is done in the order we want
        purl = attrib.get(config.sizes[i])
        if purl:  # if url is None try with the next size
            suffix = config.sizes[i].split('_')[1]
            height_str = 'height_' + suffix
            width_str = 'width_' + suffix
            height = attrib.get(height_str)
            width = attrib.get(width_str)
            ratio = int(width) / int(height)

            if config.horizontal:
                if ratio > min_size_ratio:
                    return purl
            else:
                if ratio < min_size_ratio:
                    return purl


def download_images(urls, path):
    for purl in urls:
        download_image(purl, path)


def download_image(url, path):
    image_name = url.split("/")[-1]
    image_path = os.path.join(path, image_name)

    if not os.path.isfile(image_path):  # ignore if already downloaded
        response = requests.get(url, stream=True)

        with open(image_path, 'wb') as outfile:
            outfile.write(response.content)

        return image_path


def get_urls(max_url=10000, min_size_ratio=None):
    photos = get_photos()
    counter = 0
    urls = []

    for photo in photos:
        if counter < max_url:
            url = get_url(photo, min_size_ratio)  # get preffered size url
            if url:
                urls.append(url)
                counter += 1
            # if no url for the desired sizes then try with the next photo
        else:
            break

    return urls


def get_random_url(last_url):
    urls = get_urls(min_size_ratio=config.image_ratio)
    total = len(urls)
    while True:
        num = randrange(total)
        if last_url != urls[num]:   # be sure the next photo is different.
            break
    return urls[num]


def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Thanks to Benoit C. Sirois for the original code
#https://github.com/benwah

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError
import time
import sys
import subprocess
import os
import json
import re
import random
import argparse
import socket
import ctypes

#My preferred subreddit
REDDIT_URL = 'http://www.reddit.com/r/wallpaper.json?t=week&limit=100'
TIMEOUT = 5

#Highly original name for a wallpaper folder (I'm using the working directory)
DATA_DIR = "wallpaper"

MAX_ATTEMPTS = 5
SLEEP_SECONDS_AFTER_ATTEMPT = 2

def get_image(url):
    """
    Makes a call to reddit and returns one post randomly from the page
    specified in url.
    """
    i = 0
    while True:
        if i == MAX_ATTEMPTS:
            raise Exception('Sorry, can\'t reach reddit.')
        try:
            data = json.loads(
                urlopen(url, timeout=TIMEOUT).read().decode('utf-8'))
            break
        except HTTPError as e:
            # Too many requests, give reddit a break, try again.
            print("JSON api throttled, attempt %s on %s" % (i, MAX_ATTEMPTS))
            if getattr(e, 'code', None) == 429:
                time.sleep(SLEEP_SECONDS_AFTER_ATTEMPT)
            i += 1
        except socket.timeout:
            print("Timeout, attempt %s on %s" % (i, MAX_ATTEMPTS))
            time.sleep(SLEEP_SECONDS_AFTER_ATTEMPT)
            i += 1

    candidates = data.get('data', {}).get('children', {})
    
    #pick a random one
    image = candidates[random.randrange(0, len(candidates))]['data']
    
    #return the [URL,image name,post title]
    return [
        image['preview']['images'][0]['source']['url'],
        'wallpaper_image.jpg',
        image['title']
    ]


def save_image(url, file_path):
    os.remove(file_path)
    f = open(file_path, 'wb')

    i = 0
    while True:
        if i == MAX_ATTEMPTS:
            f.close()
            raise Exception('Sorry, can\'t reach imgur.')
        try:
            data = urlopen(url, timeout=TIMEOUT).read()
            if len(data) > 0:
                f.write(data)
            else:
                raise Exception('0 Bytes in download, exiting')
            f.close()
            break
        except HTTPError:
            time.sleep(1)
            i += 1
        except socket.timeout:
            # Socket timeout, try again.
            i += 1


def display_image(image_name,title):
    
    cwd = os.getcwd()
    image_path = os.path.join(cwd, image_name)
    
    #THIS THING ADDS TITLES FOR CONTEXT
    from PIL import ImageFont, ImageDraw, ImageEnhance, Image
    source_img = Image.open(image_path)
    width,height = source_img.size
    draw = ImageDraw.Draw(source_img)
    
    #RECTANGLE 100% of width and 7% of the height drawn on the top
    draw.rectangle(((0, 00), (int(1*width), int(0.07*height))), fill="black")
    
    #TEXT is 1% of height and starts 3% from the side
    draw.text((int(0.03*width), int(0.01*height)), title, font=ImageFont.truetype("C:/Windows/fonts/Arial.ttf",int(0.03*height)))
    
    source_img.save(image_path, "JPEG")
    
    #This part sets the wallpaper
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, str(image_path), 3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('Use reddit for wallpapers'))

        #CHANGED DEFAULT HERE
    parser.add_argument(
        '--destination',
        type=str,
        default=DATA_DIR,
        help='Destination directory (default: %s)' % DATA_DIR,
        )
    
    parser.add_argument(
        '--output-name',
        type=str,
        default=None,
        help='Output filename (defaults to imgur name)',
        )

    parser.add_argument(
        '--overwrite-existing',
        type=str,
        default='',
        help=(
            'Overwrite file if exists? (True / False), default is'
            ' False'),
        )


    parser.add_argument(
        '--reddit-json-url',
        type=str,
        default=REDDIT_URL,
        help='Specify a subreddit .json url. (default %s)' % REDDIT_URL,
        )

    parser.add_argument(
        '--set-wallpaper',
        type=str,
        default='True',
        help='Set wallpaper? (True / False), default is True',
    )

    args = parser.parse_args()

    if not os.path.exists(args.destination) and args.destination == DATA_DIR:
        os.mkdir(args.destination)

    if not os.path.exists(args.destination):
        raise Exception(
            ('Destination directory %s does not exist, or is '
             'unreadable') % args.destination)

    image = get_image(args.reddit_json_url)

    if not image:
        print("No image found")
        sys.exit(1)

    target_file_name = args.output_name or image[1]
    file_path = os.path.join(args.destination, target_file_name)

    save_image(image[0], file_path)
    if args.set_wallpaper == 'True':
        display_image(file_path,image[2])

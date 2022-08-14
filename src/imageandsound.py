# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from os import path, mkdir

from PIL import Image


def img_encode(image_file, base64_file):
    with open(image_file, 'rb') as image:
        temp = f'image = {base64.b64encode(image.read())}'

    with open(base64_file, 'w') as f:
        f.write(temp)
        f.write(f'\ntype = "{path.splitext(image_file)[1]}"')


def img_decode(is_exists=False):
    from image_base64 import image, type
    if is_exists:
        return type, Image.open(path.join('.', 'img', f'image{type}')).size
    dir = path.join('.', 'img')
    if not path.isdir(dir):
        mkdir(dir)
    image = base64.b64decode(image)
    image = BytesIO(image)
    image = Image.open(image)
    image.save(path.join(dir, f'image{type}'))
    return type, image.size


def sound_encode(image_file, base64_file):
    with open(image_file, 'rb') as image:
        temp = f'sound = {base64.b64encode(image.read())}'

    with open(base64_file, 'w') as f:
        f.write(temp)


def sound_decode():
    dir = path.join('.', 'sound')
    if not path.isdir(dir):
        mkdir(dir)
    from sound_base64 import sound
    sound = base64.b64decode(sound)
    with open(path.join(dir, 'sound.mp3'), 'wb') as f:
        f.write(sound)

if __name__ == '__main__':
    base64_file = path.join('.', 'src', 'image_base64.py')
    image_file = path.join('.', 'img', 'image.jpg' if path.exists(path.join('.', 'img', 'image.jpg')) else 'image.png')
    try:
        img_encode(image_file, base64_file)
    except:
        test_file = path.join('.', 'img', 'test.jpg')
        img_encode(test_file, base64_file)

    base64_file = path.join('.', 'src', 'sound_base64.py')
    image_file = path.join('.', 'sound', 'sound.mp3')
    try:
        sound_encode(image_file, base64_file)
    except:
        test_file = path.join('.', 'sound', 'test.mp3')
        sound_encode(test_file, base64_file)

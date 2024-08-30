import math
import urllib
import cv2
import csv
from urllib.request import urlopen
from urllib.error import HTTPError
import numpy as np
import os
from os import path
from pathlib import Path


def overlay_frame(fore_im, frame):
    fh, fw = fore_im.shape[:2]
    # 选择不同模版
    if fh / fw > 1.05:
        back_im = cv2.imread('/Users/paperplane/Documents/back-m-2.jpg')
    elif fh / fw > 0.95:
        back_im = cv2.imread('/Users/paperplane/Documents/back-m-1.jpg')
    else:
        back_im = cv2.imread('/Users/paperplane/Documents/back-m-3.jpg')
    bh, bw = back_im.shape[:2]

    if bw / bh > fw / fh:
        n_fh = math.ceil(bh * 0.88)
        n_fw = math.ceil(bh * 0.88 * fw / fh)
    else:
        n_fw = math.ceil(bw * 0.88)
        n_fh = math.ceil(bw * 0.88 * fh / fw)
    fore_im = cv2.resize(fore_im, (n_fw, n_fh))

    # 计算居中位置
    x = (back_im.shape[1] - fore_im.shape[1]) // 2
    y = (back_im.shape[0] - fore_im.shape[0]) // 2

    # 将前景图片置于背景中心
    back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = fore_im[:, :, :3]

    cv2.imwrite(frame, back_im)


def overlay_env(fore_im, env):
    fh, fw = fore_im.shape[:2]
    # 选择不同模版
    if fh / fw > 1.1:
        back_im = cv2.imread('/Users/paperplane/Documents/back-e-2.png')
    elif fh / fw == 1:
        # back_im = cv2.imread('/Users/paperplane/Documents/back-e-1.jpg')
        return
    else:
        # back_im = cv2.imread('/Users/paperplane/Documents/back-e-3.jpg')
        return
    # bh, bw = back_im.shape[:2]
    inner_h = (637 - 210)
    inner_w = (700 - 382)

    if inner_w / inner_h > fw / fh:
        n_fw = math.ceil(inner_w * 1.1)
        n_fh = math.ceil(inner_w * fh / fw * 1.1)
    else:
        n_fh = math.ceil(inner_h * 1.1)
        n_fw = math.ceil(inner_h * fw / fh * 1.1)
    fore_im = cv2.resize(fore_im, (n_fw, n_fh))

    # 设置原点位置
    x = 382
    y = 210

    # 将前景图片置于背景中心
    back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = fore_im[:, :, :3]

    cv2.imwrite(env, back_im)


def overlay_envs(fore_im, env):
    fh, fw = fore_im.shape[:2]
    # 选择不同模版
    if fh / fw > 1.05:
        back_im = cv2.imread('/Users/paperplane/Documents/back-e-2.jpg')
    elif fh / fw > 0.95 or fw / fh > 0.95:
        back_im = cv2.imread('/Users/paperplane/Documents/back-e-1.jpg')
    else:
        back_im = cv2.imread('/Users/paperplane/Documents/back-e-3.jpg')
    bh, bw = back_im.shape[:2]

    if bw / bh > fw / fh:
        n_fh = math.ceil(bh * 0.85)
        n_fw = math.ceil(bh * 0.85 * fw / fh)
    else:
        n_fw = math.ceil(bw * 0.85)
        n_fh = math.ceil(bw * 0.85 * fh / fw)
    fore_im = cv2.resize(fore_im, (n_fw, n_fh))

    # 计算居中位置
    x = (back_im.shape[1] - fore_im.shape[1]) // 2
    y = (back_im.shape[0] - fore_im.shape[0]) // 2

    # 将前景图片置于背景中心
    back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = fore_im[:, :, :3]

    cv2.imwrite(env, back_im)


def read_foreground_frame(foreground):
    try:
        req = urllib.request.urlopen(foreground)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

        # Decode the image data into a format OpenCV can work with
        fore_im = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        names = foreground.split('?')[0].split('/')
        name, suffix = names[-1].split('.')
        frame = '/Users/paperplane/Downloads/opts/' + name + '-M' + '.' + suffix
        return fore_im, frame

    except HTTPError:
        print('Error:', foreground)

        try:
            foreground = foreground.replace('.jpg?', '.png?')
            req = urllib.request.urlopen(foreground)
        except HTTPError:
            print('Error:', foreground)
            return None, ''
        else:
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

            # Decode the image data into a format OpenCV can work with
            fore_im = cv2.imdecode(arr, cv2.IMREAD_COLOR)

            names = foreground.split('?')[0].split('/')
            name, suffix = names[-1].split('.')
            frame = '/Users/paperplane/Downloads/opts/' + name + '-M' + '.' + suffix
            return fore_im, frame


def read_foreground_env1(foreground):
    fore_im = cv2.imread(foreground)
    names = foreground.split('?')[0].split('/')
    name, suffix = names[-1].split('.')
    name = name.rstrip('-M')
    environment = '/Users/paperplane/Downloads/envs/' + name + '-S-1' + '.' + suffix
    return fore_im, environment


def generate_frame():
    error_path = "/Users/paperplane/Downloads/errors"
    frame_path = "/Users/paperplane/Downloads/opts"
    files = [os.path.join(frame_path, f) for f in os.listdir(error_path) if os.path.isfile(os.path.join(error_path, f))]

    with open('/Users/paperplane/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            if not url.startswith('https'):
                continue
            for_im, frame_name = read_foreground_frame(foreground=url)
            if frame_name not in files:
                continue
            if for_im is None:
                continue
            overlay_frame(for_im, frame_name)


def generate_env():
    dir_path = "/Users/paperplane/Downloads/frames"
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    for file in files:
        file_path = os.path.join(dir_path, file)
        for_im, env_name = read_foreground_env1(foreground=file_path)
        if for_im is None:
            continue
        overlay_env(for_im, env_name)


if __name__ == '__main__':
    generate_env()

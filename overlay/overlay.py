import math
import urllib
import cv2
import csv
from urllib.request import urlopen
from urllib.error import HTTPError
import numpy as np
import os


def overlay_frame(fore_im, frame):
    if frame == '/Users/ipaperplane/Downloads/f/Serenity_in_Stripes_1.png' or frame == '/Users/ipaperplane/Downloads/f/Serenity_in_Stripes_1.jpg':
        print(frame)
    fh, fw = fore_im.shape[:2]
    # 选择不同模版
    if fh / fw > 1.05:
        back_im = cv2.imread('/Users/ipaperplane/Downloads/back/back_f_2.jpg')
    elif fh / fw > 0.95:
        back_im = cv2.imread('/Users/ipaperplane/Downloads/back/back_f_3.jpg')
    else:
        back_im = cv2.imread('/Users/ipaperplane/Downloads/back/back_f_1.jpg')
    bh, bw = back_im.shape[:2]

    if bw / bh > fw / fh:
        n_fh = math.ceil(bh * 0.75)
        n_fw = math.ceil(bh * 0.75 * fw / fh)
    else:
        n_fw = math.ceil(bw * 0.75)
        n_fh = math.ceil(bw * 0.75 * fh / fw)
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
    inner_h, inner_w = 0, 0
    if fh / fw > 1.05:
        back_im = cv2.imread('/Users/ipaperplane/Downloads/back/back-e-2.jpg')
        inner_h = (637 - 210)
        inner_w = (700 - 382)

    elif fh / fw > 0.95:
        back_im = cv2.imread('/Users/ipaperplane/Downloads/back/back-e-3.jpg')
        inner_h = (230 - 125)
        inner_w = (880 - 676)

    else:
        back_im = cv2.imread('/Users/ipaperplane/Downloads/back/back-e-1.png')
        inner_h = (234 - 118)
        inner_w = (623 - 448)

    if inner_w / inner_h > fw / fh:
        n_fw = math.ceil(inner_w * 1)
        n_fh = math.ceil(inner_w * fh / fw * 1)
    else:
        n_fh = math.ceil(inner_h * 1)
        n_fw = math.ceil(inner_h * fw / fh * 1)

    fore_im = cv2.resize(fore_im, (n_fw, n_fh))

    # 设置原点位置
    if fh / fw > 1.05:
        x = 382
        y = 210
    elif fh / fw > 0.95:
        x = 676
        y = 125
    else:
        x = 448
        y = 118

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
        if name == 'Pirate_Ship_Adventure':
            print(name)
        frame = '/Users/ipaperplane/Downloads/que/' + name + '-M' + '.' + suffix
        return fore_im, frame

    except:
        print('Error:', foreground)

        try:
            foreground = foreground.replace('.jpg?', '.png?')
            req = urllib.request.urlopen(foreground)
        except:
            print('Error:', foreground)
            return None, ''
        else:
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

            # Decode the image data into a format OpenCV can work with
            fore_im = cv2.imdecode(arr, cv2.IMREAD_COLOR)

            names = foreground.split('?')[0].split('/')
            name, suffix = names[-1].split('.')
            frame = '/Users/ipaperplane/Downloads/opts/' + name + '-M' + '.' + suffix
            return fore_im, frame


def read_foreground_env1(foreground):
    fore_im = cv2.imread(foreground)
    names = foreground.split('?')[0].split('/')
    name, suffix = names[-1].split('.')
    name = name.rstrip('-M-1')
    environment = '/Users/ipaperplane/Downloads/e/' + name + '-S' + '.' + suffix
    return fore_im, environment


def generate_frame():
    with open('/Users/ipaperplane/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            if not url.startswith('https'):
                continue
            print('start: ' + url)
            for_im, frame_name = read_foreground_frame(foreground=url)
            names = url.split('?')[0].split('/')
            name, suffix = names[-1].split('.')
            frame_name = '/Users/ipaperplane/Downloads/frame/' + name + '-M' + '.' + suffix

            print('end: ' + url)
            if for_im is None:
                continue
            overlay_frame(for_im, frame_name)


def generate_env():
    dir_path = "/Users/ipaperplane/Downloads/frame"
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    for file in files:
        file_path = os.path.join(dir_path, file)
        for_im, env_name = read_foreground_env1(foreground=file_path)
        if for_im is None:
            continue
        overlay_env(for_im, env_name)


def generate_frame1():
    with open('/Users/ipaperplane/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            if not url.startswith('https'):
                continue
            print('start: ' + url)
            for_im, frame_name = read_foreground_frame(foreground=url)
            print('end: ' + url)
            if for_im is None:
                continue
            overlay_frame(for_im, frame_name)


if __name__ == '__main__':
    files = ['https://cdn.shopify.com/s/files/1/0662/6535/0302/files/Dive_into_the_waves_of_serenity_1.png?v=1723479927',
             'https://cdn.shopify.com/s/files/1/0662/6535/0302/files/Mesmerizing_wavy_lines_1.png?v=1723479928',
             'https://cdn.shopify.com/s/files/1/0662/6535/0302/files/Serenity_in_Stripes_1.png?v=1723479901',
             'https://cdn.shopify.com/s/files/1/0662/6535/0302/files/Drawing_in_the_Cafe1.jpg?v=1723479866']
    # generate_frame()
    # generate_frame1()
    # generate_env()

    for url in files:
        for_im, frame_name = read_foreground_frame(foreground=url)
        if for_im is None:
            continue
        overlay_frame(for_im, frame_name)

    dir_path = "/Users/ipaperplane/Downloads/que"
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    for file in files:
        file_path = os.path.join(dir_path, file)
        for_im, env_name = read_foreground_env1(foreground=file_path)
        if for_im is None:
            continue
        overlay_env(for_im, env_name)


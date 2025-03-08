import math
import urllib
import cv2
import csv
from urllib.request import urlopen
import numpy as np
import os


def overlay_frame(fore_im, frame):
    fh, fw = fore_im.shape[:2]
    # 选择不同模版
    if fh / fw > 1.1:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_s_2.jpg')
        inner_h = (5840 - 1351)
        inner_w = (4133 - 1189)

    elif fh / fw > 0.9:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_s_3.jpg')
        inner_h = (4975 - 1525)
        inner_w = (4420 - 970)

    else:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_s_1.jpg')
        inner_h = (4206 - 1197)
        inner_w = (5859 - 1336)

    if inner_w / inner_h > fw / fh:
        n_fw = math.ceil(inner_w * 0.72)
        n_fh = math.ceil(inner_w * fh / fw * 0.72)
    else:
        n_fh = math.ceil(inner_h * 0.72)
        n_fw = math.ceil(inner_h * fw / fh * 0.72)

    fore_im = cv2.resize(fore_im, (n_fw, n_fh))

    # 设置原点位置
    if fh / fw > 1.05:
        x = 1189 + math.ceil((inner_w - n_fw) / 2)
        y = 1351 + math.ceil((inner_h - n_fh) / 2)
    elif fh / fw > 0.95:
        x = 970 + math.ceil((inner_w - n_fw) / 2)
        y = 1525 + math.ceil((inner_h - n_fh) / 2)
    else:
        x = 1336 + math.ceil((inner_w - n_fw) / 2)
        y = 1197 + math.ceil((inner_h - n_fh) / 2)

    # 将前景图片置于背景中心
    back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = fore_im[:, :, :3]

    cv2.imwrite(frame, back_im)


def overlay_h_frame(fore_im, frame):
    fh, fw = fore_im.shape[:2]
    # 选择不同模版
    if fh / fw > 1.1:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_h_2.jpg')
        inner_h = (5876 - 1300)
        inner_w = (4350 - 1040)

    elif fh / fw > 0.9:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_h_3.jpg')
        inner_h = (4907 - 1597)
        inner_w = (4370 - 1060)

    else:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_h_1.jpg')
        inner_h = (4357 - 1042)
        inner_w = (5888 - 1308)

    if inner_w / inner_h > fw / fh:
        n_fw = math.ceil(inner_w * 0.72)
        n_fh = math.ceil(inner_w * fh / fw * 0.72)
    else:
        n_fh = math.ceil(inner_h * 0.72)
        n_fw = math.ceil(inner_h * fw / fh * 0.72)

    fore_im = cv2.resize(fore_im, (n_fw, n_fh))

    # 设置原点位置
    if fh / fw > 1.05:
        x = 1040 + math.ceil((inner_w - n_fw) / 2)
        y = 1300 + math.ceil((inner_h - n_fh) / 2)
    elif fh / fw > 0.95:
        x = 1060 + math.ceil((inner_w - n_fw) / 2)
        y = 1597 + math.ceil((inner_h - n_fh) / 2)
    else:
        x = 1308 + math.ceil((inner_w - n_fw) / 2)
        y = 1042 + math.ceil((inner_h - n_fh) / 2)

    # 将前景图片置于背景中心
    back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = fore_im[:, :, :3]

    cv2.imwrite(frame, back_im)


def overlay(fore_im, frame):
    fh, fw = fore_im.shape[:2]
    # 选择不同模版
    if fh / fw > 1.05:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_n_h_2.jpg')
    elif fh / fw > 0.95:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_n_h_3.jpg')
    else:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back_n_h_1.jpg')
    bh, bw = back_im.shape[:2]

    if bw / bh > fw / fh:
        n_fh = math.ceil(bh * 0.68)
        n_fw = math.ceil(bh * 0.68 * fw / fh)
    else:
        n_fw = math.ceil(bw * 0.68)
        n_fh = math.ceil(bw * 0.68 * fh / fw)
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
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back-e-2.jpg')
        inner_h = (637 - 210)
        inner_w = (700 - 382)

    elif fh / fw > 0.95:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back-e-3.jpg')
        inner_h = (230 - 125)
        inner_w = (880 - 676)

    else:
        back_im = cv2.imread('/Users/bytedance/Downloads/back/back-e-1.png')
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
        frame = '/Users/bytedance/Downloads/opts/' + name + '-M' + '.' + suffix
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
            frame = '/Users/bytedance/Downloads/opts/' + name + '-M' + '.' + suffix
            return fore_im, frame


def read_foreground_env1(foreground):
    fore_im = cv2.imread(foreground)
    names = foreground.split('?')[0].split('/')
    name, suffix = names[-1].split('.')
    name = name.rstrip('-M-1')
    environment = '/Users/bytedance/Downloads/e/' + name + '-S' + '.' + suffix
    return fore_im, environment


def generate_frame():
    with open('/Users/bytedance/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            if not url.startswith('https'):
                continue
            print('start: ' + url)
            for_im, frame_name = read_foreground_frame(foreground=url)
            names = url.split('?')[0].split('/')
            name, suffix = names[-1].split('.')
            file_name = name + '-M-1' + '.' + suffix
            frame_name = '/Users/bytedance/Downloads/debug/' + file_name
            print('end: ' + url)
            if for_im is None:
                continue
            overlay_frame(for_im, frame_name)


def generate_h_frame():
    with open('/Users/bytedance/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            if not url.startswith('https'):
                continue
            print('start: ' + url)
            for_im, frame_name = read_foreground_frame(foreground=url)
            names = url.split('?')[0].split('/')
            name, suffix = names[-1].split('.')
            file_name = name + '-M-2' + '.' + suffix
            frame_name = '/Users/bytedance/Downloads/debug/' + file_name
            print('end: ' + url)
            if for_im is None:
                continue
            overlay_h_frame(for_im, frame_name)


def generate_env():
    dir_path = "/Users/bytedance/Downloads/frame"
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    for file in files:
        file_path = os.path.join(dir_path, file)
        for_im, env_name = read_foreground_env1(foreground=file_path)
        if for_im is None:
            continue
        overlay_env(for_im, env_name)


def generate_frame1():
    with open('/Users/bytedance/Downloads/zenarart.csv', newline='') as csvfile:
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
    # generate_frame()
    # generate_h_frame()

    # dir_path = "/Users/bytedance/Downloads/que"
    # files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    # for file in files:
    #     file_path = os.path.join(dir_path, file)
    #     for_im, env_name = read_foreground_env1(foreground=file_path)
    #     if for_im is None:
    #         continue
    #     overlay_env(for_im, env_name)

    name_list = []
    with open('/Users/bytedance/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            if not url.startswith('https'):
                continue
            print('start: ' + url)

            fore_im, frame = read_foreground_frame(url)
            if fore_im is None:
                continue
            name_list.append(frame)
            print('end:' + url)
            overlay(fore_im, frame)

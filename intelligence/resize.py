import cv2
import numpy as np


def resize_and_pad(image, target_size):
    h, w = image.shape[:2]
    sh, sw = target_size

    # 计算缩放比例
    aspect = w / h

    # 调整大小，保持宽高比
    if aspect > 1:
        new_w = sw
        new_h = np.round(new_w / aspect).astype(int)
    else:
        new_h = sh
        new_w = np.round(new_h * aspect).astype(int)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # 创建空白画布
    padded = np.ones((sh, sw, 3), dtype=np.uint8) * 255

    # 计算偏移量
    dx = (sw - new_w) // 2
    dy = (sh - new_h) // 2

    # 将调整后的图像复制到空白画布上
    padded[dy:dy + new_h, dx:dx + new_w] = resized

    return padded


if __name__ == '__main__':
    # 使用示例
    image = cv2.imread('/Users/ipaperplane/Downloads/back.jpg')
    target_size = (3000, 3000)  # 目标尺寸
    result = resize_and_pad(image, target_size)
    cv2.imwrite('/Users/ipaperplane/Downloads/background1.jpg', result)
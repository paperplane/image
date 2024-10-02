import cv2
import numpy as np


def resize(source, output, width_ratio, height_ratio):
    # 读取原始图像
    img = cv2.imread(source)

    # 获取原始图像尺寸
    height, width = img.shape[:2]

    # 计算新的目标尺寸，保持2:3比例
    if width / height > width_ratio / height_ratio:
        new_width = width
        new_height = int(width * height_ratio / width_ratio)
    else:
        new_height = height
        new_width = int(height * width_ratio / height_ratio)

    # 调整图像大小
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # 保存调整后的图像
    cv2.imwrite(output, resized_img)


def resize_and_pad(source, output, width_ratio, height_ratio):
    # 读取原始图像
    img = cv2.imread(source)

    # 获取原始图像尺寸
    height, width = img.shape[:2]

    # 计算新的目标尺寸，保持2:3比例
    if width / height > width_ratio / height_ratio:
        new_width = width
        new_height = int(width * height_ratio / width_ratio)
    else:
        new_height = height
        new_width = int(height * width_ratio / height_ratio)

    # 调整图像大小
    resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # 创建空白画布
    padded = np.ones((new_height, new_width, 3), dtype=np.uint8) * 255

    # 计算偏移量
    dx = (width - new_width) // 2
    dy = (height - new_height) // 2

    # 将调整后的图像复制到空白画布上
    padded[dy:dy + new_height, dx:dx + new_width] = resized

    # 保存调整后的图像
    cv2.imwrite(output, resized)


if __name__ == '__main__':
    resize('/Users/ipaperplane/Downloads/back.jpg', '/Users/ipaperplane/Downloads/back1.jpg', 1, 1)
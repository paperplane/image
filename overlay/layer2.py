import cv2
import numpy as np


def read(foreground, background):
    fore = cv2.imread(foreground)
    back = cv2.imread(background)

    mask = np.ones(fore.shape[:2], dtype=np.uint8) * 255

    result = cv2.seamlessClone(fore, back, mask, (100,100), cv2.NORMAL_CLONE)


def overlay(fore_im, back_im):
    # 计算居中位置
    x = (back_im.shape[1] - fore_im.shape[1]) // 2
    y = (back_im.shape[0] - fore_im.shape[0]) // 2

    # 创建一个与背景图片大小相同的透明层
    layer = np.zeros(back_im.shape, dtype=np.uint8)

    # 将前景图片置于背景透明层中心位置
    layer[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = fore_im[:, :, :3]

    # 图片叠加
    mask = fore_im[:, :, :3] if fore_im.shape[2] == 4 else None
    if mask is not None:
        mask = cv2.resize(mask, (fore_im.shape[1], fore_im.shape[0]))
        mask_inv = cv2.bitwise_not(mask)

        bg_roi = back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]]
        bg_roi = cv2.bitwise_and(bg_roi, bg_roi, mask=mask_inv)

        fg = cv2.bitwise_and(layer[y:y + fore_im.shape[0], x:x + fore_im.shape[1]],
                             layer[y:y + fore_im.shape[0], x:x + fore_im.shape[1]], mask=mask)
        dst = cv2.add(bg_roi, fg)
        back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = dst
    else:
        back_im = cv2.addWeighted(back_im, 1, layer, 0, 0)

    cv2.imshow('Result', back_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    fore, back = read('/Users/ipaperplane/Downloads/less_is_more.png', '/Users/ipaperplane/Downloads/background.jpg')
    overlay(fore, back)

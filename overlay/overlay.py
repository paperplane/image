import cv2


def overlay(foreground, background):
    fore_im = cv2.imread(foreground, cv2.IMREAD_UNCHANGED)
    back_im = cv2.imread(background)

    bh, bw = back_im.shape[:2]
    fh, fw = fore_im.shape[:2]

    if bw / bh > fw / fh:
        n_fh = int(bh * 0.8)
        n_fw = int(bh * 0.8 * fw / fh)
    else:
        n_fw = int(bw * 0.8)
        n_fh = int(bw * 0.8 * fh / fw)
    fore_im = cv2.resize(fore_im, (n_fw, n_fh))

    # 计算居中位置
    x = (back_im.shape[1] - fore_im.shape[1]) // 2
    y = (back_im.shape[0] - fore_im.shape[0]) // 2

    # 将前景图片置于背景中心
    back_im[y:y + fore_im.shape[0], x:x + fore_im.shape[1]] = fore_im[:, :, :3]

    name, suffix = foreground.split('.')
    output = name + '-M' + '.' + suffix
    cv2.imwrite(output, back_im)


if __name__ == '__main__':
    overlay('/Users/ipaperplane/Downloads/less_is_more.jpg', '/Users/ipaperplane/Downloads/background.jpg')

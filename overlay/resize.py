import os
import cv2


def resize():
    source_path = "/Users/bytedance/Downloads/opts/"
    files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]
    for file in files:
        if file.endswith('-M-2.jpg'):
            continue
        # Decode the image data into a format OpenCV can work with
        file_path = os.path.join(source_path, file)
        fore_im = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if fore_im is not None:
            print(file_path, fore_im.shape[:2])
            fh, fw = fore_im.shape[:2]
            new_fore_im = cv2.resize(fore_im, (int(fw*0.6), int(fh*0.6)))

            target_path = "/Users/bytedance/Downloads/debug/"
            cv2.imwrite(os.path.join(target_path, file), new_fore_im)


def read():
    source_path = "/Users/bytedance/Downloads/debug/"
    files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]
    for file in files:
        if file.endswith('-M-2.jpg'):
            continue
        # Decode the image data into a format OpenCV can work with
        file_path = os.path.join(source_path, file)
        fore_im = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if fore_im is not None:
            print(fore_im.shape[:2])

if __name__ == '__main__':
    # read()
    resize()
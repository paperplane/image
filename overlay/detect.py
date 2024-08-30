import cv2


def detect(background):
    # 读取图像
    image = cv2.imread(background)

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 应用高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 计算轮廓的周长
        perimeter = cv2.arcLength(contour, True)

        # 近似轮廓
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # 检查是否为矩形
        if len(approx) == 4:
            # 绘制矩形框
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)

    cv2.imshow('Detected Frame', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detect('/Users/bytedance/Documents/back1.png')
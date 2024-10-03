import cv2
import numpy as np
from sklearn.cluster import KMeans


def cv_show(img, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)


def preprocess_image(frame):
    # 转换到HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 图像平滑去噪
    blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

    return blurred


def find_contours_by_color(hsv, lower_color, upper_color):
    # 根据颜色范围创建掩码
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # 找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def vision01(frame, pts1):
    # 透视变换
    pts2 = np.float32([[0, 0], [500, 0], [500, 500], [0, 500]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    trans = cv2.warpPerspective(frame, matrix, (500, 500))
    cv_show(trans, 'Demo0')

    # 图像预处理
    preprocessed = preprocess_image(trans)

    # 定义颜色的HSV阈值范围
    color_ranges = {
        'red': ([0, 160, 100], [10, 200, 160]),
        'green': ([70, 150, 100], [80, 240, 180]),
        'blue': ([90, 95, 140], [110, 177, 180]),
        'orange': ([4, 130, 50], [9, 160, 255]),
        'yellow': ([25, 50, 50], [40, 255, 255]),
        'white': ([80, 0, 200], [140, 10, 220]),
    }

    # 为每种颜色找到轮廓
    contours_by_color = {}
    for color, (lower, upper) in color_ranges.items():
        contours = find_contours_by_color(preprocessed, np.array(lower), np.array(upper))
        contours_by_color[color] = contours

    # 显示轮廓
    for color, contours in contours_by_color.items():
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(trans, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv_show(trans, 'Contours')

    # 将图像转换为二维数组，每个像素点是一个颜色特征
    Z = preprocessed.reshape((-1, 3))

    # 将数组类型转换为float32
    Z = np.float32(Z)

    # 执行K-means聚类
    kmeans = KMeans(n_clusters=6, random_state=0).fit(Z)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    # 将结果转换回uint8类型
    centers = np.uint8(centers)

    # 映射聚类结果到魔方的每个面上
    board = np.zeros((3, 3), dtype=int)
    width = trans.shape[1] // 3
    height = trans.shape[0] // 3

    for i in range(3):
        for j in range(3):
            # 为每个小块创建掩码
            mask = (Z[:, 0] >= i * width) & (Z[:, 0] < (i + 1) * width) & \
                   (Z[:, 1] >= j * height) & (Z[:, 1] < (j + 1) * height)
            # 应用掩码并确定颜色
            cluster_colors = centers[labels[mask]]
            # 找到最频繁的颜色索引
            color_index = np.argmax(np.bincount(labels[mask], minlength=6))
            board[i, j] = color_index

    # 显示聚类结果
    result = centers[labels].reshape((500, 500, 3))
    cv_show(result, 'K-means Clustering')

    return board, contours_by_color


if __name__ == '__main__':
    # 读取图像
    img = cv2.imread('v11.jpg')
    if img is None:
        print("Error: Unable to load image. Please check the path.")
        exit()

    # 定义四个点的坐标
    pts1 = np.float32([[342, 145], [445, 260], [335, 365], [230, 255]])

    # 调用vision01函数
    board, contours_by_color = vision01(img, pts1)

    # 打印九宫格的颜色
    colors = ['白', '红', '蓝', '绿', '黄', '橙']
    for i in range(3):
        for j in range(3):
            print(colors[board[i][j]], end=" ")
        print()
    print()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
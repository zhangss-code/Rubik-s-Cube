import cv2
import numpy as np

# 全局变量来存储区域的HSV平均值
hsv_average = {'h': 0, 's': 0, 'v': 0}

# 定义矩形区域的点
rect = (0, 0, 0, 0)
ref_point = (0, 0)

def get_average_hsv_value(event, x, y, flags, param):
    global ref_point, rect, hsv_average

    # 当左键被按下时
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = (x, y)

    # 当左键被释放时
    elif event == cv2.EVENT_LBUTTONUP:
        rect = (ref_point[0], ref_point[1], x - ref_point[0], y - ref_point[1])
        hsv_average = calculate_average_hsv(x, y, rect)
        print("Average HSV value in selected region: H: {}, S: {}, V: {}".format(hsv_average['h'], hsv_average['s'], hsv_average['v']))

def calculate_average_hsv(x, y, rect):
    # 确保矩形区域的宽度和高度是正数
    rect = (rect[0], rect[1], max(0, rect[2]), max(0, rect[3]))
    roi = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

    # 将图像从BGR转换到HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # 计算HSV的平均值
    h_sum = s_sum = v_sum = 0
    h_count = 0
    for i in range(roi.shape[0]):
        for j in range(roi.shape[1]):
            h, s, v = hsv[i, j]
            h_sum += h
            s_sum += s
            v_sum += v
            h_count += 1

    # 计算平均值
    h_avg = int(h_sum / h_count) if h_count else 0
    s_avg = int(s_sum / h_count)
    v_avg = int(v_sum / h_count)

    return {'h': h_avg, 's': s_avg, 'v': v_avg}

# 读取图像
img = cv2.imread('v11.jpg')  # 替换为你的图像路径
if img is None:
    print("Error: Unable to load image. Please check the path.")
    exit()

# 创建一个窗口
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# 设置鼠标回调函数
cv2.setMouseCallback('image', get_average_hsv_value)

# 显示图像
cv2.imshow('image', img)

# 等待直到用户按下'q'键
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 打印选择区域的HSV平均值
print("Selected region's average HSV value: H: {}, S: {}, V: {}".format(hsv_average['h'], hsv_average['s'], hsv_average['v']))

# 关闭所有窗口
cv2.destroyAllWindows()
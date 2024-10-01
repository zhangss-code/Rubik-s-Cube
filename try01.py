import cv2

# 创建VideoCapture对象，参数为0表示使用本地摄像头
# 初始化摄像头

cap = cv2.VideoCapture(0)# 前置为0，1为后置摄像头


print(cap.isOpened())
# 处理每一帧
while True:
    # 从摄像头中读取一帧图像
    ret, frame = cap.read()
    # 没有读到直接退出
    if ret is None:
        break

    # 显示图像
    cv2.imshow('Local Camera', frame)
    cv2.waitKey(1)
    cv2.imwrite('v11.jpg', frame)



    # 按下q键退出程序
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()

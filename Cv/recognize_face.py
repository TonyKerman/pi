import cv2 as cv


def StaticDetect(filename):
    """静态图像"""
    # 创建一个级联分类器 加载一个 .xml 分类器文件. 它既可以是Haar特征也可以是LBP特征的分类器.
    face_cascade = cv.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

    # 加载图像
    img = cv.imread(filename)
    # 转换为灰度图
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 进行人脸检测，传入scaleFactor，minNegihbors，分别表示人脸检测过程中每次迭代时图像的压缩率以及
    # 每个人脸矩形保留近似数目的最小值
    # 返回人脸矩形数组
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
    for (x, y, w, h) in faces:
        # 在原图像上绘制矩形
        img = cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv.namedWindow('Face Detected！')
    cv.imshow('Face Detected！', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def FaceDetect():
    '''
    打开摄像头，读取帧，检测帧中的人脸，扫描检测到的人脸中的眼睛，对人脸绘制蓝色的矩形框，对人眼绘制绿色的矩形框
    '''
    # 创建一个级联分类器 加载一个 .xml 分类器文件. 它既可以是Haar特征也可以是LBP特征的分类器.
    face_cascade = cv.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_eye.xml')

    # 打开摄像头
    camera = cv.VideoCapture(0)
    cv.namedWindow('Face')

    while True:
        # 读取一帧图像
        ret, frame = camera.read()
        # 判断图片读取成功
        if ret:
            gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # 人脸检测
            faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
            for (x, y, w, h) in faces:
                # 在原图像上绘制矩形
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray_img[y:y + h, x:x + w]
                # 眼睛检测
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.03, 5, 0, (40, 40))
                for (ex, ey, ew, eh) in eyes:
                    cv.rectangle(frame, (ex + x, ey + y), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

            cv.imshow('Face', frame)

            # 使程序停留，等待任意键按下，参数表示停留的时间，0表示无限长
            k = cv.waitKey(0)

            # 按下ESC键（ASCII码为27）后，销毁所有窗口，终止程序
            if k == 27:
                break

    camera.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    filename = 'face.png'
    #StaticDetect(filename)
    FaceDetect()

import cv2 as cv





if __name__ == "__main__":
    print('wait')
    cap = cv.VideoCapture(0)
    # width, height = 600, 600
    # cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    print('begin')
    try:
        while True:
            ret, frame = cap.read()
            # img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # 旋转
            img = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
            # cv.imshow("img", img)
            cv.imshow("frame", img)
            input = cv.waitKey(20)
            if input == ord("q"):
                break
    except Exception:
        pass
    print('over')
    cap.release()
    cv.destroyAllWindows()

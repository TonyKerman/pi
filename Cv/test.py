import cv2 as cv


def main():
    while True:
        ret, frame = cap.read()
        img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("img", img)
        cv.imshow("frame", frame)
        input = cv.waitKey(20)
        if input == ord("q"):
            break


if __name__ == "__main__":
    print('wait')
    cap = cv.VideoCapture(1)
    width, height = 1280, 960
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    print('begin')
    try:
        main()
    except Exception:
        pass
    print('over')
    cap.release()
    cv.destroyAllWindows()

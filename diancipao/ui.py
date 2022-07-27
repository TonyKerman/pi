import cv2 as cv
import math
import cmath
COLOR_MAP = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'red': (0, 0, 255),
    'white': (255, 255, 255)
}


def ui(frame, width=0, height=0,text='0'):
    x0 = int(width / 2)
    y0 = int(height / 2)
    # 准星
    l = 15
    p =(
        (int(x0 - l), y0), (int(x0 + l), y0),
        (x0, int(y0 - l)), (x0,  int(y0 + 280))
    )

    cv.line(frame, pt1=p[0], pt2=p[1], color=COLOR_MAP['white'])
    cv.line(frame, pt1=p[2], pt2=p[3], color=COLOR_MAP['white'])
    #外侧两个1/4圆
    for i in range(360):
        if i % 2 != 0:
            continue
        if 45 < i < 135 or 225 < i < 315  :
            continue
        l = 180
        if i % 45 == 0:
            dl = 10
        else:
            dl = 5
        arc = math.radians(i)
        y1 = round((l-dl) * math.sin(arc) + y0)
        x1 = round((l-dl) * math.cos(arc) + x0)
        y2 = round((l+dl) * math.sin(arc) + y0)
        x2 = round((l + dl) * math.cos(arc) + x0)
        cv.line(frame, pt1=(x1,y1), pt2=(x2,y2), color=COLOR_MAP['green'])
        #数据
        font=cv.FONT_HERSHEY_SIMPLEX
        cv.putText(img=frame,text=text, org=(x0-150, y0), fontFace=font, fontScale=0.5, color=COLOR_MAP['red'])

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    width, height = 1280, 720
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    while True:
        ret, frame = cap.read()
        ui(frame, width, height)
        cv.imshow('frame', frame)
        input = cv.waitKey(20)
        if input == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()

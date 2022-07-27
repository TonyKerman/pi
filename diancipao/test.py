import matplotlib.pyplot as plt
import math

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# 0.准备数据
val = {97.9: 595, 95.8: 645, 98.9: 610, 106: 400,
       94.6: 690, 90.5: 785, 84.1: 910, 88.1: 855,
       107: 370, 114: 138, 85.3: 910, 95.3: 685,
       93.0: 750, 103: 530, 90.9: 775, 115: 220,
       96.7: 720, 101: 580, 108: 365, 113: 245,
       105: 425, 104: 425, 111: 200, 110: 235,
       96.1: 670, 109: 255, 116: 40, 113: 215,
       88.6: 800, 96.7: 635, 112: 190, 117: -4,
       114: 200, 136: 70, 120: 580, 125: 410,
       123: 480, 124: 520, 130: 385, 127: 440,
       132: 320, 133: 280, 138: 60, 140: -20

       }
x = [k for k in val.keys()]
x.sort()
Y = []
V = []
Ek = []
bjv = 0
ajv = 0
for i in x:
    if i < 120:
        s = 1315 - val[i]
    else:
        s = 2020 - val[i]
    s = s / 1000
    Y.append(s)
    g = 9.80
    v = math.sqrt(2 * g * s)
    V.append(v)
    e = 0.5 * 0.004 * (v ** 2)
    Ek.append(e)


def fitting(xs=[], ys=[]):
    global bj, aj, R
    xb = sum(xs) / len(xs)
    yb = sum(ys) / len(ys)
    s = 0
    s1 = 0
    s2 = 0
    for i in range(len(xs)):
        s += xs[i] * ys[i]
        s1 += (xs[i] ** 2)

    bj = (len(xs) * s - sum(xs) * sum(ys)) / (len(xs) * s1 - sum(xs) ** 2)
    aj = yb - bj * xb


if __name__ == '__main__':
    # 1
    plt.subplot(2, 2, 1)
    plt.plot(x, Y)  # 实际折线
    fitting(x, Y)
    yl = [84 * bj + aj, 140 * bj + aj]
    plt.plot([84, 140], yl, color='r', label='拟合')  # 回归直线
    plt.legend(loc="best")  # 显示图例
    plt.xlabel('电压/V', fontsize=14)
    plt.ylabel('射程/m', fontsize=14)
    plt.xticks(range(84, 140, 3))  # x刻度
    plt.grid(True, linestyle='--', alpha=0.5)  # 网格

    # 2
    plt.subplot(2, 2, 2)
    plt.plot(x, V)
    u = [math.sqrt(i) for i in x]
    fitting(u, V)
    bjv =bj
    ajv = aj
    print(bjv, ajv)
    xl = range(84, 140)
    yl = [math.sqrt(i) * bj + aj for i in xl]
    plt.plot(xl, yl, color='r', label='拟合')  # 回归曲线
    plt.legend(loc="best")  # 显示图例
    plt.xlabel('电压/V', fontsize=14)
    plt.ylabel('初速度/ m/s', fontsize=14)
    plt.xticks(range(84, 140, 3))
    plt.grid(True, linestyle='--', alpha=0.5)

    # 3
    plt.subplot(2, 2, 3)
    plt.plot(x, Ek)
    fitting(x, Ek)
    yl = [84 * bj + aj, 140 * bj + aj]
    plt.plot([84, 140], yl, color='r', label='拟合')  # 回归直线
    plt.legend(loc="best")  # 显示图例
    plt.xlabel('电压/V', fontsize=14)
    plt.ylabel('动能/ j', fontsize=14)
    plt.xticks(range(84, 140, 3))
    plt.grid(True, linestyle='--', alpha=0.5)

    # 3.图像显示
    plt.show()

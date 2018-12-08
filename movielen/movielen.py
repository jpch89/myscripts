# -*- coding: utf-8 -*-
# @Author: jpch89
# 打包命令：
"""
pyinstaller --add-data="img\电影.png;img" --add-data="ffprobe.exe;." -i="img\电影.ico" -Fw movielen.py
"""

# man ffprobe 查看ffprobe的帮助文档

import subprocess
import re
import os
import sys
from PyQt5 import sip
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QFont

exts = ['.avi', '.mp4', '.mkv', '.flv']
exts += [i.upper() for i in exts]
version = 'v0.0.4'


# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath('.')
#     print(base_path)
#     print(relative_path)
#     abs_path = os.path.join(base_path, relative_path)
#     print(abs_path)
#     return abs_path


# 另外一种写法
def resource_path(relative_path):
    '''定义一个返回绝对路径的函数'''
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def get_length(filepath):
    # pyinstaller找不到资源的修改
    ffprobe_path = resource_path('ffprobe')
    cmd = '%s "%s"' % (ffprobe_path, filepath)

    # 不进行资源重定向
    # cmd = 'ffprobe "%s"' % filepath

    # pyinstaller使用Popen时的修改
    # si = subprocess.STARTUPINFO()
    # si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # 推测：
    # 在REPL的输出是stderr标准错误输出
    # 如果把标准错误输出归并到标准输出的话
    # 调用命令就不会在REPL有输出了
    # 因为标准输出需要显式的读取出来
    # sp = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True, startupinfo = si)
    sp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # print(sp.stdout.read().decode('gbk'))
    results = sp.stdout.readlines()
    for result in results:
        # print(result.decode('utf-8'))
        if b"Duration" in result:
            result = result.decode('utf-8')
            break

    pattern = r'Duration: (\d*:\d*:\d*\.\d*), start'
    durations = re.search(pattern, result).group(1)
    durations = durations.split(':')
    durations = list(map(float, durations))
    return durations


# 注意int(a)不是四舍五入，是简单截断
def get_hms(total_len):
    quotient, remainder = divmod(total_len[2], 60)
    total_len[1] += quotient
    total_len[2] = remainder
    quotient, remainder = divmod(total_len[1], 60)
    total_len[0] += quotient
    total_len[1] = remainder

    return total_len


def is_movie(file):
    filename, ext = os.path.splitext(file)
    if ext in exts:
        return True
    else:
        return False


def get_total_len():
    total_len = [0.0, 0.0, 0.0]
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if is_movie(file):
                count += 1
                filepath = os.path.join(root, file)
                durations = get_length(filepath)
                for i in range(3):
                    total_len[i] += durations[i]

    # 测试代码：通过！
    # file = 'test.mp4'
    # total_len = get_length(file)
    # total_len = get_hms(total_len)
    # return(total_len)
    # 测试代码结束

    total_len = get_hms(total_len)
    total_len[0] = int(total_len[0])
    total_len[1] = int(total_len[1])
    total_len[2] = round(total_len[2], 2)
    return count, total_len


class MovieLen(QWidget):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.setWindowTitle(' '.join(['MovieLen', version]))
        self.setWindowIcon(QIcon(resource_path(r'img\电影.png')))
        self.resize(400, 160)
        self.label = QLabel(self)
        self.label.setText(msg)
        self.label.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        self.label.move(20, 50)
        self.show()


if __name__ == '__main__':
    count, total_len = get_total_len()

    msg1 = '共有%d个视频文件' % count
    print(msg1)
    msg1 += '\n'

    msg2 = '总时长：%s小时%s分%s秒' % (total_len[0], total_len[1], total_len[2])
    print(msg2)

    msg = msg1 + msg2

    # GUI
    app = QApplication(sys.argv)
    # 注意
    # 写成movielen = MovieLen()而不是直接MovieLen()
    # 否则的话窗口创建之后没有引用
    # 导致一闪而过
    movielen = MovieLen()
    sys.exit(app.exec_())

# 更新日志
# v0.0.1
# 20180722016
# 加入 resource_path 函数之后单文件不再报错！

# v0.0.2
# 201807222221
# 修复使用 pyinstaller 的 -w 参数报错！

# v0.0.3
# 201810302214
# 添加对 .flv 文件的支持

# v0.0.4
# 201812080947
# 添加对大写扩展名的支持

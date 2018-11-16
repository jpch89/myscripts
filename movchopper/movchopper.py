# 官网 https://pypi.org/project/moviepy/
# 文档 http://zulko.github.io/moviepy/

from moviepy.editor import *

while True:
    start = input('请输入起始秒数：')
    end = input('请输入结束秒数：')
    try:
        start = int(start)
        end = int(end)
    except Exception:
        print('输入错误，请重新输入！')
        continue
    if start > end:
        print('起始秒数大于结束秒数！')
        print('请重新输入！')
    elif start < 0:
        print('起始秒数小于 0，请重新输入！')
    elif end < 0:
        print('结束秒数小于 0，请重新输入！')
    else:
        break

file = input('请输入文件名：')
name, ext = file.split('.')
clip = VideoFileClip(file).subclip(start, end)
new_file = name + '_edited.' + ext
clip.write_videofile(new_file)

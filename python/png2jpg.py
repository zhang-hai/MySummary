import cv2
import os
import numpy as np

path = "./"
# 该文件夹下所有的文件（包括文件夹）
filelist = os.listdir(path)
count = 1

for file in filelist:   # 遍历所有文件
    Olddir = os.path.join(path, file)   # 原来的文件路径
    # 如果是文件文件 && 是.png文件进行转换
    if os.path.isfile(file) and file.endswith(".png"):
        # 文件名
        str = file.rsplit(".", 1)
        if not os.path.exists("jpg"):
            os.mkdir("jpg")
        # 转换后的格式
        output = "jpg/"+str[0] + ".jpg"
        print(output)
        image = cv2.imread(file,cv2.IMREAD_COLOR)
        # 按比例缩小为原来的0.5倍
        # image = cv2.resize(image,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(output,image,[cv2.IMWRITE_JPEG_QUALITY, 60])
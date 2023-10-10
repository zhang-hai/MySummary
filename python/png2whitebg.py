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
        if not os.path.exists("new"):
            os.mkdir("new")
        # 转换后的格式
        output = "new/"+str[0] + ".png"
        print(output)
        image = cv2.imread(file,cv2.IMREAD_COLOR) 
        
        # 图像进行反转：白变黑，黑变白
        # 灰度处理
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 图像进行反转：白变黑，黑变白
        # ret,binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        dst = 255 - gray
        ret2, binary2 = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)

        cv2.imwrite(output,binary2,[cv2.IMWRITE_PNG_COMPRESSION, 3])

        # 白底转透明色
        # image = cv2.imread(output) 
        # # Point 1: 生成与白色部分对应的mask图像
        # mask = np.all(image[:,:,:] == [255, 255, 255], axis=-1)
        # # Point 2: 将图片从三通道转为四通道
        # dst = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        # # Point3:  以mask图像为基础，使白色部分透明化
        # dst[mask,3] = 0

        # # 压缩到原有质量的80%
        # cv2.imwrite(output,dst,[cv2.IMWRITE_PNG_COMPRESSION, 3])
"""
Created on Thu Mar 12 09:47:04 2020

@author: LX
"""
import netCDF4 as nc
import numpy as np
import cv2
# import pyexiv2
# from pyexiv2 import Image
import PIL.Image as IImage
import sys
import colorsys

JXBJ = np.array(
    [[255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 1, 1, 1, 255, 255, 255, 255, 255, 255],
     [255, 255, 255, 255, 255, 255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 255, 255, 255, 255, 255, 255],
     [255, 255, 255, 255, 255, 255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 255, 255, 255, 255, 255, 255],
     [255, 255, 255, 255, 255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 1, 255, 255, 255, 255, 255, 255],
     [255, 255, 255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 255, 255, 255],
     [255, 255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 255],
     [255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 255, 255, 255],
     [1, 1, 1, 1, 255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 255, 255, 255, 255],
     [255, 255, 1, 255, 255, 255, 255, 255, 255, 1, 1, 1, 1, 1, 1, 1, 1, 255, 255, 255, 255, 255],
     [255, 255, 255, 255, 255, 255, 255, 255, 255, 1, 1, 1, 1, 1, 255, 255, 255, 255, 255, 255, 255, 255]])


def pre_day(pr_data, time_data, time_start):  # 获取20点降水数据
    pre_day = []
    h = int(time_start[8:10])
    for i in range(len(time_data)):
        if (time_data[i] + h) % 24 == 20:
            pre_day.append(pr_data[i])
    return pre_day


def Ww12_day_day(Ww12_data, time_data, time_start):  # 获取20点天气数据
    Ww12_day = []
    h = int(time_start[8:10])
    for i in range(len(time_data)):
        if (time_data[i] + h) % 24 == 20:
            Ww12_day.append(Ww12_data[i])
    return Ww12_day


def transparent_back(img):  # 增加背景隐藏
    img = img.convert("RGBA")
    L, H = img.size
    color_0 = (0, 0, 0, 255)
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            #            print(dot)
            color_1 = img.getpixel(dot)
            #            if color_1 == color_0:
            #                color_1 = color_1[:-1] + (0,)
            #                img.putpixel(dot, (0, 0, 0, 0))
            #            else:
            #                color_1 = color_1[:-1] + (128,)
            #                img.putpixel(dot,color_1)
            if color_1 != color_0 and JXBJ[h, l] != 255:
                color_1 = color_1[:-1] + (128,)
                img.putpixel(dot, color_1)
            else:
                img.putpixel(dot, (0, 0, 0, 0))
    return img


def several_rain(
        pr_data, Ww12_data, time_data, time_start, pr_Threshold, step, weather, outputname
):  # 计算连阴雨指数
    pre_data_day = pre_day(pr_data, time_data, time_start)
    Ww12_day = Ww12_day_day(Ww12_data, time_data, time_start)
    H, W = pre_data_day[0].shape
    new_im = np.zeros((H, W, 3))
    HSV_color = colorsys.rgb_to_hsv(255, 185, 66)  # 规定色彩转HSV
    lianyinyu = False
    for i in range(H):
        for j in range(W):
            #            print('percent   '+str(round((i*W+j)/(H*W)*100,4))+'%')
            number_day = 0
            HSV_V = HSV_color[2]
            for k in range(15 - step):
                #                print('percent   '+str(round((i*W+j)/(H*W)*100,4))+'%')
                pre_4 = []
                Ww12_4 = []
                for l in range(step):
                    pre_4.append(pre_data_day[k + l][i, j])
                    Ww12_4.append(Ww12_day[k + l][i, j])

                if (
                        len([pre for pre in pre_4 if pre > pr_Threshold]) >= step
                        and len([Ww for Ww in Ww12_4 if Ww in weather]) >= step
                ):
                    number_day = number_day + 1  # 计算连续天数
                    lianyinyu = True
                    HSV_V = HSV_V - 10  # 修改颜色亮度
            if number_day != 0:
                RGB_color = colorsys.hsv_to_rgb(
                    HSV_color[0], HSV_color[1], HSV_V
                )  # HSV转RGB
                new_im[i, j, 0] = RGB_color[0]
                new_im[i, j, 1] = RGB_color[1]
                new_im[i, j, 2] = RGB_color[2]
    fnjh_out = new_im
    fnjh_out = fnjh_out.astype(np.float32)
    #    fnjh_out = cv2.resize(fnjh_out, (440, 340), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(outputname, fnjh_out)
    # print("*******Calculate complete！*******")
    return lianyinyu


def coordinate(lat_data, lon_data):  # 获取数据地理范围
    lef_up = (lon_data[0], lat_data[-1])
    rig_do = (lon_data[-1], lat_data[0])
    coo = [lef_up, rig_do]
    return coo


if __name__ == "__main__":
    filename = sys.argv[1]
    pr_Threshold = float(sys.argv[2])
    step = int(sys.argv[3])
    outputname = sys.argv[4]

    #    filename = r"C:\Users\LX\Desktop\11111\zngxjx\111\2019061710.nc"  # .nc文件名
    #    outputname = r"C:\Users\LX\Desktop\11111\zngxjx\111\lianyinyu.png"
    #    pr_Threshold = 0.1  # 输入阈值
    #    step = 4
    weather = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, ]  # 天气现象列表

    f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

    pr = "Pr24"
    pr_data = f[pr][:]  # 获取变量的数据
    pr_data = np.array(pr_data)  # 转化为np.array数组

    Ww12 = "Ww12"
    Ww12_data = f[Ww12][:]
    Ww12_data = np.array(Ww12_data)  # 转化为np.array数组

    tim = f.variables["time"]
    units = tim.units
    units_time = units.split(" ")
    time_start = units_time[-1]

    time = "time"
    time_data = f[time][:]
    time_data = np.array(time_data)

    lat = "lat"
    lat_data = f[lat][:]
    lat_data = np.array(lat_data)

    lon = "lon"
    lon_data = f[lon][:]
    lon_data = np.array(lon_data)

    lianyinyu = several_rain(
        pr_data,
        Ww12_data,
        time_data,
        time_start,
        pr_Threshold,
        step,
        weather,
        outputname,
    )
    coo = coordinate(lat_data, lon_data)
    img1 = IImage.open(outputname)
    img1 = transparent_back(img1)
    img1 = img1.resize((440, 340))
    img1.save(outputname)
    print(lianyinyu)

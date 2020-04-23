# -*- coding: utf-8 -*-
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
import colorsys
import sys

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


def num2time(time_data, time_start):  # 区分日期
    h = int(time_start[8:10])
    labels = np.zeros(15)
    for i in range(len(time_data)):
        for j in range(15):
            if (time_data[i] + h) / 24 <= (j + 1):
                labels[j] = i
    label = np.zeros(16) + 1
    label[1:16] = labels + 1
    label_c = []
    for k in range(len(label) - 1):
        label_c.append((label[k], label[k + 1]))
    return label_c


def hour_to_day(hdata, label):  # 根据nc文件中的小时数据，得出每日平均数据
    H, W = hdata.shape[1:]
    mean = np.zeros((H, W))
    startHour = int(label[0])
    endHour = int(label[1])
    start = startHour
    if startHour == 1:
        startHour = 0
    while startHour < endHour:
        mean = hdata[startHour] + mean
        startHour += 1
    mean_day = mean / (endHour - start)

    return mean_day


def T_mean_day(te_data, label):  # 返回15天平均温度
    tem_mean = []
    for i in range(len(label)):
        temp_t = hour_to_day(te_data, label[i])
        tem_mean.append(temp_t)
    return tem_mean


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


def seedling_rotting(
        te_data,
        pr_data,
        Ww12_data,
        time_data,
        time_start,
        te_Threshold,
        pr_Threshold,
        step,
        weather,
        outputname,
):  # 计算烂秧指数
    label = num2time(time_data, time_start)
    tem_mean_day = T_mean_day(te_data, label)
    pre_data_day = pre_day(pr_data, time_data, time_start)
    Ww12_day = Ww12_day_day(Ww12_data, time_data, time_start)
    H, W = tem_mean_day[0].shape
    new_im = np.zeros((H, W, 3))
    HSV_color = colorsys.rgb_to_hsv(196, 234, 0)  # 规定色彩转HSV
    seedling = False
    for i in range(H):
        for j in range(W):
            number_day = 0
            HSV_V = HSV_color[2]
            for k in range(15 - step):
                tem_4 = []
                pre_4 = []
                Ww12_4 = []

                for l in range(step):
                    tem_4.append(tem_mean_day[k + l][i, j])
                    pre_4.append(pre_data_day[k + l][i, j])
                    Ww12_4.append(Ww12_day[k + l][i, j])

                if (
                        len([tem for tem in tem_4 if tem < te_Threshold]) >= step
                        and len([pre for pre in pre_4 if pre > pr_Threshold]) >= step
                        and len([Ww for Ww in Ww12_4 if Ww in weather]) >= step
                ):
                    number_day = number_day + 1  # 计算连续天数
                    seedling = True
                    HSV_V = HSV_V - 10  # 修改颜色亮度
            #            print(HSV_V)
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
    return seedling


def coordinate(lat_data, lon_data):  # 获取数据地理范围
    lef_up = (lon_data[0], lat_data[-1])
    rig_do = (lon_data[-1], lat_data[0])
    coo = [lef_up, rig_do]
    return coo


def data_read(filename):
    f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息
    pr = "Pr24"
    pr_data = f[pr][:]  # 获取变量的数据
    pr_data = np.array(pr_data)  # 转化为np.array数组

    te = "T"
    te_data = f[te][:]  # 获取变量的数据
    te_data = np.array(te_data)

    Ww12 = "Ww12"
    Ww12_data = f[Ww12][:]
    Ww12_data = np.array(Ww12_data)  # 转化为np.array数组

    tim = f.variables["time"]  # 获取起始时间数据
    units = tim.units
    units_time = units.split(" ")
    time_start = units_time[-1]

    time = "time"  # 获取时间数据
    time_data = f[time][:]
    time_data = np.array(time_data)

    lat = "lat"  # 获取经纬度数据
    lat_data = f[lat][:]
    lat_data = np.array(lat_data)

    lon = "lon"
    lon_data = f[lon][:]
    lon_data = np.array(lon_data)

    return (pr_data, te_data, Ww12_data, time_start, time_data, lat_data, lon_data)


if __name__ == "__main__":
    filename = sys.argv[1]
    pr_Threshold = float(sys.argv[2])
    te_Threshold = float(sys.argv[3])
    step = int(sys.argv[4])
    outputname = sys.argv[5]

    #    filename = r"C:\Users\LX\Desktop\11111\zngxjx\111\2019061710.nc"  # .nc文件名
    #    outputname = r"C:\Users\LX\Desktop\11111\zngxjx\111\lanyang.png"
    #    pr_Threshold = 0.1  # 输入降雨阈值
    #    te_Threshold = 23  # 温度阈值
    #    step = 2  # 连续天数阈值
    weather = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, ]  # 天气现象列表
    pr_data, te_data, Ww12_data, time_start, time_data, lat_data, lon_data = data_read(
        filename
    )
    seedling = seedling_rotting(
        te_data,
        pr_data,
        Ww12_data,
        time_data,
        time_start,
        te_Threshold,
        pr_Threshold,
        step,
        weather,
        outputname,
    )  # 烂秧算法调用，seedling返回值是否存在烂秧
    coo = coordinate(lat_data, lon_data)  # 经纬度数据获取
    img1 = IImage.open(outputname)  # 背景透明化
    img1 = transparent_back(img1)
    img1 = img1.resize((440, 340))
    img1.save(outputname)

    print(seedling)

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 09:47:04 2020

@author: LX
"""
import netCDF4 as nc
import numpy as np
import cv2


filename = r'C:\Users\LX\Desktop\zngxjx\nc\2019110110.nc'   # .nc文件名
pr_Threshold = 50  # 输入阈值
te_Threshold = 12
step = 4
weather = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
           14, 15, 16, 17, 19, 21, 22, 2, 24, 25, 26, 27, 28]


f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

pr = 'Pr24'
pr_data = f[pr][:]  # 获取变量的数据
pr_data = np.array(pr_data)  # 转化为np.array数组

te = 'T'
te_data = f[te][:]  # 获取变量的数据
te_data = np.array(te_data)

Ww12 = 'Ww12'
Ww12_data = f[Ww12][:]
Ww12_data = np.array(Ww12_data)  # 转化为np.array数组

tim = f.variables['time']
units = tim.units
units_time = units.split(' ')
time_start = units_time[-1]

time = 'time'
time_data = f[time][:]
time_data = np.array(time_data)


def num2time(time_data, time_start):  # 区分日期
    h = int(time_start[8:10])
    labels = np.zeros(15)
    for i in range(len(time_data)):
        for j in range(15):
            if (time_data[i]+h)/24 <= (j+1):
                labels[j] = i
    label = np.zeros(16)+1
    label[1:16] = labels+1
    label_c = []
    for k in range(len(label)-1):
        label_c.append((label[k], label[k+1]))
    return(label_c)


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

    return (mean_day)


def T_mean_day(te_data, label):  # 返回15天平均温度
    tem_mean = []
    for i in range(len(label)):
        temp_t = hour_to_day(te_data, label[i])
        tem_mean.append(temp_t)
    return(tem_mean)


def pre_day(pr_data, time_data, time_start):
    pre_day = []
    h = int(time_start[8:10])
    for i in range(len(time_data)):
        if (time_data[i]+h) % 24 == 20:
            pre_day.append(pr_data[i])
    return(pre_day)


def Ww12_day_day(Ww12_data, time_data, time_start):
    Ww12_day = []
    h = int(time_start[8:10])
    for i in range(len(time_data)):
        if (time_data[i]+h) % 24 == 20:
            Ww12_day.append(Ww12_data[i])
    return(Ww12_day)


def run(te_data, pr_data, Ww12_data, time_data, time_start, te_Threshold, pr_Threshold, step, weather):
    label = num2time(time_data, time_start)
    tem_mean_day = T_mean_day(te_data, label)
    pre_data_day = pre_day(pr_data, time_data, time_start)
    Ww12_day = Ww12_day_day(Ww12_data, time_data, time_start)
    H, W = tem_mean_day[0].shape
    new_im = np.zeros((H, W))
    tem_4 = []
    pre_4 = []
    Ww12_4 = []
    for i in range(H):
        for j in range(W):
            for k in range(15-step):
                for l in range(step):
                    print('percent   '+str(round((i*W+j)/(H*W)*100, 4))+'%')
                    tem_4.append(tem_mean_day[k+l][i, j])
                    pre_4.append(pre_data_day[k+l][i, j])
                    Ww12_4.append(Ww12_day[k+l][i, j])
                    if [tem for tem in tem_4 if tem > te_Threshold] or [pre for pre in pre_4 if pre < pr_Threshold] or not[Ww for Ww in Ww12_4 if Ww in weather]:
                        new_im[i, j] = 255
    fnjh_out = new_im
    fnjh_out = fnjh_out.astype(np.float32)
    fnjh_out = cv2.resize(fnjh_out, (440, 340),
                          interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(r'C:\Users\LX\Desktop\zngxjx\output/2.png', fnjh_out)

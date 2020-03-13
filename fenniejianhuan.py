# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import cv2

filename = 'C:/Users/Zn/Desktop/WORK/2019120516.nc'   # .nc文件名
f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

var = 'TMax24'
var_data = f[var][:]  # 获取变量的数据
var_data = np.array(var_data)  # 转化为np.array数组

# Threshold = 30 #设置阈值
Threshold = input("设置阈值：")  # 输入分蘖减缓阈值
Threshold = int(Threshold)

TMax_day1 = var_data[3][:]  # 第1天最高温度
TMax_day2 = var_data[27][:]  # 第2天最高温度
TMax_day3 = var_data[51][:]  # 第3天最高温度
TMax_day4 = var_data[57][:]  # 第4天最高温度
TMax_day5 = var_data[61][:]  # 第5天最高温度
TMax_day6 = var_data[65][:]  # 第6天最高温度
TMax_day7 = var_data[69][:]  # 第7天最高温度
TMax_day8 = var_data[73][:]  # 第8天最高温度
TMax_day9 = var_data[77][:]  # 第9天最高温度
TMax_day10 = var_data[81][:]  # 第10天最高温度
TMax_day11 = var_data[83][:]  # 第11天最高温度
TMax_day12 = var_data[85][:]  # 第12天最高温度
TMax_day13 = var_data[87][:]  # 第13天最高温度
TMax_day14 = var_data[89][:]  # 第14天最高温度
TMax_day15 = var_data[91][:]  # 第15天最高温度

fnjh_day1 = ((TMax_day1 < Threshold)+0)
fnjh_day2 = ((TMax_day2 < Threshold)+0)
fnjh_day3 = ((TMax_day3 < Threshold)+0)
fnjh_day4 = ((TMax_day4 < Threshold)+0)
fnjh_day5 = ((TMax_day5 < Threshold)+0)
fnjh_day6 = ((TMax_day6 < Threshold)+0)
fnjh_day7 = ((TMax_day7 < Threshold)+0)
fnjh_day8 = ((TMax_day8 < Threshold)+0)
fnjh_day9 = ((TMax_day9 < Threshold)+0)
fnjh_day10 = ((TMax_day10 < Threshold)+0)
fnjh_day11 = ((TMax_day11 < Threshold)+0)
fnjh_day12 = ((TMax_day12 < Threshold)+0)
fnjh_day13 = ((TMax_day13 < Threshold)+0)
fnjh_day14 = ((TMax_day14 < Threshold)+0)
fnjh_day15 = ((TMax_day15 < Threshold)+0)

fnjh_sum = fnjh_day1 + fnjh_day2 + fnjh_day3 + fnjh_day4 + fnjh_day5 + fnjh_day6 + fnjh_day7 + \
    fnjh_day8 + fnjh_day9 + fnjh_day10 + fnjh_day11 + \
    fnjh_day12 + fnjh_day13 + fnjh_day14 + fnjh_day15
fnjh_final = ((fnjh_sum > 10)+0)

fnjh_out = fnjh_final * 255
fnjh_out = fnjh_out.astype(np.float32)
fnjh_out = cv2.resize(fnjh_out, (440, 340), interpolation=cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/fnjh/1.png', fnjh_out)

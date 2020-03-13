# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import cv2

filename = 'C:/Users/Zn/Desktop/WORK/2019120516.nc'   # .nc文件名
f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

var = 'Pr24'
var_data = f[var][:]  # 获取变量的数据
var_data = np.array(var_data)  # 转化为np.array数组
Threshold = 50  # 输入阈值

Pr_day = var_data[3][:]  # 当天24h累计降水
by_day = ((Pr_day >= Threshold)+0)

by_out = by_day * 255
by_out = by_out.astype(np.float32)
by_out = cv2.resize(by_out, (440, 340), interpolation=cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/by/1.png', by_out)

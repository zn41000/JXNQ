# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import datetime
import time
import cv2

filename = 'C:/Users/Zn/Desktop/WORK/2019120516.nc'   # .nc文件名
f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

var = 'Pr24'
var_data = f[var][:]  # 获取变量的数据
var_data = np.array(var_data)  # 转化为np.array数组
threshold = 50  # 输入阈值


def getTimeValue(self):

    dateTimeNumList = []  # 准备存储time的值
    dateTimeUnits = ''  # 准备记录初始时间
    for key in self.variables.keys():  # 在变量中筛选出time变量的全部信息
        if key.lower() in ['time', 't']:
            dateTimeNumList = self.variables[key][:]  # 获取time字段全部值
            dateTimeUnits = self.variables[key].units  # 获取初始时间信息
            break

    dateTimeStrList = []  # 该列表存储真实日期字符串
    dayValueList = []  # 该列表存储日值数据对应的time字段值

    # dateTimeUnits = 'hours since yyyymmddhhmmss'
    startDateTimeStr = ' '.join(dateTimeUnits.split()[-1:])  # -1提取日期

    stdt = datetime.datetime.strptime(
        startDateTimeStr, '%Y%m%d%H%M%S')  # stdt=真实起始时间

    if dateTimeUnits.split()[0] == 'hours':  # 0提取计时单位
        for dtn in dateTimeNumList:  # 逐一提取time字段值
            dt = stdt + datetime.timedelta(hours=dtn)  # 真实时间 = 起始时间 + 时间差
            ymdH = dt.strftime('%Y-%m-%d')  # 生成真实日期字符串
            H = dt.strftime('%H')  # 生成真实时间值
            dateTimeStrList.append(ymdH)

            # 取出每日20点的time字段值，并存入列表
            if int(H) % 24 == 20:
                dayValueList.append(dtn)

    # 分别返回：真实日期列表，逐日time值列表，全部time值列表
    return dateTimeStrList, dayValueList, dateTimeNumList


today = getTimeValue(f)[1][0]  # 准备获取time数据对应下标
today_in = np.argwhere(getTimeValue(f)[2] == today)  # today_in为np格式浮点数
today_out = int(today_in[0])  # 转化为int整数

Pr_day = var_data[today_out][:]  # 当天24h累计降水
baoyu_day = np.where(Pr_day > threshold, 1, 0)

baoyu_out = baoyu_day * 255
baoyu_out = baoyu_out.astype(np.float32)
baoyu_out = cv2.resize(baoyu_out, (440, 340), interpolation=cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/baoyu/baoyu.png', baoyu_out)

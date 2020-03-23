# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import datetime
import time
import cv2
import pyexiv2
from pyexiv2 import Image
import PIL.Image as IImage

if __name__ == '__main__':
    # filename = sys.argv[1]
    # out_imgpath = sys.argv[2]
    # out_txtpath = sys.argv[3]
    # threshold = sys.argv[4]

    filename = 'C:/Users/Zn/Desktop/WORK/2019120516.nc'   # 输入.nc文件名
    out_imgpath = 'C:/Users/Zn/Desktop/WORK/diwen/diwen.png'  # 输出图像路径
    out_txtpath = 'C:/Users/Zn/Desktop/WORK/diwen/alert.txt'  # 输出文件路径
    threshold = 20  # 输入阈值

    f = nc.Dataset(filename)  # 读取.nc文件，传入f中

    var_max = 'TMax24'
    var_max_data = f[var_max][:]  # 获取变量的数据
    var_max_data = np.array(var_max_data)  # 转化为np.array数组

    var_min = 'TMin24'
    var_min_data = f[var_min][:]  # 获取变量的数据
    var_min_data = np.array(var_min_data)  # 转化为np.array数组

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

    # 获取日值数据对应下标
    timelist = getTimeValue(f)[1]
    daylist = []
    for day in timelist:
        day_in = np.argwhere(getTimeValue(f)[2] == day)  # week_in为np格式浮点数
        day_out = int(day_in[0])  # 转化为int整数
        daylist.append(day_out)
    print(daylist)

    # 获取15天的日值数据
    TMax_daylist = []
    for d in daylist:
        TMax_daylist.append(var_max_data[d][:])
    print(np.shape(TMax_daylist))

    TMin_daylist = []
    for d in daylist:
        TMin_daylist.append(var_min_data[d][:])
    print(np.shape(TMin_daylist))

    # 获取日均值数据
    Tmean_list = (np.array(TMax_daylist) - np.array(TMin_daylist)) / 2

    diwen_ez = []
    for i in range(15):
        condition = np.where(Tmean_list[i][:] < threshold, 1, 0)  # 根据阈值二值化
        diwen_ez.append(condition)  # 存入二值数据
    diwen_ez = np.array(diwen_ez)  # 便于后续计算

    print(type(diwen_ez))
    print(np.shape(diwen_ez))

    diwen_list = []  # 用于将15天二值数据每三天求和，然后储存
    diwen_mark = []  # 记录每一次出现满足预警条件的日期下标
    diwen_condition = np.zeros((17, 22))  # 判断连续3天条件

    for x in range(13):
        diwen_condition = diwen_ez[x][:] + diwen_ez[x+1][:] + diwen_ez[x+2][:]
        diwen_list.append(diwen_condition)
        if np.max(diwen_condition) == 3:
            diwen_mark_in = np.argwhere(
                getTimeValue(f)[2] == getTimeValue(f)[1][x])
            diwen_mark.append(int(diwen_mark_in[0]))

    print(diwen_mark)

    print(np.shape(diwen_list))

    diwen_days = []  # 记录出现满足预警条件的日期
    for mark in diwen_mark:
        diwen_days.append(getTimeValue(f)[0][mark])

    print(diwen_days)

    # 记录预警日期到文件中
    with open(out_txtpath, 'w+') as fp:
        thisday = getTimeValue(f)[0][0]
        str_today = "今天的日期为：" + thisday + "\n"
        str_alert = "出现低温预警的日期有：\n"
        fp.write(str_today)
        fp.write(str_alert)
        for line in diwen_days:
            fp.writelines(line+'\n')
        fp.close()

    dw_alert_sum = np.zeros((17, 22))
    for diwen in np.array(diwen_list, dtype=int):
        dw_alert = np.where(diwen > 2, 1, 0)  # 根据出现预警的次数二值化
        dw_alert_sum += dw_alert  # 叠加总次数为一张图（一个点最多出现13次）

    # 出图
    dw_alert_sum = dw_alert_sum * 19  # 范围（0,1）
    dw_alert_sum = dw_alert_sum.astype(np.uint8)
    dw_alert_sum = cv2.resize(dw_alert_sum, (440, 340),
                              interpolation=cv2.INTER_NEAREST)
    img_rgba = cv2.cvtColor(dw_alert_sum, cv2.COLOR_GRAY2RGBA)
    img_rgba[:, :, 3] = dw_alert_sum
    img_rgba[:, :, 0] = 180
    img_rgba[:, :, 1] = 0
    img_rgba[:, :, 2] = 194
    cv2.imwrite(out_imgpath, img_rgba)

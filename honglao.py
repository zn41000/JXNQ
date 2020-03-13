# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import cv2

filename = 'C:/Users/Zn/Desktop/ncdata/2019110110.nc'   # .nc文件名
f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

var_Pr, var_time = 'Pr24', 'time'
var_data_Pr, var_data_time = f[var_Pr][:], f[var_time][:]  # 获取变量的数据

var_info = f.variables[var_time].units  # 获取变量信息
print(var_info)

var_data_Pr, var_data_time = np.array(
    var_data_Pr), np.array(var_data_time)  # 转化为np.array数组
Threshold1 = 100  # 输入阈值(每天)
Threshold2 = 150  # 输入阈值(每3天)
Threshold3 = 200  # 输入阈值(每5天)
print(var_data_time)
dayarg1 = 9


# def timectrl():
#     global dayarg1
#     Pr_daylist = []
#     for i in var_data_time:
#         if int(i) == dayarg1:
#             Pr_daylist.append(i)
#             dayarg1 += 24
#             print(dayarg1)
#             print(np.argwhere(var_data_time == dayarg1))
#     print(Pr_daylist)


# timectrl()

def getTimeValue(self):

    dateTimeNumList = []
    dateTimeUnits = ''
    for key in self.f.variables.keys():
        if key.lower() in ['time', 't']:
            dateTimeNumList = self.f.variables[key][:]
            dateTimeUnits = self.f.variables[key].units
            break

    dateTimeStrList = []  # 该序列每个元素都是时间直观的字符串
    # -1是时间,-2是日期,'2000-01-01 00:00:00'
    startDateTimeStr = ' '.join(dateTimeUnits.split()[-2:])
    stdt = datetime.datetime.strptime(startDateTimeStr,
                                      '%Y-%m-%d %H:%M:%S')
    if dateTimeUnits.split()[0] == 'hours':
        for dtn in dateTimeNumList:
            dt = stdt + datetime.timedelta(hours=dtn)  # type is datetime
            ymd = dt.strftime('%Y-%m-%d')
            dateTimeStrList.append(ymd)
            # DIFF存放没有12点数据的日期，则取15点或9点的
            # if ymd in DIFF5 and dtn % 24 == 15:
            #     self.dateFlagList.append(True)
            #     print(ymd)
            # else:
            #     self.dateFlagList.append(False)
            # 只提取某天12点的数据
            if dtn % 24 == 12:
                self.dateFlagList.append(True)
            else:
                self.dateFlagList.append(False)

    return dateTimeStrList

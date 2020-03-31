# def hour_to_day (hdata,startHour,endHour):  # 根据nc文件中的小时数据，得出每日平均数据
#     mean = np.zeros((17,22))
newvariable876 = startHour
#     while startHour <= endHour:
#         mean = hdata[startHour::] + mean
#         startHour += 1
#     else:
#         mean = mean / (d - i + 1)
#     print(mean)

# hour_to_day (var_data,0,2)

import netCDF4 as nc
import numpy as np
import datetime
import time

filename = "C:/Users/Zn/Desktop/ncdata/2019110110.nc"  # .nc文件名
f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息


def getTimeValue(self):

    dateTimeNumList = []  # 准备存储time的值
    dateTimeUnits = ""  # 准备记录初始时间
    for key in self.variables.keys():  # 在变量中筛选出time变量的全部信息
        if key.lower() in ["time", "t"]:
            dateTimeNumList = self.variables[key][:]  # 获取time字段全部值
            dateTimeUnits = self.variables[key].units  # 获取初始时间信息
            break

    dateTimeStrList = []  # 该列表存储真实日期字符串
    dayValueList = []  # 该列表存储日值数据对应的time字段值

    # dateTimeUnits = 'hours since yyyymmddhhmmss'
    startDateTimeStr = " ".join(dateTimeUnits.split()[-1:])  # -1提取日期

    stdt = datetime.datetime.strptime(startDateTimeStr, "%Y%m%d%H%M%S")  # stdt=真实起始时间

    if dateTimeUnits.split()[0] == "hours":  # 0提取计时单位
        for dtn in dateTimeNumList:  # 逐一提取time字段值
            dt = stdt + datetime.timedelta(hours=dtn)  # 真实时间 = 起始时间 + 时间差
            ymdH = dt.strftime("%Y-%m-%d")  # 生成真实日期字符串
            H = dt.strftime("%H")  # 生成真实时间值
            dateTimeStrList.append(ymdH)

            # 取出每日20点的time字段值，并存入列表
            if int(H) % 24 == 20:
                dayValueList.append(dtn)

    return dateTimeStrList, dayValueList


print(getTimeValue(f)[0])
print(getTimeValue(f)[1])

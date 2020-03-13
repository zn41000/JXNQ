# import numpy as np
# a = np.array([True, False])
# print(a)
# print(a + 0)


# def hour_to_day (hdata,startHour,endHour):  # 根据nc文件中的小时数据，得出每日平均数据
#     mean = np.zeros((17,22))
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

filename = 'C:/Users/Zn/Desktop/ncdata/2019110110.nc'   # .nc文件名
f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息


def getTimeValue(self):

    dateTimeNumList = []  # 准备存储time的值
    dateTimeUnits = ''  # 准备记录初始时间
    for key in self.variables.keys():  # 在变量中筛选出time变量的全部信息
        if key.lower() in ['time', 't']:
            dateTimeNumList = self.variables[key][:]  # 获取time字段全部值
            # 获取初始时间信息 'since yyyymmddhhmmss'
            dateTimeUnits = self.variables[key].units
            break

    dateTimeStrList = []  # 该列表每个元素都是时间直观的字符串
    # -1提取日期,'hours since yyyymmddhhmmss'
    startDateTimeStr = ' '.join(dateTimeUnits.split()[-1:])
    print(dateTimeUnits.split()[:])
    print(startDateTimeStr)

    stdt = datetime.datetime.strptime(startDateTimeStr, '%Y%m%d%H%M%S')
    if dateTimeUnits.split()[0] == 'hours':
        for dtn in dateTimeNumList:
            dt = stdt + datetime.timedelta(hours=dtn)  # type is datetime
            ymd = dt.strftime('%Y-%m-%d')

            dateTimeStrList.append(ymd)
            # DIFF存放没有20点数据的日期，则取15点或9点的
            # if ymd in DIFF5 and dtn % 24 == 15:
            #     self.dateFlagList.append(True)
            #     print(ymd)
            # else:
            #     self.dateFlagList.append(False)
            # 只提取某天20点的数据
            # if dtn % 24 == 20:
            #     self.dateFlagList.append(True)
            # else:
            #     self.dateFlagList.append(False)

    return dateTimeStrList


print(getTimeValue(f))

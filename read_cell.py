# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import datetime
import time

filename = "C:/Users/Zn/Desktop/WORK/2019120516.nc"  # .nc文件路径
f = nc.Dataset(filename)  # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

var_lat, var_lon, var_TMax24, var_TMin24, var_Ww12 = (
    "lat",
    "lon",
    "TMax24",
    "TMin24",
    "Ww12",
)
var_lat_data, var_lon_data, var_TMax24_data, var_TMin24_data, var_Ww12_data = (
    f[var_lat][:],
    f[var_lon][:],
    f[var_TMax24][:],
    f[var_TMin24][:],
    f[var_Ww12][:],
)  # 获取变量的数据
var_lat_data, var_lon_data, var_TMax24_data, var_TMin24_data, var_Ww12_data = (
    np.array(var_lat_data),
    np.array(var_lon_data),
    np.array(var_TMax24_data),
    np.array(var_TMin24_data),
    np.array(var_Ww12_data),
)  # 转化为np.array数组
var_lon_data, var_lat_data = (
    np.around(var_lon_data, decimals=2),
    np.around(var_lat_data, decimals=2),
)  # 将经纬度数据统一保留两位小数
print("经度可选项(保留两位小数):", var_lon_data)
print("纬度可选项(保留两位小数):", var_lat_data)
# 根据输入经纬度获取对应点坐标
x = input("请输入经度:")
y = input("请输入纬度:")
lon_in = np.argwhere(var_lon_data == float(x))
lat_in = np.argwhere(var_lat_data == float(y))
# print("读取输入的经纬度对应下标：", lon_in, lat_in)
lon_out, lat_out = int(lon_in[0]), int(lat_in[0])
# print("输入的经纬度对应下标分别是：", lon_out, lat_out)


def findcell(x, y, attribute):  # 规定统一函数，传入定位参数，输出所需位置的属性值
    attribute_day1 = attribute[3][y][x]
    attribute_day2 = attribute[27][y][x]
    attribute_day3 = attribute[51][y][x]
    attribute_day4 = attribute[57][y][x]
    attribute_day5 = attribute[61][y][x]
    attribute_day6 = attribute[65][y][x]
    attribute_day7 = attribute[69][y][x]
    week = [
        attribute_day1,
        attribute_day2,
        attribute_day3,
        attribute_day4,
        attribute_day5,
        attribute_day6,
        attribute_day7,
    ]
    return week


TMax_week = findcell(lon_out, lat_out, var_TMax24_data)
TMin_week = findcell(lon_out, lat_out, var_TMin24_data)
Ww_week = findcell(lon_out, lat_out, var_Ww12_data)

Ww_week = np.array(Ww_week)
Ww_week = Ww_week.astype(np.int32)

weather = {
    0: "晴",
    1: "多云",
    2: "阴",
    3: "阵雨",
    4: "雷阵雨",
    5: "雷阵雨并伴有冰雹",
    6: "雨夹雪",
    7: "小雨",
    8: "中雨",
    9: "大雨",
    10: "暴雨",
    11: "大暴雨",
    12: "特大暴雨",
    13: "阵雪",
    14: "小雪",
    15: "中雪",
    16: "大雪",
    17: "暴雪",
    18: "雾",
    19: "冻雨",
    20: "沙尘暴",
    21: "小到中雨",
    22: "中到大雨",
    23: "大到暴雨",
    24: "暴雨到大暴雨",
    25: "大暴雨到特大暴雨",
    26: "小到中雪",
    27: "中到大雪",
    28: "大到暴雪",
    29: "浮尘",
    30: "扬沙",
    31: "强沙尘暴",
    32: "尚未编码",
    33: "尚未编码",
    34: "尚未编码",
    35: "尚未编码",
    36: "尚未编码",
    37: "尚未编码",
    38: "尚未编码",
    39: "尚未编码",
    40: "尚未编码",
    41: "尚未编码",
    42: "尚未编码",
    43: "尚未编码",
    44: "尚未编码",
    45: "尚未编码",
    46: "尚未编码",
    47: "尚未编码",
    48: "尚未编码",
    49: "尚未编码",
    50: "尚未编码",
    51: "尚未编码",
    52: "尚未编码",
    53: "霾",
}
Ww_week = [weather[x] if x in weather else x for x in Ww_week]


print("一周最高气温：", TMax_week)
print("一周最低气温：", TMin_week)
print("一周天气现象：", Ww_week)

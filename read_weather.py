# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import datetime


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

    # 分别返回：真实日期列表，逐日time值列表，全部time值列表
    return dateTimeStrList, dayValueList, dateTimeNumList


if __name__ == "__main__":
    # filename = sys.argv[1]
    # xlon = sys.argv[2]
    # ylat = sys.argv[3]

    filename = "C:/Users/Zn/Desktop/WORK/2019120516.nc"  # .nc文件路径

    # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息
    f = nc.Dataset(filename)
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

    # print("经度可选项(保留两位小数):", var_lon_data)
    # print("纬度可选项(保留两位小数):", var_lat_data)

    # 获取一星期time数据对应下标
    daylist = getTimeValue(f)[1]
    week = daylist[:7]
    weeklist = []
    for day in week:
        week_in = np.argwhere(getTimeValue(f)[2] == day)  # week_in为np格式浮点数
        week_out = int(week_in[0])  # 转化为int整数
        weeklist.append(week_out)

    # 根据输入经纬度获取对应点坐标
    xlon = input("请输入经度:")
    ylat = input("请输入纬度:")
    lon_in = np.argwhere(var_lon_data == float(xlon))
    lat_in = np.argwhere(var_lat_data == float(ylat))
    lon_out, lat_out = int(lon_in[0]), int(lat_in[0])

    def findcell(t, x, y, attribute):  # 传入定位下标参数与目标属性，输出所需位置的属性值
        attribute_week = []
        for i in t:
            attribute_day = attribute[i][y][x]
            attribute_week.append(attribute_day)

        return attribute_week

    TMax_week = findcell(weeklist, lon_out, lat_out, var_TMax24_data)
    TMin_week = findcell(weeklist, lon_out, lat_out, var_TMin24_data)
    Ww_week = findcell(weeklist, lon_out, lat_out, var_Ww12_data)

    Ww_week = np.array(Ww_week)
    Ww_week = Ww_week.astype(np.int32)

    # weather = {
    #     0: "晴",
    #     1: "多云",
    #     2: "阴",
    #     3: "阵雨",
    #     4: "雷阵雨",
    #     5: "雷阵雨并伴有冰雹",
    #     6: "雨夹雪",
    #     7: "小雨",
    #     8: "中雨",
    #     9: "大雨",
    #     10: "暴雨",
    #     11: "大暴雨",
    #     12: "特大暴雨",
    #     13: "阵雪",
    #     14: "小雪",
    #     15: "中雪",
    #     16: "大雪",
    #     17: "暴雪",
    #     18: "雾",
    #     19: "冻雨",
    #     20: "沙尘暴",
    #     21: "小到中雨",
    #     22: "中到大雨",
    #     23: "大到暴雨",
    #     24: "暴雨到大暴雨",
    #     25: "大暴雨到特大暴雨",
    #     26: "小到中雪",
    #     27: "中到大雪",
    #     28: "大到暴雪",
    #     29: "浮尘",
    #     30: "扬沙",
    #     31: "强沙尘暴",
    #     32: "尚未编码",
    #     33: "尚未编码",
    #     34: "尚未编码",
    #     35: "尚未编码",
    #     36: "尚未编码",
    #     37: "尚未编码",
    #     38: "尚未编码",
    #     39: "尚未编码",
    #     40: "尚未编码",
    #     41: "尚未编码",
    #     42: "尚未编码",
    #     43: "尚未编码",
    #     44: "尚未编码",
    #     45: "尚未编码",
    #     46: "尚未编码",
    #     47: "尚未编码",
    #     48: "尚未编码",
    #     49: "尚未编码",
    #     50: "尚未编码",
    #     51: "尚未编码",
    #     52: "尚未编码",
    #     53: "霾",
    # }
    # Ww_week = [weather[x] if x in weather else x for x in Ww_week]

    print(
        "Max_temperature_week:",
        TMax_week,
        "/Min_temperature_week:",
        TMin_week,
        "/Weather_week:",
        Ww_week,
    )

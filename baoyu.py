# -*- coding: UTF-8 -*-
# 导入nc库
import netCDF4 as nc
import numpy as np
import datetime
import cv2


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


def imgout(img_in, scatter, red, green, blue, img_out):  # 出图
    img_gray = img_in * scatter  # 离散扩大到最大值为255
    img_gray = img_gray.astype(np.uint8)
    img_gray_rsz = cv2.resize(img_gray, (440, 340), interpolation=cv2.INTER_NEAREST)
    img_rgba = cv2.cvtColor(img_gray_rsz, cv2.COLOR_GRAY2RGBA)
    img_rgba[:, :, 3] = img_gray_rsz  # Alpha通道
    img_rgba[:, :, 0] = blue  # B通道
    img_rgba[:, :, 1] = green  # G通道
    img_rgba[:, :, 2] = red  # R通道
    cv2.imwrite(img_out, img_rgba)


def disaster(img):  # 判断是否出现灾情
    if np.max(img) > 0:
        print(True)
    else:
        print(False)


if __name__ == "__main__":
    # filename = sys.argv[1]
    # out_imgpath = sys.argv[2]
    # threshold = sys.argv[3]

    filename = "C:/Users/Zn/Desktop/WORK/2019120516.nc"  # .nc文件名
    out_imgpath = "C:/Users/Zn/Desktop/WORK/baoyu/baoyu.png"  # 输出图像路径
    threshold = 50  # 输入阈值

    # 读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息
    f = nc.Dataset(filename)
    var = "Pr24"
    var_data = f[var][:]  # 获取变量的数据
    var_data = np.array(var_data)  # 转化为np.array数组

    # 提取当天数据
    today = getTimeValue(f)[1][0]  # 准备获取time数据对应下标
    today_in = np.argwhere(getTimeValue(f)[2] == today)  # today_in为np格式浮点数
    today_out = int(today_in[0])  # 下标转化为int整数
    Pr_day = var_data[today_out][:]  # 当天24h累计降水
    baoyu_day = np.where(Pr_day >= threshold, 1, 0)  # 二值化

    # 判断灾情
    disaster(baoyu_day)

    # 出图
    imgout(baoyu_day, 255, 0, 27, 235, out_imgpath)

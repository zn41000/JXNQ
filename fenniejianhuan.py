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


def imgout(img_in, scatter, red, green, blue, alpha, img_out):  # 出图
    img_channel = cv2.resize(img_in, (440, 340), interpolation=cv2.INTER_NEAREST)
    img_gray = img_in * scatter  # 离散扩大到最大值为255
    img_gray = img_gray.astype(np.uint8)
    img_gray_rsz = cv2.resize(img_gray, (440, 340), interpolation=cv2.INTER_NEAREST)
    img_rgba = cv2.cvtColor(img_gray_rsz, cv2.COLOR_GRAY2RGBA)
    img_rgba[:, :, 3] = alpha * msk_rsz  # Alpha通道
    img_rgba[:, :, 0] = blue * img_channel  # B通道
    img_rgba[:, :, 1] = green * img_channel  # G通道
    img_rgba[:, :, 2] = red * img_channel  # R通道
    cv2.imwrite(img_out, img_rgba)


def disaster(img):  # 判断是否出现灾情
    if np.max(img) > 0:
        print(True)
    else:
        print(False)


if __name__ == "__main__":
    # filename = sys.argv[1]
    # out_imgpath = sys.argv[2]
    # threshold1 = sys.argv[3]
    # threshold2 = sys.argv[4]
    # alpha_val = sys.argv[5]

    filename = "C:/Users/Zn/Desktop/WORK/2019120516.nc"  # .nc文件名
    out_imgpath = "C:/Users/Zn/Desktop/WORK/fnjh/fnjh.png"  # 输出图像路径
    threshold1 = 30  # 设置阈值（气温）
    threshold2 = 10  # 设置阈值（天数）
    alpha_val = 128  # 输入透明程度(0-255)

    alpha_mask = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                           [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
    msk_rsz = cv2.resize(alpha_mask, (440, 340), interpolation=cv2.INTER_NEAREST)

    f = nc.Dataset(filename)  # 读取.nc文件，传入f中

    var = "TMax24"
    var_data = f[var][:]  # 获取变量的数据
    var_data = np.array(var_data)  # 转化为np.array数组

    # 获取日值数据对应下标
    timelist = getTimeValue(f)[1]
    daylist = []
    for day in timelist:
        day_in = np.argwhere(getTimeValue(f)[2] == day)  # week_in为np格式浮点数
        day_out = int(day_in[0])  # 转化为int整数
        daylist.append(day_out)
    # print(daylist)

    # 获取15天的日值数据
    TMax_daylist = []
    for d in daylist:
        TMax_daylist.append(var_data[d][:])
    # print(np.shape(TMax_daylist))

    fnjh_ez = []
    for i in range(15):
        condition = np.where(TMax_daylist[i][:] < threshold1, 1, 0)  # 根据阈值二值化
        fnjh_ez.append(condition)  # 存入二值数据
    fnjh_ez = np.array(fnjh_ez)  # 便于后续计算

    fnjh_sum = np.zeros((17, 22))
    for fnjh in np.array(fnjh_ez, dtype=int):
        fnjh_sum += fnjh  # 叠加总次数为一张图（一个点最多出现15次）
    fnjh_final = np.where(fnjh_sum > threshold2, 1, 0)  # 根据出现预警的次数二值化为一张图

    # 判断灾情
    disaster(fnjh_final)

    # 出图
    imgout(fnjh_final, 255, 61, 119, 255, alpha_val, out_imgpath)

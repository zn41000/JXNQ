# -*- coding: UTF-8 -*-
#导入nc库
import netCDF4 as nc
import numpy as np
# from PIL import Image
# import matplotlib
# import matplotlib.pyplot as pyplot
# from scipy import misc
#import imageio
import cv2

filename = 'C:/Users/Zn/Desktop/WORK/2019120516.nc'   # .nc文件名
f = nc.Dataset(filename)   #读取.nc文件，传入f中。此时f包含了该.nc文件的全部信息

var = 'T'
var_info = f.variables[var]   #获取变量信息
var_data = f[var][:]   #获取变量的数据
print(var_info)
#print(var_data.shape)  

#很方便转化为array数组
#print(type(var_data))    #<class 'numpy.ma.core.MaskedArray'>  .nc文件的变量数组都为Masked array
var_data = np.array(var_data)  #转化为np.array数组
# print(var_data[0][0][0])
# print(var_data[1][0][0])
# #print(var_data[2][0][0])
# print((var_data[0][0][0] + var_data[1][0][0])/2)
#print(var_data[0][0][0] / var_data[1][0][0])

def hour_to_day (hdata,startHour,endHour):  # 根据nc文件中的小时数据，得出每日平均数据
    mean = np.zeros((17,22))
    start = startHour
    while startHour <= endHour:
        mean = hdata[startHour][:] + mean
        #  print("table:", startHour)
        #print(mean)
        startHour += 1
    mean_day = mean / (endHour - start + 1)
    #  print(endHour - start + 1)
    return mean_day

day1 = hour_to_day (var_data,0,14) #第1天日均温度
day2 = hour_to_day (var_data,15,38) #第2天日均温度
day3 = hour_to_day (var_data,39,54) #第3天日均温度
day4 = hour_to_day (var_data,55,58) #第4天日均温度
day5 = hour_to_day (var_data,59,62) #第5天日均温度
day6 = hour_to_day (var_data,63,66) #第6天日均温度
day7 = hour_to_day (var_data,67,70) #第7天日均温度
day8 = hour_to_day (var_data,71,74) #第8天日均温度
day9 = hour_to_day (var_data,75,78) #第9天日均温度
day10 = hour_to_day (var_data,79,81) #第10天日均温度
day11 = hour_to_day (var_data,82,83) #第11天日均温度
day12 = hour_to_day (var_data,84,85) #第12天日均温度
day13 = hour_to_day (var_data,86,87) #第13天日均温度
day14 = hour_to_day (var_data,88,89) #第14天日均温度
day15 = hour_to_day (var_data,90,91) #第15天日均温度
# print((day1<9)+0)
# print(((day1<9)+0)+0)
QJDW_1=((day1<9)+0)+((day2<9)+0)+((day3<9)+0)
DW1 = ((QJDW_1>2)+0)
print(DW1)
DW_out1=DW1 *85
DW_out1 = DW_out1.astype(np.float32)
DW_out1 = cv2.resize(DW_out1,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day1.png',DW_out1)

QJDW_2=((day2<9)+0)+((day3<9)+0)+((day4<9)+0)
DW2 = ((QJDW_2>2)+0)

DW_out2=DW2 *85
DW_out2 = DW_out2.astype(np.float32)
DW_out2 = cv2.resize(DW_out2,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day2.png',DW_out2)

QJDW_3=((day3<9)+0)+((day4<9)+0)+((day5<9)+0)
DW3 = ((QJDW_3>2)+0)

DW_out3=DW3 *85
DW_out3 = DW_out3.astype(np.float32)
DW_out3 = cv2.resize(DW_out3,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day3.png',DW_out3)

QJDW_4=((day4<9)+0)+((day5<9)+0)+((day6<9)+0)
DW4 = ((QJDW_4>2)+0)

DW_out4=DW4 *85
DW_out4 = DW_out4.astype(np.float32)
DW_out4 = cv2.resize(DW_out4,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day4.png',DW_out4)

QJDW_5=((day5<9)+0)+((day6<9)+0)+((day7<9)+0)
DW5 = ((QJDW_5>2)+0)

DW_out5=DW5 *85
DW_out5 = DW_out5.astype(np.float32)
DW_out5 = cv2.resize(DW_out5,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day5.png',DW_out5)

QJDW_6=((day6<9)+0)+((day7<9)+0)+((day8<9)+0)
DW6 = ((QJDW_6>2)+0)

DW_out6=DW6 *85
DW_out6 = DW_out6.astype(np.float32)
DW_out6 = cv2.resize(DW_out6,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day6.png',DW_out6)

QJDW_7=((day7<9)+0)+((day8<9)+0)+((day9<9)+0)
DW7 = ((QJDW_7>2)+0)

DW_out7=DW7 *85
DW_out7 = DW_out7.astype(np.float32)
DW_out7 = cv2.resize(DW_out7,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day7.png',DW_out7)


QJDW_8=((day8<9)+0)+((day9<9)+0)+((day10<9)+0)
DW8 = ((QJDW_8>2)+0)

DW_out8=DW8 *85
DW_out8 = DW_out8.astype(np.float32)
DW_out8 = cv2.resize(DW_out8,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day8.png',DW_out8)

QJDW_9=((day9<9)+0)+((day10<9)+0)+((day11<9)+0)
DW9 = ((QJDW_9>2)+0)

DW_out9=DW9 *85
DW_out9 = DW_out9.astype(np.float32)
DW_out9 = cv2.resize(DW_out9,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day9.png',DW_out9)

QJDW_10=((day10<9)+0)+((day11<9)+0)+((day12<9)+0)
DW10 = ((QJDW_10>2)+0)

DW_out10=DW10 *85
DW_out10 = DW_out10.astype(np.float32)
DW_out10 = cv2.resize(DW_out10,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day10.png',DW_out10)

QJDW_11=((day11<9)+0)+((day12<9)+0)+((day13<9)+0)
DW11 = ((QJDW_11>2)+0)

DW_out11=DW11 *85
DW_out11 = DW_out11.astype(np.float32)
DW_out11 = cv2.resize(DW_out11,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day11.png',DW_out11)

QJDW_12=((day12<9)+0)+((day13<9)+0)+((day14<9)+0)
DW12 = ((QJDW_12>2)+0)

DW_out12=DW12 *85
DW_out12 = DW_out12.astype(np.float32)
DW_out12 = cv2.resize(DW_out12,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day12.png',DW_out12)

QJDW_13=((day13<9)+0)+((day14<9)+0)+((day15<9)+0)
DW13 = ((QJDW_13>2)+0)

DW_out13=DW13 *85
DW_out13 = DW_out13.astype(np.float32)
DW_out13 = cv2.resize(DW_out13,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/day13.png',DW_out13)

QJDW_sum = DW1 + DW2 + DW3 + DW4 + DW5 + DW6 + DW7 + DW8 + DW9 + DW10 + DW11 + DW12 +DW13
# print(QJDW_sum)
QJDW_sum=QJDW_sum *85
print(QJDW_sum)
QJDW_sum2 = QJDW_sum.astype(np.float32)
QJDW_sum3 = cv2.resize(QJDW_sum2,(440, 340),interpolation = cv2.INTER_NEAREST)
cv2.imwrite('C:/Users/Zn/Desktop/WORK/test7.png',QJDW_sum3)

# im = Image.fromarray(QJDW_sum)
# im.save("C:/Users/Zn/Desktop/WORK/outfile.jpeg")
# matplotlib.pyplot.imshow(QJDW_sum)

# def out_img(data):                 #输出图片
#     new_im = Image.fromarray(data)     #调用Image库，数组归一化 
#     #new_im.show() 

#     pyplot.rcParams['figure.figsize'] = (8.0, 4.0) # 设置figure_size尺寸
#     pyplot.rcParams['image.interpolation'] = 'nearest' # 设置 interpolation style
#     pyplot.rcParams['image.cmap'] = 'hot' # 设置 颜色 style
#     pyplot.rcParams['savefig.dpi'] = 300 #图片像素
#     pyplot.rcParams['figure.dpi'] = 300 #分辨率

#     pyplot.imshow(data)                  #显示新图片
#     imageio.imwrite('C:/Users/Zn/Desktop/WORK/outfile7.png', new_im)   #保存图片到本地

# out_img(QJDW_sum)


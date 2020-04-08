# 导入nc库
import netCDF4 as nc
import numpy as np

f_w = nc.Dataset("Tem_15days.nc", "w", format="NETCDF4")

f_w.createDimension("day", 15)
f_w.createDimension("lat", 17)
f_w.createDimension("lon", 22)

f_w.createVariable("day", np.int, ("day"))
f_w.createVariable("lat", np.float32, ("lat"))
f_w.createVariable("lon", np.float32, ("lon"))

day = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

f_w.variables["day"][:] = day

f_w.createVariable("q", np.float32, ("time", "lat", "lon"))
var_data = np.ones(shape=(15, 17, 22), dtype=np.float32)
f_w.variables["q"][:] = var_data

# 创建一个群组，名字为'wind'
group1 = f_w.createGroup("wind")

group1.createVariable("u", np.float32, ("time", "level", "lat", "lon"))
var_data = np.ones(shape=(12, 37, 161, 177), dtype=np.float32)
group1.variables["u"][:] = var_data

group1.createVariable("v", np.float32, ("time", "level", "lat", "lon"))
var_data = np.zeros(shape=(12, 37, 161, 177), dtype=np.float32)
group1.variables["v"][:] = var_data

group1.close  # 关闭群组， 注意，这里没有括号

f_w.close()

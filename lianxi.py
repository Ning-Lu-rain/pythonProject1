# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# data = pd.read_excel("hotel_v5_now_gai.xlsx")
# data1 = data.copy(deep=True)
# is_null = pd.isnull(data["生成达标"])
# # print(type(is_null))
# dis = []
# dis_bi = []
# cet = []
# for i in range(len(data)):
#     if not is_null[i]:
#         dis.append(data.loc[i,"编辑距离"])
#         dis_bi.append(data.loc[i,"编辑距离比"])
#         cet.append(data.loc[i,"生成达标"])
# dis_bi_zero = []
# dis_bi_one = []
# for i in range(len(dis_bi)):
#     if cet[i] == 0:
#         dis_bi_zero.append(dis_bi[i])
#     else:
#         dis_bi_one.append(dis_bi[i])
# max1 = max(dis_bi_zero)
# max2 = max(dis_bi_one)
# min1 = min(dis_bi_zero)
# min2 = min(dis_bi_one)
# mean1 = np.mean(dis_bi_zero)
# mean2 = np.mean(dis_bi_one)
# var1 = np.var(dis_bi_zero)
# var2 = np.var(dis_bi_one)
# std1 = np.std(dis_bi_zero)
# std2 = np.std(dis_bi_one)
# Q3_1 = np.quantile(dis_bi_zero,0.75)
# Q3_2 = np.quantile(dis_bi_one,0.75)
# print("不达标：\nmax:{:.2f}\nmin:{:.2f}\nmean:{:.2f}\nvar:{:.2f}\nstd:{:.2f}\nQ3:{:.2f}".format(max1, min1, mean1, var1, std1,Q3_1))
# print("达标：\nmax:{:.2f}\nmin:{:.2f}\nmean:{:.2f}\nvar:{:.2f}\nstd:{:.2f}\nQ3:{:.2f}".format(max2, min2, mean2, var2, std2,Q3_2))
#
# plt.rcParams['font.sans-serif'] = ['SimHei']
# # 读取数据
# # data = dis_bi_zero
# data = dis_bi_one
# # 画笔对象
# fig,ax = plt.subplots()
# ax.hist(data,range=(0,1.5),bins=15)
# plt.xlabel("编辑距离比")
# plt.ylabel("频数")
#
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_excel("zhuanye.xlsx")
data1 = data.copy(deep=True)
is_null = pd.isnull(data["编辑距离"])
# print(type(is_null))
dis = []
dis_bi = []
name = []
for i in range(len(data)):
    if not is_null[i]:
        dis.append(data.loc[i,"编辑距离"])
        dis_bi.append(data.loc[i,"编辑距离比"])
        name.append(data.loc[i,"主播名字"])

max1 = max(dis_bi)

min1 = min(dis_bi)

mean1 = np.mean(dis_bi)

var1 = np.var(dis_bi)

std1 = np.std(dis_bi)

Q3_1 = np.quantile(dis_bi,0.75)

print("max:{:.2f}\nmin:{:.2f}\nmean:{:.2f}\nvar:{:.2f}\nstd:{:.2f}\nQ3:{:.2f}".format(max1, min1, mean1, var1, std1,Q3_1))


plt.rcParams['font.sans-serif'] = ['SimHei']
# 读取数据
data = dis_bi
# 画笔对象
fig,ax = plt.subplots()
ax.hist(data,range=(0,1.5),bins=15)
plt.xlabel("编辑距离比")
plt.ylabel("频数")

plt.show()


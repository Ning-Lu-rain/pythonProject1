encoding="gbk"
import pandas as pd
import os
dis_bi_num = []
change_num = []
list_name = []
for path in os.listdir("sys_result"):
    data = pd.read_excel("sys_result/"+path)
    dis_bi_num.append(len(data[data["编辑距离比"]<0.2]))
    change_num.append(len(data[data["【】变化"]=="是"]))
    list_name.append(path.split(".")[0])
df = pd.DataFrame(columns=["文件名","编辑距离比不合格","【】变化"])
df["文件名"] = list_name
df["编辑距离比不合格"] = dis_bi_num
df["【】变化"] = change_num
df.to_excel("result.xlsx",index=False)
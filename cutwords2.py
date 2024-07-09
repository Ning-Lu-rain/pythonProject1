import jieba
import logging
from collections import Counter
import os
import datetime

def logger_init():
    # 结构化日志
    txt_path = 'log'
    logger = logging.getLogger()  # 获取Logger对象
    logger.setLevel(logging.INFO)
    # handler = TimedRotatingFileHandler(f'{txt_path}/output', when="M", interval=1)
    handler = logging.FileHandler(os.path.join(txt_path, 'log_{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))), encoding='utf-8')
    handler.suffix = "_%Y-%m-%d_%H-%M-%S.log"
    formatter = logging.Formatter('%(asctime)s %(lineno)s  %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = logger_init()

def count_freq(words):
    # 统计词频，字频
    a = Counter(words)
    return a

def cut_concat(line,words,freq):
    logger.info("正在处理的句子为：{}".format(line))
    #如果字符串词频都相等，就返回首个字符串
    bb = [i for i in freq.values()]
    b = set(freq.values())
    if len(b) == 1 and bb[0]>1:
        result = line[:int(len(line)/bb[0])]
        result = "用户说了{}遍{}".format(bb[0],result)
        # logger.info("处理结果为：{}".format(result))
        logger.info("处理逻辑：返回首个字符串")
        return result

    logger_print0 = False
    # 如果分割后有字符串词频大于0.8，只保留一个字符串
    cc = [jj for jj in freq.keys()]
    c = [i for i in freq.values()]
    for i in range(len(freq)):
        if c[i]/len(words) > 0.8:
            logger_print0 = True
            for j in range(c[i]-1):
                words.remove(cc[i])
    if logger_print0:
        logger.info("处理逻辑：词频比例大于0.8，只保留一个")

    #如果临近字符串有起始包含关系，则保留最长的字符串
    logger_print1 = False
    if len(words) > 1:
        words2 = words.copy()
        for k in range(1,len(words2)):
            # print(k)
            if words2[k].startswith(words2[k-1]) or words2[k-1].startswith(words2[k]):
                logger_print1 = True
                words.remove(words2[k] if len(words2[k])<len(words2[k-1]) else words2[k-1])
    if logger_print1:
        logger.info("处理逻辑：临近字符串有起始包含关系，保留最长的字符串")

    #对长度大于3的字符串进行字频统计,如果字符串中有字的频率大于0.9，就把该字放入manywords里面，同时把该字符串置为空
    d = []
    logger_print2 = False
    for l in range(len(words)):
        if len(words[l])>2:
            e = count_freq(list(words[l]))
            ee = [i for i in e.keys()]
            f = [m for m in e.values()]
            for n in range(len(e)):
                if f[n]/len(words[l]) > 0.9:
                    logger_print2 = True
                    d.append(ee[n])
                    words[l] = ""
    if logger_print2:
        logger.info("处理逻辑：字频比例大于0.9")

    #如果result里面还有字与manywords里面的字相同，则剔除
    logger_print3 = False
    result = "".join(words)
    manywords = "".join(d)
    if result == " " and manywords != "" and len(line) / len(result) > 2:
        result = "用户说了大量的{}".format(manywords)
    elif result != "" and manywords != "" and len(line)/len(result) > 2:
        result2 = list(result)
        for kk in range(len(result)):
            for mm in range(len(manywords)):
                if manywords[mm] == result[kk]:
                    logger_print3 = True
                    result2[kk] = ""
        if logger_print3:
            logger.info("处理逻辑：进一步剔除重复信息")
        result = "用户说了大量的{},还说了{}".format(manywords,"".join(result2))
    elif manywords != "" and len(result)==0 and len(line)/len(manywords) > 2:
        result = "用户说了大量的{}".format(manywords)
    # logger.info("处理结果为：{}".format(result))
    return result

if __name__ == '__main__':
    data =  open('线上Question-例子.txt',encoding="utf-8")
    datalines = data.readlines()
    newfile = open("newfile4.txt", "w", encoding="utf-8")

    for line in datalines:
        line = line.strip()
        # line = line.replace(' ','')
        # print(line)
        words = jieba.lcut(line)
        words_freq = count_freq(words)
        result = cut_concat(line,words,words_freq)
        newfile.write(result+"\n")

    data.close()
    newfile.close()

# if __name__ == '__main__':
#     # words_list = ["[iloveyou][iloveyou][iloveyou][iloveyou][iloveyou][iloveyou][iloveyou][iloveyou][iloveyou][iloveyou][iloveyou]",#39 处理逻辑：返回首个字符串
#     #               "配送范围，哈哈哈哈哈哈哈哈哈哈哈哈哈呀哈哈",
#     #                                                            #64 处理逻辑：临近字符串有起始包含关系，保留最长的字符串
#     #                                                            #80 处理逻辑：字频比例大于0.9
#     #                                                            #94 处理逻辑：进一步剔除重复信息
#     #               "哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈"
#     #                                                            #52 处理逻辑：词频比例大于0.8，只保留一个
#     #                                                            #64 处理逻辑：临近字符串有起始包含关系，保留最长的字符串
#     #                                                            #80 处理逻辑：字频比例大于0.9
#     #               ]
#     for word in words_list:
#         word = word.strip()
#         # word = word.replace(' ','')
#         words = jieba.lcut(word)
#         words_freq = count_freq(words)
#         result = cut_concat(word,words,words_freq)
#         print(result)

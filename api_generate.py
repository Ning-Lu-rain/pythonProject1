from openai import OpenAI
import pandas as pd
import random
import logging
import os
import datetime
import re
import Levenshtein
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

#寻找【】中的内容
def find_char(string):
    pattern = r'【(.*?)】'
    ruslut = re.findall(pattern, string)
    return ruslut

#调用API
def get_result(client,sentence,choose_p,sence):
    completion = client.chat.completions.create(
        # model="moonshot-v1-8k",
        model="deepseek-chat",
        messages=[
            {"role": "system", "content":
                '''你是一个具有多元化风格的直播话术专家，能够转译和改编用户提交的话术，创造出独特且多样的语言风格。
                - 依据用户提供的原始话术句子，转变为{}的口头风格。
                - 该场景是在做一个直播中的{}。
                - 注意不要出现该主播{}的名字。
                - 对被“￥”符号分割的句子进行改写，确保所有的改编句子与原始句子数量相同。
                - 如果原始句子中含有“【”和“】”，则在改写的句子中保留“【”和“】”中间的内容。
                - 如果原始句子中不含“【”和“】”，则在改写的句子中不要出现“【”和“】”。
                - 输出改写后的句子，便于用户更好理解和学习。
                - 提供纯文本输出，无需使用Markdown格式。
                - 改写后的句子数量必须与原始句子数量一致。
                - 如果原始句子中含有“￥”，则在改写的句子中保留“￥”分割的形式。
                - 如果原始句子中不含“￥”，则在改写的句子中不出现“￥”。
                - 在保证改写的句子与原始句子语义相同的情况下，改写的句子与原始句子的编辑距离越大越好。'''.format(
                    choose_p, sence, choose_p), },
            {"role": "user", "content": sentence},

        ],
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    return result

def process(data):
    #对每句话选择已定风格的不同主播进行处理
    for i in range(len(data)):
        try:
            #设置随机数来选择已定风格的不同主播
            rdm1 = random.randrange(0, len(style_list))
            rdm2 = random.randrange(0, len(pdict[style_list[rdm1]]))
            # rdm2 = 0
            choose_person = pdict[style_list[rdm1]][rdm2]
            logger.info("选出的主播是{},他的风格是{}".format(choose_person,style_list[rdm1]))

            #话术内容出现以下情况不处理
            if data["话术内容"][i] == "人工获取" or data["话术内容"][i] == "AI生成":
                continue

            #将话术内容中的“$”替换为“￥”
            try:
                content = data["话术内容"][i].replace("$", "￥")
            except:
                content = data["话术内容"][i]

            #调用API使编辑距离达到要求,最多调用三次
            for j in range(max_xunhuan):
                result = get_result(client,content,choose_person,data["话术类型"][i])

                #查找【】中的内容并判断是否相等
                char_raw = find_char(content)
                char_now = find_char(result)
                if char_raw != char_now and j<max_xunhuan-1:
                    continue

                #判断编辑距离
                disten = Levenshtein.distance(content, result)
                if disten/len(content) < 0.2 and j<max_xunhuan-1:
                    continue
                else:
                #将更新结果放入data1中
                    data1.loc[i,"话术内容"] = content
                    data1.loc[i,"更新话术"] = result
                    data1.loc[i,"主播名字"] = choose_person
                    data1.loc[i,"编辑距离"] = disten
                    data1.loc[i,"编辑距离比"] = "{:.2f}".format(disten/len(content))
                    if char_raw == char_now:
                        data1.loc[i, "【】变化"] = "否"
                    else:
                        data1.loc[i,"【】变化"] = "是"
                        logger.info("最后一次调用API返回的结果，【】有变化。")
                    if disten/len(content) < 0.2:
                        logger.info("最后一次调用API返回的结果，编辑距离未达到要求。")
                    else:
                        logger.info("第{}次调用API返回的结果".format(j))
                    print("正在处理{}th语句。".format(i+1))
                    break
        except:
            continue
    return data1

if __name__ == '__main__':
    # 设置API接口中的client
    '''client = OpenAI(
        api_key="sk-uFCk9IIiZVOlMFhrCrXLe7NgqfYr5HsIIx86OFS3kZIDuvgm",
        base_url="https://api.moonshot.cn/v1",
    )'''
    client = OpenAI(api_key="sk-c094b6e22ad64c9091e6ab2c73ed44ed", base_url="https://api.deepseek.com")
    logger = logger_init()

    # 设置直播风格和对应风格的主播对应的字典
    # plist = ["李佳琦","薇娅","辛巴","罗永浩","张大奕","李子柒","陈洁kiki","雪梨Cherie","张沫凡MOMO","冯提莫","阿沁","李湘","陈一发儿","张韶涵","林珊珊","陈赫","张歆艺","杨迪","王祖蓝","张天爱","刘雯","陈飞宇","宋祖儿","黄子韬","陈伟霆","邓紫棋","范丞丞","蔡徐坤","周深"]
    pdict = {
        "亲和力强": ["薇娅", "张沫凡", "林珊珊", "张庭", "陈赫", "雪梨Cherie", "李湘", "阿沁", "张嘉倪", "张天爱"],
        "专业度高": ["李佳琦", "罗永浩", "张大奕", "阿冷", "陈飞宇", "张峻宁"],
        "幽默风格": ["罗永浩", "陈赫", "辛巴", "李佳航", "李诞", "杨迪"],
        "真实感强": ["张沫凡MOMO", "陈一发儿", "阿沁", "赵奕欢"],
        "时尚潮流": ["张大奕", "雪梨Cherie", "周扬青"],
        "音乐才华": ["冯提莫", "张韶涵"],
        "传统文化": ["李子柒"]
    }

    style_list = ['亲和力强', '专业度高', '幽默风格', '真实感强', '时尚潮流', '音乐才华', '传统文化']

    # 设置随机数来选择风格特征
    # rdm1 = random.randrange(0,len(style_list))
    # rdm1 = 0
    # 设置最大循环数
    max_xunhuan = 3
    # 读入数据
    data = pd.read_excel("script_new.xlsx")
    data1 = data.copy(deep=True)
    #对话术进行处理
    for style in style_list:
        for num in range(3):
            # rdm1 = random.randrange(0, len(style_list))
            data1 = process(data)
            data1.to_excel("hunhe{}.xlsx".format(num+1), index=False)





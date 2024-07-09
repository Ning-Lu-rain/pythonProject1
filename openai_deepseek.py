# python3
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI


client = OpenAI(api_key="sk-c094b6e22ad64c9091e6ab2c73ed44ed", base_url="https://api.deepseek.com")
data = open('线上Question-例子.txt', encoding="utf-8")
datalines = data.readlines()
newfile = open("newfile_deepseek2.txt", "w", encoding="utf-8")

for line in datalines:
    line = line.strip()
    line = line.replace(' ', '')
    # print(line)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "请帮我处理下面的句子，如果句子中有叠词请缩短，比如哈哈哈哈哈哈哈哈哈啊哈哈哈，处理成哈哈，比如中奖了，哈哈哈哈哈哈哈哈，处理成中奖了，如果没有叠词的话请按原文输出，注意不要改变句子的意思，不要多加词"},
            {"role": "user", "content": line},
        ],
        stream=False
    )
    print(response.choices[0].message.content)
    newfile.write(response.choices[0].message.content + "\n")
data.close()
newfile.close()
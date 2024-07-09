from openai import OpenAI
import time

client = OpenAI(
    api_key="sk-uFCk9IIiZVOlMFhrCrXLe7NgqfYr5HsIIx86OFS3kZIDuvgm",
    base_url="https://api.moonshot.cn/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system",
         "content": "你是一个万事通"},
        {"role": "user", "content":"请说出30个中国最火的非常幽默的直播带货主播"}
    ],
    temperature=0.3,
)
result = completion.choices[0].message.content
print(result)






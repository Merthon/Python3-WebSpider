import openai

# 设置你的 API 密钥
openai.api_key = 'sk-xFVnXciRUCCZ4wrmW4Yrfn8jVtLn6Rk7qOmRTOaHNZ7fbnOu'

# 如果你要使用自定义的 base_url（如你提供的地址），可以在调用时设置：
openai.api_base = "https://api.chatanywhere.tech/v1"

# 调用 ChatCompletion 接口生成文本
completion = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # 使用你选择的模型，如 gpt-4
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ]
)

# 输出生成的文本
print(completion.choices[0].message['content'])

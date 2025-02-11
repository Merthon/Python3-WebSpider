import openai

# 设置你的 API 密钥
openai.api_key = 'sk-xFVnXciRUCCZ4wrmW4Yrfn8jVtLn6Rk7qOmRTOaHNZ7fbnOu'

# 调用 OpenAI API，生成一个文本响应
response = openai.Completion.create(
  model="gpt-4o-mini",  # 使用的模型，这里是 GPT-3 的 Davinci 模型
  prompt="Hello, OpenAI!",  # 输入文本
  max_tokens=10,  # 返回的最大 token 数量
)

# 输出生成的文本
print(response.choices[0].text.strip())

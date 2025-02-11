# 配置小红书，企业微信通知以及监控相关信息

# 小红书config
XHS_CONFIG = {
    "COOKIE": "登录后小红书的cookie"
}

# 这里使用企业微信 Webhook
# 机器人 Webhook 是最简单的方法，无需 API 认证，也没有 IP 限制
WECOM_CONFIG = {
    "WEBHOOK_URL": "自己获取的Webhook URL"
}

MONITOR_CONFIG = {
    "USER_ID": "被监控用户的小红书id", 
    "CHECK_INTERVAL": 5, #检查笔记更新
    "ERROR_COUNT": 10,
    "AUTO_INTERACT": True,  # 是否开启自动互动
    "FALLBACK_COMMENTS": [  # 随机选择一条评论
        "太棒了！",
        "喜欢这篇笔记",
        "我来啦~",
        "路过~",
        "感谢分享",
        "期待更新~",
        "支持支持！"
    ],
    "LIKE_DELAY": 5,  # 点赞延迟(秒)
    "COMMENT_DELAY": 10,  # 评论延迟(秒)
}
# LLM配置
LLM_CONFIG = {
    "API_KEY": "OpenAI API Key",
    "API_BASE": "API代理地址", 
    "MODEL": "gpt-3.5-turbo",  
    "MAX_TOKENS": 150, # 生成的评论最大字数
    "TEMPERATURE": 0.7,
    "SYSTEM_PROMPT": """你是一个正在追求心仪女生的人，需要对她的小红书笔记进行评论。
请根据笔记内容生成一条甜蜜、真诚但不过分的评论。评论要：
1. 体现你在认真看她的内容
2. 表达适度的赞美和支持
3. 语气要自然、真诚
4. 避免过分讨好或低声下气
5. 根据内容类型（图文/视频）采用合适的表达
6. 字数控制在100字以内
7. 避免过于模板化的表达
8. 评论内容要符合小红书平台规则"""
} 
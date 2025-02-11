# 配置小红书，企业微信通知以及监控相关信息
# config
XHS_CONFIG = {
    "COOKIE": "abRequestId=0cfa9aa7-fce4-5319-afc8-569259c108b7; xsecappid=xhs-pc-web; a1=19349fcfe9f56eislqey1a19bh51g3tu2rx87d4px30000349558; webId=51b022fdbc49272d09cab7852f5059e2; gid=yjq4jifyiiJJyjq4jiSidFf4ji2Kd3M1AdvyCUC0yjDx2Yq8ykq97W888q4j22Y8Y8iWfJyj; web_session=040069b4c95abb679862651192354b1a536772; webBuild=4.55.1; acw_tc=0ad52d8017392364093803980e7e42a0510a065546507470593e65d05fdaab; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=29385093-eb3d-43fd-afef-3580505a3a18; unread={%22ub%22:%2267aa087f000000002900bfb6%22%2C%22ue%22:%2267a9ec72000000001800667f%22%2C%22uc%22:23}"
}

WECOM_CONFIG = {
    "WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=294dc5f2-9112-4ca4-a396-b604f2032c04"
}

MONITOR_CONFIG = {
    "USER_ID": "5b8a29d56c11370001d4d254", #  5b8a29d56c11370001d4d254
    "CHECK_INTERVAL": 5,
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
    "API_KEY": "sk-xFVnXciRUCCZ4wrmW4Yrfn8jVtLn6Rk7qOmRTOaHNZ7fbnOu",
    "API_BASE": "https://api.chatanywhere.tech/v1", 
    "MODEL": "gpt-3.5-turbo",  
    "MAX_TOKENS": 150,
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
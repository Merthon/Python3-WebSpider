# 小红书配置
XHS_CONFIG = {
    "COOKIE": "abRequestId=0cfa9aa7-fce4-5319-afc8-569259c108b7; xsecappid=xhs-pc-web; a1=19349fcfe9f56eislqey1a19bh51g3tu2rx87d4px30000349558; webId=51b022fdbc49272d09cab7852f5059e2; gid=yjq4jifyiiJJyjq4jiSidFf4ji2Kd3M1AdvyCUC0yjDx2Yq8ykq97W888q4j22Y8Y8iWfJyj; webBuild=4.55.1; web_session=040069b4c95abb679862651192354b1a536772; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=93877da6-33e1-4b86-b4bc-2bed4a1525a1; acw_tc=0a00d5bf17390273202372505e82f2e7ca6a4dafcb9514f05420573c25969d; unread={%22ub%22:%22678f60c20000000017038f19%22%2C%22ue%22:%226785f8420000000019036010%22%2C%22uc%22:32}",  # 必需包含 a1、web_session 和 webId 字段
}

# 企业微信应用配置
WECOM_CONFIG = {
    "CORPID": "ww37c0b3c0eb30b914",  # 企业ID
    "AGENTID": "1000002",  # 应用ID
    "SECRET": "dHW3PFTrizE-t_tVAJhFGdeCNZQuwxtFH5PbCfnIJc0",  # 应用的Secret
}

# 监控配置
MONITOR_CONFIG = {
    "USER_ID": "67a76ecc000000002a0014f5",
    "CHECK_INTERVAL": 5,  # 建议至少5秒以上
    "ERROR_COUNT": 10,  # 连续错误次数
}


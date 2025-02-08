import time
import requests

class WecomMessage:
    def __init__(self, corpid: str, agentid: int, secret: str):
        """
        初始化企业微信消息发送类
        :param corpid: ww37c0b3c0eb30b914
        :param agentid: 1000002
        :param secret: dHW3PFTrizE-t_tVAJhFGdeCNZQuwxtFH5PbCfnIJc0
        """
        self.corpid = corpid
        self.agentid = agentid
        self.secret = secret
        self.access_token = None
        self.token_expires_time = 0
    
    def get_access_token(self) -> str:
        """
        获取访问令牌
        :return: access_token
        """
        now = time.time()
        if self.access_token and now < self.token_expires_time:
            return self.access_token
            
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corpid,
            "corpsecret": self.secret
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get("errcode") == 0:
                self.access_token = data.get("access_token")
                self.token_expires_time = now + data.get("expires_in") - 200  # 提前200秒刷新
                return self.access_token
            else:
                raise Exception(f"获取access_token失败: {data}")
        except Exception as e:
            print(f"获取access_token异常: {e}")
            raise

    def send_text(self, content: str, touser: str = "@all") -> bool:
        """
        发送文本消息
        :param content: 消息内容
        :param touser: 接收人，默认为所有人
        :return: 是否发送成功
        """
        try:
            message = {
                "touser": touser,
                "msgtype": "text",
                "agentid": self.agentid,
                "text": {
                    "content": content
                },
                "enable_duplicate_check": 1,
                "duplicate_check_interval": 1800
            }
            
            access_token = self.get_access_token()
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            
            response = requests.post(url, json=message)
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"企业微信消息发送成功")
                return True
            else:
                print(f"企业微信消息发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"企业微信消息发送异常: {e}")
            return False 
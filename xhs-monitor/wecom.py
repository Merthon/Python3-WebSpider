import time
import requests

class WecomMessage:
    def __init__(self, webhook_url: str):
        """
        初始化 WecomMessage 实例
        :param webhook_url: 企业微信机器人的 Webhook 地址
        """
        self.webhook_url = webhook_url

    def send_text(self, content: str):
        """
        发送文本消息
        :param content: 消息内容
        :return: 是否发送成功
        """
        try:
            message = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "enable_duplicate_check": 1, # 启用重复消息检查
                "duplicate_check_interval": 1800 # 重复消息的检查间隔（单位：秒），这里设置为 30 分钟
            }
            # # 向 Webhook URL 发送 POST 请求，携带消息体
            response = requests.post(self.webhook_url,json=message)
            result = response.json() # 解析返回的 JSON 响应
            
            # 如果返回的 errcode 为 0，则表示发送成功
            if result.get("errcode") == 0:
                print(f"群机器人消息发送成功")
                return True
            else:
                # 如果发送失败，记录错误信息并返回
                print(f"群消息机器人发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"群机器人消息发送异常: {e}")
            return False 
        
        finally:
            time.sleep(1.5)  #1.5 秒延时，防止频繁请求
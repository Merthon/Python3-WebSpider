import time
import requests

class WecomMessage:
    def __init__(self, webhook_url: str):
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
                "enable_duplicate_check": 1,
                "duplicate_check_interval": 1800
            }
            response = requests.post(self.webhook_url,json=message)
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"群机器人消息发送成功")
                return True
            else:
                print(f"群消息机器人发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"群机器人消息发送异常: {e}")
            return False 
        
        finally:
            time.sleep(1.5)  # 限流，避免超限
import time
import requests

class WecomMessage:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_text(self, content: str):
        """
        发送文本消息
        :param content: 消息内容
        """
        try:
            message = {"msgtype": "text", "text": {"content": content}}
            response = requests.post(self.webhook_url, json=message)
            result = response.json()

            if result.get("errcode") == 0:
                print("企业微信消息发送成功")
                return True
            else:
                print(f"企业微信消息发送失败: {result}")
                return False

        except Exception as e:
            print(f"企业微信消息发送异常: {e}")
            return False

        finally:
            time.sleep(1.5)  # 限流，避免超限

import requests
import random
import logging
from config import LLM_CONFIG, MONITOR_CONFIG

# 设置日志记录
logging.basicConfig(level=logging.INFO)

class CommentGenerator:
    def __init__(self):
        self.api_key = LLM_CONFIG["API_KEY"]
        self.api_base = LLM_CONFIG["API_BASE"]
        self.model = LLM_CONFIG["MODEL"]
        
    def generate_comment(self, title: str, content: str) -> str:
        """
        根据笔记标题和内容生成评论
        """
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": LLM_CONFIG["SYSTEM_PROMPT"]
                        },
                        {
                            "role": "user",
                            "content": f"请根据以下笔记生成一条评论:\n标题: {title}\n内容: {content}"
                        }
                    ],
                    "max_tokens": LLM_CONFIG["MAX_TOKENS"],
                    "temperature": LLM_CONFIG["TEMPERATURE"]
                }
            )
            
            if response.status_code == 200:
                comment = response.json()["choices"][0]["message"]["content"].strip()
                logging.info("评论生成成功")
                return comment
            else:
                logging.error(f"API 请求失败: {response.status_code}")
                logging.error(f"错误信息: {response.text}")
                return self._get_fallback_comment()
                
        except requests.exceptions.RequestException as e:
            logging.error(f"生成评论失败: {e}")
            return self._get_fallback_comment()
            
    def _get_fallback_comment(self) -> str:
        """
        当 API 调用失败时的备用评论
        """
        fallback_comment = random.choice(MONITOR_CONFIG.get('FALLBACK_COMMENTS', []))
        logging.warning(f"使用备用评论: {fallback_comment}")
        return fallback_comment


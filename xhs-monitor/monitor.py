from xhs import XhsClient
import time
from typing import List
from config import XHS_CONFIG, WECOM_CONFIG, MONITOR_CONFIG
from utils import xhs_sign
from db import Database
from wecom import WecomMessage

class XHSMonitor:
    def __init__(self, cookie: str, corpid: str, agentid: int, secret: str):
        """
        初始化监控类
        :param cookie: abRequestId=0cfa9aa7-fce4-5319-afc8-569259c108b7; xsecappid=xhs-pc-web; a1=19349fcfe9f56eislqey1a19bh51g3tu2rx87d4px30000349558; webId=51b022fdbc49272d09cab7852f5059e2; gid=yjq4jifyiiJJyjq4jiSidFf4ji2Kd3M1AdvyCUC0yjDx2Yq8ykq97W888q4j22Y8Y8iWfJyj; webBuild=4.55.1; web_session=040069b4c95abb679862651192354b1a536772; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=93877da6-33e1-4b86-b4bc-2bed4a1525a1; acw_tc=0a00d5bf17390273202372505e82f2e7ca6a4dafcb9514f05420573c25969d; unread={%22ub%22:%22678f60c20000000017038f19%22%2C%22ue%22:%226785f8420000000019036010%22%2C%22uc%22:32}
        :param corpid: ww37c0b3c0eb30b914
        :param agentid: 1000002
        :param secret: dHW3PFTrizE-t_tVAJhFGdeCNZQuwxtFH5PbCfnIJc0
        """
        self.client = XhsClient(cookie=cookie, sign=xhs_sign)
        self.wecom = WecomMessage(corpid, agentid, secret)
        self.db = Database()
        self.error_count = 0
        
    def send_error_notification(self, error_msg: str):
        """
        发送错误通知
        :param error_msg: 错误信息
        """
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        content = (
            "小红书监控异常告警\n"
            f"错误信息：{error_msg}\n"
            f"告警时间：{time_str}"
        )
        self.wecom.send_text(content)
    
    def get_latest_notes(self, user_id: str) -> List[dict]:
        """
        获取用户最新笔记
        :param user_id: 用户ID
        :return: 笔记列表
        """
        try:
            res_data = self.client.get_user_notes(user_id)
            self.error_count = 0
            return res_data.get('notes', [])
            
        except Exception as e:
            error_msg = str(e)

            print(f"获取用户笔记失败: {error_msg}")

            time.sleep(60)

            self.error_count += 1

            if self.error_count >= MONITOR_CONFIG["ERROR_COUNT"]:
                self.send_error_notification(f"API 请求失败\n详细信息：{error_msg}")
                exit(-1)

            return []

    def send_note_notification(self, note_data: dict):
        """
        发送笔记通知
        :param note_data: 笔记数据
        """
        note_url = f"https://www.xiaohongshu.com/explore/{note_data.get('note_id')}"
        user_name = note_data.get('user', {}).get('nickname', '未知用户')
        title = note_data.get('display_title', '无标题')
        type = note_data.get('type', '未知类型')
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        
        content = (
            "小红书用户发布新笔记\n"
            f"用户：{user_name}\n"
            f"标题：{title}\n"
            f"链接：{note_url}\n"
            f"类型：{type}\n"
            f"监控时间：{time_str}"
        )
        
        self.wecom.send_text(content)

    def monitor_user(self, user_id: str, interval: int):
        """
        监控用户动态
        :param user_id: 用户ID
        :param interval: 检查间隔(秒)
        """
        print(f"开始监控用户: {user_id}")
        
        while True:
            try:
                latest_notes = self.get_latest_notes(user_id)

                for note in latest_notes:
                    if self.db.add_note_if_not_exists(note):
                        print(f"发现新笔记: {note.get('display_title')}")
                        self.send_note_notification(note)
                    
            except Exception as e:
                error_msg = str(e)
                print(f"监控过程发生错误: {error_msg}")
            time.sleep(interval)

def main():
    monitor = XHSMonitor(
        cookie=XHS_CONFIG["COOKIE"],
        corpid=WECOM_CONFIG["CORPID"],
        agentid=WECOM_CONFIG["AGENTID"],
        secret=WECOM_CONFIG["SECRET"]
    )

    monitor.monitor_user(
        user_id=MONITOR_CONFIG["USER_ID"],
        interval=MONITOR_CONFIG["CHECK_INTERVAL"]
    )

if __name__ == "__main__":
    main()

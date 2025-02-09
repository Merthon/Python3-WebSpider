from xhs import XhsClient
import time
from typing import List
from config import XHS_CONFIG, WECOM_CONFIG, MONITOR_CONFIG
from utils import xhs_sign  # 导入修改后的 xhs_sign
from db import Database
from wecom import WecomMessage


class XHSMonitor:
    def __init__(self, cookie: str, corpid: str, agentid: int, secret: str):
        """
        初始化监控类
        :param cookie: 小红书cookie
        :param corpid: 企业ID
        :param agentid: 应用ID
        :param secret: 应用的Secret
        """
        self.client = XhsClient(cookie=cookie, sign=xhs_sign)  # 使用传入的 xhs_sign
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
import os
import logging
from playwright.sync_api import sync_playwright
from time import sleep

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 获取 stealth.min.js 路径
STEALTH_JS_PATH = os.path.join(os.path.dirname(__file__), "public/stealth.min.js")

# Playwright 全局管理
class XhsSigner:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()

        if not os.path.exists(STEALTH_JS_PATH):
            raise FileNotFoundError(f"Stealth.js 文件未找到: {STEALTH_JS_PATH}")

        self.context.add_init_script(path=STEALTH_JS_PATH)
        self.page = self.context.new_page()
        self.page.goto("https://www.xiaohongshu.com")

        logging.info("Playwright 浏览器已启动")

    def xhs_sign(self, uri, data=None, a1="", web_session=""):
        """
        生成小红书请求签名
        :param uri: 请求地址
        :param data: 请求数据
        :param a1: 用户 Cookie (可选)
        :param web_session: 可能的额外 Cookie (当前未使用)
        :return: 包含 x-s 和 x-t 的字典
        """
        for attempt in range(10):
            try:
                # 如果提供了 a1，设置 Cookie
                if a1:
                    self.context.add_cookies([
                        {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}
                    ])
                    self.page.reload()
                    sleep(1)  # 避免 Cookie 未生效

                # 检查 window._webmsxyw 是否存在
                exists = self.page.evaluate("() => typeof window._webmsxyw === 'function'")
                if not exists:
                    logging.warning("window._webmsxyw 未加载，可能需要手动检查页面")
                    continue

                encrypt_params = self.page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }

            except Exception as e:
                logging.error(f"第 {attempt+1} 次尝试失败: {e}")

        raise Exception("重试 10 次仍无法签名，请检查 Playwright 或小红书页面")

    def close(self):
        """ 关闭浏览器 """
        self.browser.close()
        self.playwright.stop()
        logging.info("Playwright 浏览器已关闭")


# 创建 XhsSigner 实例
signer = XhsSigner()

# 封装 xhs_sign 函数
def xhs_sign(uri, data=None, a1="", web_session=""):
    return signer.xhs_sign(uri, data, a1, web_session)

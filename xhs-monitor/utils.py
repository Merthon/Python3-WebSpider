from playwright.sync_api import sync_playwright
from time import sleep
import logging
import random

def xhs_sign(uri, data=None, a1="", web_session="", stealth_js_path="public/stealth.min.js"):
    """
    获取小红书签名参数
    :param uri: 请求的 URI
    :param data: 请求的数据
    :param a1: 用户的 cookies 信息
    :param web_session: 当前的 web 会话（暂未使用）
    :param stealth_js_path: stealth.js 的路径
    :return: 加密后的请求参数
    """
    retry_limit = 10  # 最大重试次数
    for attempt in range(retry_limit):
        try:
            with sync_playwright() as playwright:
                chromium = playwright.chromium

                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)  # 加载反爬虫脚本
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                
                # 设置 cookies
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}
                ])
                context_page.reload()  # 刷新页面
                sleep(random.uniform(1, 2))  # 随机等待，模拟正常行为
                
                # 加密参数获取
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                
                # 返回加密后的签名参数
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception as e:
            logging.error(f"第 {attempt + 1} 次尝试失败: {e}")
            sleep(random.uniform(3, 5))  # 重试间隔随机化，避免频繁请求
    # 重试多次失败，抛出异常
    raise Exception("签名失败，重试次数达到上限")

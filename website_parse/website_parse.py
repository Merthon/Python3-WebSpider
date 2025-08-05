from genericpath import exists
import requests
import json
import re
import sys
import os
import sqlite3
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime, timedelta
import argparse

class TechDetectorWithCache:
    def __init__(self, cache_file='web_info.db', cache_hours=24):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
        self.cache_file = cache_file
        self.cache_hours = cache_hours
        self.init_cache()
        
        # 检测规则
        self.rules = {
            # JavaScript 框架/库
            'JavaScript 框架/库': {
                'React': {
                    'scripts': [r'react\.js', r'react\.min\.js', r'react-dom'],
                    'html': [r'data-react', r'__REACT_DEVTOOLS_GLOBAL_HOOK__'],
                    'dom': ['[data-reactroot]']
                },
                'Vue.js': {
                    'scripts': [r'vue\.js', r'vue\.min\.js'],
                    'html': [r'data-v-', r'v-if', r'v-for'],
                    'dom': ['[data-v-', '[v-cloak]']
                },
                'Angular': {
                    'scripts': [r'angular\.js', r'@angular'],
                    'html': [r'ng-', r'data-ng-'],
                    'dom': ['[ng-app]', '[ng-controller]']
                },
                'jQuery': {
                    'scripts': [r'jquery\.js', r'jquery\.min\.js', r'jquery-\d+'],
                    'html': [r'\$\(', r'jQuery\(']
                },
                'Next.js': {
                    'scripts': [r'_next/static'],
                    'html': [r'__NEXT_DATA__', r'_next/static']
                },
                'Nuxt.js': {
                    'scripts': [r'_nuxt/'],
                    'html': [r'__NUXT__', r'_nuxt/']
                },
                'Svelte': {
                    'scripts': [r'svelte', r'_app/immutable'],
                    'html': [r'svelte-', r'__svelte']
                },
                'Alpine.js': {
                    'scripts': [r'alpine\.js', r'alpinejs'],
                    'html': [r'x-data', r'x-show', r'x-if']
                }
            },
            
            # CSS 框架
            'CSS 框架': {
                'Bootstrap': {
                    'css': [r'bootstrap\.css', r'bootstrap\.min\.css'],
                    'html': [r'class=".*?btn.*?"', r'class=".*?container.*?"']
                },
                'Tailwind CSS': {
                    'css': [r'tailwind'],
                    'html': [r'class=".*?(flex|grid|text-|bg-|p-|m-)']
                },
                'Bulma': {
                    'css': [r'bulma'],
                    'html': [r'class=".*?button.*?"', r'class=".*?column.*?"']
                },
                'Foundation': {
                    'css': [r'foundation'],
                    'html': [r'class=".*?foundation.*?"']
                },
                '自定义CSS': {
                    'css': [r'style\.css', r'main\.css', r'custom\.css', r'app\.css'],
                    'html': [r'<style[^>]*>(?!.*?(bootstrap|tailwind|bulma|foundation))']
                }
            },
            
            # UI 组件库
            'UI 组件库': {
                'Ant Design': {
                    'css': [r'antd'],
                    'html': [r'ant-', r'__antd']
                },
                'Element UI': {
                    'css': [r'element-ui'],
                    'html': [r'el-']
                },
                'Material-UI': {
                    'scripts': [r'material-ui', r'@mui'],
                    'html': [r'MuiThemeProvider', r'makeStyles']
                },
                'Vuetify': {
                    'css': [r'vuetify'],
                    'html': [r'v-application', r'vuetify']
                }
            },
            
            # CMS
            'CMS': {
                'WordPress': {
                    'meta': [{'name': 'generator', 'content': 'WordPress'}],
                    'html': [r'wp-content', r'wp-includes'],
                    'headers': {'X-Powered-By': 'WordPress'}
                },
                'Drupal': {
                    'meta': [{'name': 'generator', 'content': 'Drupal'}],
                    'html': [r'Drupal\.settings', r'sites/default']
                },
                'Joomla': {
                    'meta': [{'name': 'generator', 'content': 'Joomla'}],
                    'html': [r'joomla', r'com_content']
                },
                'Shopify': {
                    'html': [r'Shopify\.theme', r'shopify_pay'],
                    'scripts': [r'cdn\.shopify\.com']
                },
                'Hexo': {
                    'meta': [{'name': 'generator', 'content': 'Hexo'}],
                    'html': [r'hexo']
                }
            },
            
            # 后端技术
            '后端技术': {
                'PHP': {
                    'headers': {'X-Powered-By': 'PHP'},
                    'html': [r'PHPSESSID', r'\.php']
                },
                'ASP.NET': {
                    'headers': {'X-Powered-By': 'ASP.NET'},
                    'html': [r'__VIEWSTATE', r'__EVENTVALIDATION']
                },
                'Django': {
                    'html': [r'csrfmiddlewaretoken', r'django'],
                    'headers': {'X-Frame-Options': 'DENY'}
                },
                'Laravel': {
                    'html': [r'laravel_session', r'_token'],
                    'scripts': [r'laravel']
                },
                'Ruby on Rails': {
                    'html': [r'csrf-token', r'rails'],
                    'headers': {'X-Powered-By': 'Phusion Passenger'}
                },
                'Express.js': {
                    'headers': {'X-Powered-By': 'Express'}
                },
                'Spring Boot': {
                    'headers': {'X-Application-Context': 'application'},
                    'html': [r'spring', r'jsessionid']
                },
                'Node.js': {
                    'headers': {'X-Powered-By': 'Express'},
                    'html': [r'node_modules']
                }
            },
            
            # 服务器
            '服务器': {
                'Apache': {
                    'headers': {'Server': 'Apache'}
                },
                'Nginx': {
                    'headers': {'Server': 'nginx'}
                },
                'Cloudflare': {
                    'headers': {'Server': 'cloudflare', 'CF-RAY': ''}
                },
                'IIS': {
                    'headers': {'Server': 'Microsoft-IIS'}
                }
            },
            
            # 分析工具
            '分析工具': {
                'Google Analytics': {
                    'scripts': [r'google-analytics\.com', r'gtag\(', r'googletagmanager'],
                    'html': [r'UA-\d+-\d+', r'G-[A-Z0-9]+']
                },
                'Baidu Analytics': {
                    'scripts': [r'hm\.baidu\.com'],
                    'html': [r'_hmt\.push']
                },
                'Adobe Analytics': {
                    'scripts': [r'omniture', r'adobe'],
                    'html': [r's_account']
                }
            },
            
            # 其他工具
            '其他工具': {
                'GSAP': {
                    'scripts': [r'gsap', r'greensock', r'TweenMax', r'TweenLite'],
                    'html': [r'TweenMax', r'gsap', r'ScrollTrigger', r'TimelineMax']
                },
                'Core.js': {
                    'scripts': [r'core-js', r'corejs'],
                    'html': [r'core-js', r'__core-js_shared__']
                },
                'Three.js': {
                    'scripts': [r'three\.js', r'three\.min\.js'],
                    'html': [r'THREE\.', r'WebGLRenderer']
                },
                'D3.js': {
                    'scripts': [r'd3\.js', r'd3\.min\.js'],
                    'html': [r'd3\.', r'__d3_version__']
                },
                'Chart.js': {
                    'scripts': [r'chart\.js', r'chartjs'],
                    'html': [r'Chart\.']
                },
                'Font Awesome': {
                    'css': [r'font-awesome', r'fontawesome'],
                    'html': [r'fa-', r'fas ', r'far ']
                },
                'Swiper': {
                    'scripts': [r'swiper'],
                    'css': [r'swiper']
                },
                'AOS': {
                    'scripts': [r'aos\.js'],
                    'css': [r'aos\.css']
                },
                'Lottie': {
                    'scripts': [r'lottie', r'bodymovin'],
                    'html': [r'lottie-', r'bodymovin']
                },
                'Framer Motion': {
                    'scripts': [r'framer-motion'],
                    'html': [r'framer-motion']
                },
                'Intersection Observer': {
                    'html': [r'IntersectionObserver', r'intersectionObserver']
                },
                'Lodash': {
                    'scripts': [r'lodash\.js', r'lodash\.min\.js'],
                    'html': [r'_\.', r'lodash']
                },
                'Moment.js': {
                    'scripts': [r'moment\.js', r'moment\.min\.js'],
                    'html': [r'moment\(']
                }
            }
        }

    def init_cache(self):
        """初始化缓存数据库"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS web_info (
                url TEXT PRIMARY KEY,
                data TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_from_cache(self, url):
        """从缓存获取数据"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        cursor.execute('SELECT data, timestamp FROM web_info WHERE url = ?', (url,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            data, timestamp = result
            cache_time = datetime.fromisoformat(timestamp)
            if datetime.now() - cache_time < timedelta(hours=self.cache_hours):
                return json.loads(data)
        return None

    def save_to_cache(self, url, data):
        """保存数据到缓存"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO web_info (url, data, timestamp)
            VALUES (?, ?, ?)
        ''', (url, json.dumps(data), datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def detect(self, url, use_cache=True):
        """检测网站技术栈"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 尝试从缓存获取
        if use_cache:
            cached_data = self.get_from_cache(url)
            if cached_data:
                cached_data['from_cache'] = True
                return cached_data
        
        try:
            print(f"正在检测: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            result = {
                'url': url,
                'status': 'success',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'from_cache': False
            }
            
            # 按分类检测
            for category, techs in self.rules.items():
                for tech_name, rules in techs.items():
                    if self._check_tech(response, soup, rules):
                        result[category] = tech_name
                        break
            
            # 保存到缓存
            if use_cache:
                self.save_to_cache(url, result)
            
            return result
            
        except Exception as e:
            error_result = {
                'url': url,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'from_cache': False
            }
            return error_result

    def _check_tech(self, response, soup, rules):
        """检查是否使用了某项技术"""
        # 检查HTTP头
        if 'headers' in rules:
            for header, value in rules['headers'].items():
                if header in response.headers:
                    if not value:  # 如果value为空，只检查header存在
                        return True
                    if value.lower() in response.headers[header].lower():
                        return True
        
        # 检查HTML内容
        if 'html' in rules:
            for pattern in rules['html']:
                if re.search(pattern, response.text, re.IGNORECASE):
                    return True
        
        # 检查脚本标签
        if 'scripts' in rules:
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script.get('src', '')
                for pattern in rules['scripts']:
                    if re.search(pattern, src, re.IGNORECASE):
                        return True
        
        # 检查CSS链接
        if 'css' in rules:
            links = soup.find_all('link', rel='stylesheet')
            for link in links:
                href = link.get('href', '')
                for pattern in rules['css']:
                    if re.search(pattern, href, re.IGNORECASE):
                        return True
        
        # 检查DOM元素
        if 'dom' in rules:
            for selector in rules['dom']:
                try:
                    if soup.select(selector):
                        return True
                except:
                    continue
        
        # 检查Meta标签
        if 'meta' in rules:
            for meta_rule in rules['meta']:
                if soup.find('meta', attrs=meta_rule):
                    return True
        
        return False

    def save_to_csv(self, results, filename=None):
        """保存结果到CSV文件，追加新数据并保留自定义列"""
    # 使用固定文件名，除非通过 --output 指定
        if not filename:
            filename = 'tech_detection.csv'
        
        # 核心字段
        core_fieldnames = ['URL', '状态', 'JavaScript框架/库', 'CSS框架', 'UI组件库', 
                        'CMS', '后端技术', '服务器', '分析工具', '其他工具', 
                        '检测时间', '缓存状态', '错误信息']
        
        # 检查文件是否存在并获取现有字段和数据
        existing_urls = set()
        existing_data = []
        all_fieldnames = core_fieldnames.copy()  # 默认使用核心字段
        file_exists = os.path.exists(filename)
        
        if file_exists:
            try:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    # 获取现有字段（包括自定义列）
                    all_fieldnames = reader.fieldnames or core_fieldnames
                    # 确保核心字段都在
                    for field in core_fieldnames:
                        if field not in all_fieldnames:
                            all_fieldnames.append(field)
                    # 读取现有数据
                    existing_data = list(reader)
                    existing_urls = {row['URL'] for row in existing_data if 'URL' in row}
            except Exception as e:
                print(f"检查文件 {filename} 时出错: {e}")
                # 如果文件损坏，保留核心字段继续写入
        
        # 准备写入数据
        new_results = 0
        with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames, extrasaction='ignore')
            # 如果文件不存在，写入表头
            if not file_exists:
                writer.writeheader()
            
            # 写入未重复的URL结果
            for result in results:
                if result['url'] in existing_urls:
                    print(f"URL {result['url']} 已存在，跳过保存。")
                    continue
                # 构建新行，保留现有字段的默认值
                row = {field: '' for field in all_fieldnames}  # 初始化所有字段为空
                row.update({
                    'URL': result['url'],
                    '状态': '检测失败' if result['status'] == 'error' else '成功',
                    'JavaScript框架/库': result.get('JavaScript 框架/库', ''),
                    'CSS框架': result.get('CSS 框架', ''),
                    'UI组件库': result.get('UI 组件库', ''),
                    'CMS': result.get('CMS', ''),
                    '后端技术': result.get('后端技术', ''),
                    '服务器': result.get('服务器', ''),
                    '分析工具': result.get('分析工具', ''),
                    '其他工具': result.get('其他工具', ''),
                    '检测时间': result['timestamp'],
                    '缓存状态': '缓存' if result.get('from_cache') else '实时',
                    '错误信息': result.get('error', '') if result['status'] == 'error' else ''
                })
                writer.writerow(row)
                existing_urls.add(result['url'])
                new_results += 1
        if new_results > 0:
            print(f"已保存 {new_results} 条新结果到: {filename}")
        else:
            print(f"没有新结果保存到: {filename}")
        return filename

    def display_console(self, results):
        """在控制台简单显示结果"""
        print(f"\n检测结果 ({len(results)} 个网站):")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            cache_status = "缓存" if result.get('from_cache') else "实时"
            print(f"\n{i}. {result['url']}")
            print(f"   状态: {result['status']} ({cache_status})")
            
            if result['status'] == 'error':
                print(f"   错误: {result.get('error', '')}")
            else:
                # 只显示检测到的技术
                detected = []
                categories = ['JavaScript 框架/库', 'CSS 框架', 'UI 组件库', 'CMS', 
                             '后端技术', '服务器', '分析工具', '其他工具']
                
                for category in categories:
                    if category in result:
                        detected.append(f"{category}: {result[category]}")
                
                if detected:
                    print("   检测到的技术:")
                    for tech in detected:
                        print(f"     - {tech}")
                else:
                    print("   未检测到已知技术")

    def clear_cache(self):
        """清空缓存"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tech_cache')
        conn.commit()
        conn.close()
        print("缓存已清空")

    def show_cache_stats(self):
        """显示缓存统计"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM web_info')
        count = cursor.fetchone()[0]
        conn.close()
        print(f"缓存中共有 {count} 条记录")

def main():
    parser = argparse.ArgumentParser(description='网站技术栈检测器（生成CSV表格）')
    parser.add_argument('urls', nargs='*', help='要检测的网站URL（可以是多个）')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    parser.add_argument('--clear-cache', action='store_true', help='清空缓存')
    parser.add_argument('--cache-stats', action='store_true', help='显示缓存统计')
    parser.add_argument('--output', '-o', help='指定CSV输出文件名')
    parser.add_argument('--format', choices=['csv', 'json', 'console'], default='csv', 
                       help='输出格式 (默认: csv)')
    
    args = parser.parse_args()
    
    detector = TechDetectorWithCache()
    
    # 处理缓存相关命令
    if args.clear_cache:
        detector.clear_cache()
        return
    
    if args.cache_stats:
        detector.show_cache_stats()
        return
    
    # 如果没有提供URL，交互式输入
    urls = args.urls
    if not urls:
        try:
            url_input = input("请输入要检测的网站URL（多个URL用空格分隔）: ").strip()
            if url_input:
                urls = url_input.split()
        except KeyboardInterrupt:
            print("\n检测已取消")
            return
    
    if not urls:
        print("未提供URL")
        return
    
    # 检测所有URL
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 检测中...")
        result = detector.detect(url, use_cache=not args.no_cache)
        results.append(result)
    
    # 显示结果
    if args.format == 'csv':
        detector.save_to_csv(results, args.output)
        detector.display_console(results)  # 同时在控制台显示摘要
    elif args.format == 'json':
        for result in results:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:  # console
        detector.display_console(results)

if __name__ == '__main__':
    main()
import sqlite3
from datetime import datetime
from typing import Dict


class Database:
    def __init__(self, db_path: str = "notes.db"):
        """
        初始化数据库连接
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)  # 允许多线程访问
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        """
        初始化数据库表
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                note_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT,
                discovered_time TEXT NOT NULL,
                type TEXT
            )
        ''')
        self.conn.commit()

    def add_note_if_not_exists(self, note_data: Dict) -> bool:
        """
        添加笔记记录
        :param note_data: 笔记数据
        :return: 是否为新笔记
        """
        try:
            note_id = note_data.get('note_id')
            user_id = note_data.get('user', {}).get('user_id')
            title = note_data.get('display_title', '无标题')
            discovered_time = note_data.get('discovered_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            note_type = note_data.get('type', 'normal')

            if not note_id or not user_id:
                print("缺少必要字段: note_id 或 user_id，跳过插入")
                return False

            self.cursor.execute('SELECT 1 FROM notes WHERE note_id = ?', (note_id,))
            if self.cursor.fetchone():
                return False  # 笔记已存在

            # 插入新笔记
            self.cursor.execute('''
                INSERT INTO notes (note_id, user_id, title, discovered_time, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (note_id, user_id, title, discovered_time, note_type))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as e:
            print(f"数据库插入错误: {e}")
            self.conn.rollback()
            return False

    def get_user_notes_count(self, user_id: str) -> int:
        """
        获取数据库中某用户的笔记数量
        :param user_id: 用户ID
        :return: 笔记数量
        """
        self.cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()[0]

    def __del__(self):
        """
        关闭数据库连接
        """
        if hasattr(self, 'conn'):
            self.conn.close()

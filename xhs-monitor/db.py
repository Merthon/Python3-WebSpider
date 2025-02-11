import sqlite3
from datetime import datetime
from typing import List

class Database:
    def __init__(self, db_path: str = "notes.db"):
        """
        初始化数据库连接
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """
        初始化数据库表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    note_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT,
                    discovered_time TEXT NOT NULL,
                    type TEXT
                )
            ''')
            conn.commit()
    
    def add_note_if_not_exists(self, note_data: dict) -> bool:
        """
        添加笔记记录
        :param note_data: 笔记数据
        :return: 是否为新笔记
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT note_id FROM notes WHERE note_id = ?', 
                         (note_data.get('note_id'),))
            if cursor.fetchone():
                return False
                
            # 插入新笔记
            cursor.execute('''
                INSERT INTO notes (
                    note_id, user_id, title, discovered_time, type
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                note_data.get('note_id'),
                note_data.get('user').get('user_id'),
                note_data.get('display_title', '无标题'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                note_data.get('type', 'normal')
            ))
            conn.commit()
            return True
    
    def get_user_notes_count(self, user_id: str) -> int:
        """
        获取数据库中某用户的笔记数量
        :param user_id: 用户ID
        :return: 笔记数量
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,))
            count = cursor.fetchone()[0]
            print(f"用户 {user_id} 的笔记数量: {count}")
            return count or 0
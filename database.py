"""
ملف إدارة قاعدة البيانات SQLite لنظام CRM محل الخياطة
"""

import sqlite3
import os
from datetime import datetime


class Database:
    def __init__(self, db_path="tailor_crm.db"):
        """
        تهيئة قاعدة البيانات
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """
        إنشاء اتصال بقاعدة البيانات
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
        return conn
    
    def init_database(self):
        """
        إنشاء جداول قاعدة البيانات إذا لم تكن موجودة
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول العملاء
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE,
                address TEXT,
                email TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الطلبات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_type TEXT NOT NULL,
                status TEXT DEFAULT 'قيد التنفيذ',
                order_date TEXT DEFAULT CURRENT_TIMESTAMP,
                delivery_date TEXT,
                total_amount REAL DEFAULT 0,
                paid_amount REAL DEFAULT 0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # جدول القياسات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_id INTEGER,
                height REAL,
                shoulder_width REAL,
                sleeve_length REAL,
                chest_width REAL,
                waist_width REAL,
                neck_size REAL,
                arm_circumference REAL,
                thigh_circumference REAL,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        
        # جدول المواعيد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                purpose TEXT NOT NULL,
                status TEXT DEFAULT 'مجدول',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # جدول المدفوعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT DEFAULT 'نقداً',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("تم إنشاء قاعدة البيانات بنجاح!")
    
    def execute_query(self, query, params=None):
        """
        تنفيذ استعلام SQL
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"خطأ في قاعدة البيانات: {e}")
            return None
        finally:
            conn.close()
    
    def execute_insert(self, query, params=None):
        """
        تنفيذ استعلام إدراج وإرجاع ID الصف الجديد
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"خطأ في قاعدة البيانات: {e}")
            return None
        finally:
            conn.close()
    
    def get_current_timestamp(self):
        """
        الحصول على الوقت الحالي بتنسيق مناسب
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# اختبار قاعدة البيانات
if __name__ == "__main__":
    db = Database()
    print("تم إنشاء قاعدة البيانات وجداولها بنجاح!")


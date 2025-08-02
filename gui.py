"""
واجهة المستخدم الرسومية لنظام CRM محل الخياطة
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTabWidget, QLabel, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLineEdit, 
                            QTextEdit, QComboBox, QDateEdit, QTimeEdit,
                            QDialog, QFormLayout, QDialogButtonBox, 
                            QMessageBox, QHeaderView, QSpinBox, QDoubleSpinBox,
                            QGroupBox, QGridLayout, QFrame, QSplitter)
from PyQt6.QtCore import Qt, QDate, QTime, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from logic import CRMLogic
from models import Customer, Order, Measurement, Appointment, Payment
from datetime import datetime


class MainWindow(QMainWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self):
        super().__init__()
        self.crm = CRMLogic()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("نظام إدارة محل الخياطة الرجالية")
        self.setGeometry(100, 100, 1200, 800)
        
        # إعداد الخط العربي
        font = QFont("Arial", 10)
        self.setFont(font)
        
        # إنشاء التبويبات الرئيسية
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # إنشاء التبويبات
        self.create_dashboard_tab()
        self.create_customers_tab()
        self.create_orders_tab()
        self.create_measurements_tab()
        self.create_appointments_tab()
        self.create_payments_tab()
        
        # تطبيق الستايل
        self.apply_style()
    
    def apply_style(self):
        """تطبيق الستايل على التطبيق"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
        }
        QTabBar::tab {
            background-color: #e0e0e0;
            padding: 8px 16px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #4CAF50;
            color: white;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QTableWidget {
            gridline-color: #d0d0d0;
            background-color: white;
            alternate-background-color: #f9f9f9;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {
            border: 1px solid #d0d0d0;
            padding: 6px;
            border-radius: 4px;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #d0d0d0;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """
        self.setStyleSheet(style)
    
    def create_dashboard_tab(self):
        """إنشاء تبويب لوحة التحكم"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان لوحة التحكم
        title = QLabel("لوحة التحكم")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # إحصائيات سريعة
        stats_layout = QHBoxLayout()
        
        # بطاقات الإحصائيات
        self.customers_card = self.create_stat_card("العملاء", "0", "#2196F3")
        self.orders_card = self.create_stat_card("الطلبات", "0", "#FF9800")
        self.revenue_card = self.create_stat_card("الإيرادات", "0 ريال", "#4CAF50")
        self.appointments_card = self.create_stat_card("مواعيد اليوم", "0", "#9C27B0")
        
        stats_layout.addWidget(self.customers_card)
        stats_layout.addWidget(self.orders_card)
        stats_layout.addWidget(self.revenue_card)
        stats_layout.addWidget(self.appointments_card)
        
        layout.addLayout(stats_layout)
        
        # جدول مواعيد اليوم
        appointments_group = QGroupBox("مواعيد اليوم")
        appointments_layout = QVBoxLayout()
        
        self.today_appointments_table = QTableWidget()
        self.today_appointments_table.setColumnCount(4)
        self.today_appointments_table.setHorizontalHeaderLabels(["العميل", "الوقت", "الغرض", "الحالة"])
        appointments_layout.addWidget(self.today_appointments_table)
        
        appointments_group.setLayout(appointments_layout)
        layout.addWidget(appointments_group)
        
        dashboard_widget.setLayout(layout)
        self.tabs.addTab(dashboard_widget, "لوحة التحكم")
    
    def create_stat_card(self, title, value, color):
        """إنشاء بطاقة إحصائية"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }}
            QLabel {{
                border: none;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 12))
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        
        # حفظ مرجع لتحديث القيمة لاحقاً
        card.value_label = value_label
        
        return card
    
    def create_customers_tab(self):
        """إنشاء تبويب العملاء"""
        customers_widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        
        add_customer_btn = QPushButton("إضافة عميل جديد")
        add_customer_btn.clicked.connect(self.add_customer_dialog)
        
        edit_customer_btn = QPushButton("تعديل عميل")
        edit_customer_btn.clicked.connect(self.edit_customer_dialog)
        
        delete_customer_btn = QPushButton("حذف عميل")
        delete_customer_btn.clicked.connect(self.delete_customer)
        delete_customer_btn.setStyleSheet("background-color: #f44336;")
        
        search_layout = QHBoxLayout()
        search_label = QLabel("البحث:")
        self.customer_search = QLineEdit()
        self.customer_search.setPlaceholderText("ابحث بالاسم أو رقم الهاتف...")
        self.customer_search.textChanged.connect(self.search_customers)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.customer_search)
        
        buttons_layout.addWidget(add_customer_btn)
        buttons_layout.addWidget(edit_customer_btn)
        buttons_layout.addWidget(delete_customer_btn)
        buttons_layout.addStretch()
        buttons_layout.addLayout(search_layout)
        
        layout.addLayout(buttons_layout)
        
        # جدول العملاء
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(5)
        self.customers_table.setHorizontalHeaderLabels(["ID", "الاسم", "رقم الهاتف", "العنوان", "البريد الإلكتروني"])
        self.customers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # إخفاء عمود ID
        self.customers_table.setColumnHidden(0, True)
        
        layout.addWidget(self.customers_table)
        
        customers_widget.setLayout(layout)
        self.tabs.addTab(customers_widget, "العملاء")
    
    def create_orders_tab(self):
        """إنشاء تبويب الطلبات"""
        orders_widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        
        add_order_btn = QPushButton("إضافة طلب جديد")
        add_order_btn.clicked.connect(self.add_order_dialog)
        
        edit_order_btn = QPushButton("تعديل طلب")
        edit_order_btn.clicked.connect(self.edit_order_dialog)
        
        delete_order_btn = QPushButton("حذف طلب")
        delete_order_btn.clicked.connect(self.delete_order)
        delete_order_btn.setStyleSheet("background-color: #f44336;")
        
        buttons_layout.addWidget(add_order_btn)
        buttons_layout.addWidget(edit_order_btn)
        buttons_layout.addWidget(delete_order_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # جدول الطلبات
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(8)
        self.orders_table.setHorizontalHeaderLabels([
            "ID", "العميل", "نوع الطلب", "الحالة", "تاريخ الطلب", 
            "المبلغ الإجمالي", "المبلغ المدفوع", "المبلغ المتبقي"
        ])
        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # إخفاء عمود ID
        self.orders_table.setColumnHidden(0, True)
        
        layout.addWidget(self.orders_table)
        
        orders_widget.setLayout(layout)
        self.tabs.addTab(orders_widget, "الطلبات")
    
    def create_measurements_tab(self):
        """إنشاء تبويب القياسات"""
        measurements_widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        
        add_measurement_btn = QPushButton("إضافة قياس جديد")
        add_measurement_btn.clicked.connect(self.add_measurement_dialog)
        
        buttons_layout.addWidget(add_measurement_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # جدول القياسات
        self.measurements_table = QTableWidget()
        self.measurements_table.setColumnCount(7)
        self.measurements_table.setHorizontalHeaderLabels([
            "ID", "العميل", "الطول", "عرض الكتف", "طول الكم", "عرض الصدر", "تاريخ القياس"
        ])
        self.measurements_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # إخفاء عمود ID
        self.measurements_table.setColumnHidden(0, True)
        
        layout.addWidget(self.measurements_table)
        
        measurements_widget.setLayout(layout)
        self.tabs.addTab(measurements_widget, "القياسات")
    
    def create_appointments_tab(self):
        """إنشاء تبويب المواعيد"""
        appointments_widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        
        add_appointment_btn = QPushButton("إضافة موعد جديد")
        add_appointment_btn.clicked.connect(self.add_appointment_dialog)
        
        buttons_layout.addWidget(add_appointment_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # جدول المواعيد
        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(6)
        self.appointments_table.setHorizontalHeaderLabels([
            "ID", "العميل", "التاريخ", "الوقت", "الغرض", "الحالة"
        ])
        self.appointments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # إخفاء عمود ID
        self.appointments_table.setColumnHidden(0, True)
        
        layout.addWidget(self.appointments_table)
        
        appointments_widget.setLayout(layout)
        self.tabs.addTab(appointments_widget, "المواعيد")
    
    def create_payments_tab(self):
        """إنشاء تبويب المدفوعات"""
        payments_widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        
        add_payment_btn = QPushB

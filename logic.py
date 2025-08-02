"""
منطق العمل (Business Logic) لنظام CRM محل الخياطة
"""

from database import Database
from models import Customer, Order, Measurement, Appointment, Payment
from datetime import datetime
from typing import List, Optional


class CRMLogic:
    def __init__(self):
        """تهيئة منطق العمل"""
        self.db = Database()
    
    # ==================== إدارة العملاء ====================
    
    def add_customer(self, customer: Customer) -> Optional[int]:
        """إضافة عميل جديد"""
        try:
            current_time = self.db.get_current_timestamp()
            customer.created_at = current_time
            customer.updated_at = current_time
            
            query = '''
                INSERT INTO customers (name, phone, address, email, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (customer.name, customer.phone, customer.address, 
                     customer.email, customer.created_at, customer.updated_at)
            
            return self.db.execute_insert(query, params)
        except Exception as e:
            print(f"خطأ في إضافة العميل: {e}")
            return None
    
    def get_all_customers(self) -> List[Customer]:
        """الحصول على جميع العملاء"""
        try:
            query = "SELECT * FROM customers ORDER BY name"
            results = self.db.execute_query(query)
            
            customers = []
            if results:
                for row in results:
                    customer = Customer.from_dict(dict(row))
                    customers.append(customer)
            
            return customers
        except Exception as e:
            print(f"خطأ في جلب العملاء: {e}")
            return []
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """الحصول على عميل بواسطة ID"""
        try:
            query = "SELECT * FROM customers WHERE id = ?"
            results = self.db.execute_query(query, (customer_id,))
            
            if results:
                return Customer.from_dict(dict(results[0]))
            return None
        except Exception as e:
            print(f"خطأ في جلب العميل: {e}")
            return None
    
    def update_customer(self, customer: Customer) -> bool:
        """تحديث بيانات عميل"""
        try:
            customer.updated_at = self.db.get_current_timestamp()
            
            query = '''
                UPDATE customers 
                SET name = ?, phone = ?, address = ?, email = ?, updated_at = ?
                WHERE id = ?
            '''
            params = (customer.name, customer.phone, customer.address, 
                     customer.email, customer.updated_at, customer.id)
            
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"خطأ في تحديث العميل: {e}")
            return False
    
    def delete_customer(self, customer_id: int) -> bool:
        """حذف عميل"""
        try:
            # التحقق من وجود طلبات مرتبطة بالعميل
            orders = self.get_orders_by_customer(customer_id)
            if orders:
                print("لا يمكن حذف العميل لوجود طلبات مرتبطة به")
                return False
            
            query = "DELETE FROM customers WHERE id = ?"
            self.db.execute_query(query, (customer_id,))
            return True
        except Exception as e:
            print(f"خطأ في حذف العميل: {e}")
            return False
    
    def search_customers(self, search_term: str) -> List[Customer]:
        """البحث عن العملاء"""
        try:
            query = '''
                SELECT * FROM customers 
                WHERE name LIKE ? OR phone LIKE ? OR address LIKE ?
                ORDER BY name
            '''
            search_pattern = f"%{search_term}%"
            params = (search_pattern, search_pattern, search_pattern)
            results = self.db.execute_query(query, params)
            
            customers = []
            if results:
                for row in results:
                    customer = Customer.from_dict(dict(row))
                    customers.append(customer)
            
            return customers
        except Exception as e:
            print(f"خطأ في البحث عن العملاء: {e}")
            return []
    
    # ==================== إدارة الطلبات ====================
    
    def add_order(self, order: Order) -> Optional[int]:
        """إضافة طلب جديد"""
        try:
            current_time = self.db.get_current_timestamp()
            if not order.order_date:
                order.order_date = current_time
            order.created_at = current_time
            order.updated_at = current_time
            
            query = '''
                INSERT INTO orders (customer_id, order_type, status, order_date, 
                                  delivery_date, total_amount, paid_amount, notes, 
                                  created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (order.customer_id, order.order_type, order.status, 
                     order.order_date, order.delivery_date, order.total_amount,
                     order.paid_amount, order.notes, order.created_at, order.updated_at)
            
            return self.db.execute_insert(query, params)
        except Exception as e:
            print(f"خطأ في إضافة الطلب: {e}")
            return None
    
    def get_all_orders(self) -> List[dict]:
        """الحصول على جميع الطلبات مع أسماء العملاء"""
        try:
            query = '''
                SELECT o.*, c.name as customer_name
                FROM orders o
                JOIN customers c ON o.customer_id = c.id
                ORDER BY o.order_date DESC
            '''
            results = self.db.execute_query(query)
            
            orders = []
            if results:
                for row in results:
                    order_dict = dict(row)
                    orders.append(order_dict)
            
            return orders
        except Exception as e:
            print(f"خطأ في جلب الطلبات: {e}")
            return []
    
    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        """الحصول على طلبات عميل معين"""
        try:
            query = "SELECT * FROM orders WHERE customer_id = ? ORDER BY order_date DESC"
            results = self.db.execute_query(query, (customer_id,))
            
            orders = []
            if results:
                for row in results:
                    order = Order.from_dict(dict(row))
                    orders.append(order)
            
            return orders
        except Exception as e:
            print(f"خطأ في جلب طلبات العميل: {e}")
            return []
    
    def update_order(self, order: Order) -> bool:
        """تحديث طلب"""
        try:
            order.updated_at = self.db.get_current_timestamp()
            
            query = '''
                UPDATE orders 
                SET customer_id = ?, order_type = ?, status = ?, order_date = ?,
                    delivery_date = ?, total_amount = ?, paid_amount = ?, 
                    notes = ?, updated_at = ?
                WHERE id = ?
            '''
            params = (order.customer_id, order.order_type, order.status,
                     order.order_date, order.delivery_date, order.total_amount,
                     order.paid_amount, order.notes, order.updated_at, order.id)
            
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"خطأ في تحديث الطلب: {e}")
            return False
    
    def delete_order(self, order_id: int) -> bool:
        """حذف طلب"""
        try:
            # حذف المدفوعات المرتبطة بالطلب أولاً
            self.db.execute_query("DELETE FROM payments WHERE order_id = ?", (order_id,))
            
            # حذف الطلب
            query = "DELETE FROM orders WHERE id = ?"
            self.db.execute_query(query, (order_id,))
            return True
        except Exception as e:
            print(f"خطأ في حذف الطلب: {e}")
            return False
    
    # ==================== إدارة القياسات ====================
    
    def add_measurement(self, measurement: Measurement) -> Optional[int]:
        """إضافة قياس جديد"""
        try:
            current_time = self.db.get_current_timestamp()
            measurement.created_at = current_time
            measurement.updated_at = current_time
            
            query = '''
                INSERT INTO measurements (customer_id, order_id, height, shoulder_width,
                                        sleeve_length, chest_width, waist_width, neck_size,
                                        arm_circumference, thigh_circumference, notes,
                                        created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (measurement.customer_id, measurement.order_id, measurement.height,
                     measurement.shoulder_width, measurement.sleeve_length, measurement.chest_width,
                     measurement.waist_width, measurement.neck_size, measurement.arm_circumference,
                     measurement.thigh_circumference, measurement.notes, measurement.created_at,
                     measurement.updated_at)
            
            return self.db.execute_insert(query, params)
        except Exception as e:
            print(f"خطأ في إضافة القياس: {e}")
            return None
    
    def get_all_measurements(self) -> List[dict]:
        """الحصول على جميع القياسات مع أسماء العملاء"""
        try:
            query = '''
                SELECT m.*, c.name as customer_name
                FROM measurements m
                JOIN customers c ON m.customer_id = c.id
                ORDER BY m.created_at DESC
            '''
            results = self.db.execute_query(query)
            
            measurements = []
            if results:
                for row in results:
                    measurement_dict = dict(row)
                    measurements.append(measurement_dict)
            
            return measurements
        except Exception as e:
            print(f"خطأ في جلب القياسات: {e}")
            return []
    
    def get_measurements_by_customer(self, customer_id: int) -> List[Measurement]:
        """الحصول على قياسات عميل معين"""
        try:
            query = "SELECT * FROM measurements WHERE customer_id = ? ORDER BY created_at DESC"
            results = self.db.execute_query(query, (customer_id,))
            
            measurements = []
            if results:
                for row in results:
                    measurement = Measurement.from_dict(dict(row))
                    measurements.append(measurement)
            
            return measurements
        except Exception as e:
            print(f"خطأ في جلب قياسات العميل: {e}")
            return []
    
    # ==================== إدارة المواعيد ====================
    
    def add_appointment(self, appointment: Appointment) -> Optional[int]:
        """إضافة موعد جديد"""
        try:
            current_time = self.db.get_current_timestamp()
            appointment.created_at = current_time
            appointment.updated_at = current_time
            
            query = '''
                INSERT INTO appointments (customer_id, date, time, purpose, status, 
                                        notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (appointment.customer_id, appointment.date, appointment.time,
                     appointment.purpose, appointment.status, appointment.notes,
                     appointment.created_at, appointment.updated_at)
            
            return self.db.execute_insert(query, params)
        except Exception as e:
            print(f"خطأ في إضافة الموعد: {e}")
            return None
    
    def get_all_appointments(self) -> List[dict]:
        """الحصول على جميع المواعيد مع أسماء العملاء"""
        try:
            query = '''
                SELECT a.*, c.name as customer_name
                FROM appointments a
   

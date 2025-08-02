#!/usr/bin/env python3
"""
نقطة الدخول الرئيسية لنظام CRM محل الخياطة
"""

import sys
import os

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main

if __name__ == "__main__":
    main()


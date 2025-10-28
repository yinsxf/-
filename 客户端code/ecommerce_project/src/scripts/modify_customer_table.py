#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修改customers表结构，添加phone和gender字段
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.database import Database


def main():
    """主函数"""
    print("开始修改customers表结构...")
    
    # 初始化数据库连接
    db = Database()
    
    # 检查并添加phone字段
    try:
        # 先检查字段是否存在
        check_query = "SHOW COLUMNS FROM customers LIKE 'phone'"
        result = db.execute_query(check_query)
        
        if not result:
            # 字段不存在，添加phone字段
            alter_query = "ALTER TABLE customers ADD COLUMN phone VARCHAR(20) DEFAULT ''"
            db.execute_update(alter_query)
            print("✅ 成功添加phone字段")
        else:
            print("ℹ️ phone字段已存在")
    except Exception as e:
        print(f"❌ 添加phone字段失败: {str(e)}")
    
    # 检查并添加gender字段
    try:
        # 先检查字段是否存在
        check_query = "SHOW COLUMNS FROM customers LIKE 'gender'"
        result = db.execute_query(check_query)
        
        if not result:
            # 字段不存在，添加gender字段
            alter_query = "ALTER TABLE customers ADD COLUMN gender VARCHAR(10) DEFAULT NULL"
            db.execute_update(alter_query)
            print("✅ 成功添加gender字段")
        else:
            print("ℹ️ gender字段已存在")
    except Exception as e:
        print(f"❌ 添加gender字段失败: {str(e)}")
    
    print("表结构修改完成！")


if __name__ == "__main__":
    main()
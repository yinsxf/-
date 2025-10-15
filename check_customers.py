#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查customers表中存在的客户ID
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.database import Database


def check_customers():
    """检查customers表中的客户数据"""
    print("开始检查customers表...")
    
    # 创建数据库连接
    db = Database()
    
    try:
        # 查询前10个客户ID
        query = "SELECT customer_id FROM customers LIMIT 10"
        result = db.execute_query(query)
        
        if result:
            print(f"✅ 找到 {len(result)} 个客户ID:")
            for row in result:
                print(f"  - {row['customer_id']}")
        else:
            print("❌ 未找到任何客户数据")
        
        # 查询客户表的总记录数
        count_query = "SELECT COUNT(*) as count FROM customers"
        count_result = db.execute_query(count_query)
        
        if count_result:
            total_count = count_result[0]['count']
            print(f"\n总客户数量: {total_count}")
        
    except Exception as e:
        print(f"❌ 查询过程中发生错误: {str(e)}")
    
    # 关闭数据库连接
    db.close()


if __name__ == "__main__":
    check_customers()
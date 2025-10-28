# -*- coding: utf-8 -*-
"""
检查表结构的脚本，用于查看customers表的实际列名
"""

from src.models.database import Database

if __name__ == "__main__":
    try:
        # 连接数据库
        db = Database()
        
        # 查询表结构
        query = "SHOW COLUMNS FROM customers"
        columns = db.execute_query(query)
        
        if columns:
            print("✅ customers表结构:")
            for col in columns:
                print(f"列名: {col['Field']}, 类型: {col['Type']}, 是否可为空: {col['Null']}")
        else:
            print("❌ 无法获取表结构")
            
        # 检查是否有旧表结构的客户表（可能使用name而不是first_name/last_name）
        query = "SELECT COUNT(*) as count FROM customers"
        result = db.execute_query(query)
        if result:
            print(f"\n✅ 客户表记录数: {result[0]['count']}")
        else:
            print("❌ 无法获取记录数")
            
    except Exception as e:
        print(f"❌ 执行过程中出错: {str(e)}")
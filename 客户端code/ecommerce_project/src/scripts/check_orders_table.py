#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查看orders表的结构
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.database import Database


def main():
    """主函数"""
    print("开始查看orders表结构...")
    
    # 初始化数据库连接
    db = Database()
    
    try:
        # 查询表结构
        query = "SHOW COLUMNS FROM orders"
        result = db.execute_query(query)
        
        if result:
            print("\norders表结构：")
            print("+----------------+--------------+------+-----+---------+----------------+")
            print("| Field          | Type         | Null | Key | Default | Extra          |")
            print("+----------------+--------------+------+-----+---------+----------------+")
            for row in result:
                field = row['Field']
                type_ = row['Type']
                null_ = row['Null']
                key = row['Key']
                default = row['Default'] if row['Default'] is not None else "NULL"
                extra = row['Extra']
                
                print(f"| {field:<14} | {type_:<12} | {null_:<4} | {key:<3} | {default:<7} | {extra:<14} |")
            print("+----------------+--------------+------+-----+---------+----------------+")
        else:
            print("无法查询orders表结构")
    except Exception as e:
        print(f"查询表结构失败: {str(e)}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清除客户管理中所有数据的脚本
"""

import os
import sys
import argparse

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.customer import Customer


def clear_all_customers_data(auto_confirm=False):
    """清除所有客户数据"""
    try:
        # 创建Customer模型实例
        customer_model = Customer()
        
        # 获取当前客户数量
        current_count = customer_model.count_customers()
        print(f"当前客户数量: {current_count}")
        
        # 确认操作
        if not auto_confirm:
            confirm = input("确定要清除所有客户数据吗？这将无法恢复！(y/N): ")
            if confirm.lower() != 'y':
                print("操作已取消。")
                return
        else:
            print("已通过命令行参数确认清除所有客户数据！")
        
        # 清除所有客户数据
        result = customer_model.clear_all_customers()
        
        if result:
            print("✅ 所有客户数据已成功清除！")
            # 验证清除结果
            new_count = customer_model.count_customers()
            print(f"清除后客户数量: {new_count}")
        else:
            print("❌ 清除客户数据失败！")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='清除客户管理中所有数据')
    parser.add_argument('--auto-confirm', '-y', action='store_true', help='自动确认清除操作')
    args = parser.parse_args()
    
    clear_all_customers_data(auto_confirm=args.auto_confirm)
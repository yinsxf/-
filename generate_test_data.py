#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量数据生成工具入口脚本
用于生成大量测试数据插入到数据库中
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.bulk_data_generator import BulkDataGenerator


def main():
    """主函数"""
    print("===== 电子商务系统批量数据生成工具 =====")
    print("此工具将生成大量测试数据插入到数据库中")
    print("\n注意：")
    print("1. 请确保您的数据库连接配置正确")
    print("2. 生成大量数据可能需要一些时间")
    print("3. 生成过程中会显示进度信息")
    
    try:
        generator = BulkDataGenerator()
        
        # 直接使用默认值，不询问用户输入
        customers_count = 1000
        products_count = 1000
        orders_count = 1000
        
        # 开始生成数据
        print("\n开始生成数据...")
        result = generator.generate_all_data(customers_count, products_count, orders_count)
        
        print("\n===== 数据生成结果汇总 =====")
        print(f"成功生成的客户数量: {result['customers']}")
        print(f"成功生成的商品数量: {result['products']}")
        print(f"成功生成的订单数量: {result['orders']}")
        print("\n数据生成工具执行完成！")
        
    except Exception as e:
        print(f"数据生成过程中出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
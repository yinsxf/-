#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成大量客户数据的脚本
"""
import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.data_generator import DataGenerator


def main():
    """主函数"""
    print("开始生成大量客户数据...")
    start_time = time.time()
    
    # 初始化数据生成器
    generator = DataGenerator()
    
    # 设置要生成的客户数量
    customer_count = 100000
    
    # 生成客户数据
    print(f"正在生成{customer_count}条客户数据...")
    created_count = generator.generate_customers(customer_count)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"客户数据生成完成！")
    print(f"成功生成: {created_count}条客户数据")
    print(f"总耗时: {elapsed_time:.2f}秒")
    print(f"平均每秒生成: {created_count/elapsed_time:.2f}条记录")


if __name__ == "__main__":
    main()
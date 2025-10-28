#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成大量订单数据的脚本 - 优化版
"""
import os
import sys
import time
import random

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.data_generator import DataGenerator

def main():
    """主函数"""
    print("开始生成大量订单数据...")
    start_time = time.time()
    
    # 初始化数据生成器
    generator = DataGenerator()
    
    # 确保有足够的商品数据
    product_count = generator.product_model.count_products()
    if product_count < 100:
        print(f"商品数量不足，需要至少100个商品，当前有{product_count}个商品")
        print("开始生成额外的商品数据...")
        # 生成额外的商品数据
        needed_products = 100 - product_count
        if needed_products > 0:
            products_created = generator.generate_products(needed_products)
            print(f"成功生成{products_created}个额外的商品数据")
    
    # 设置要生成的订单数量
    order_count = 100000
    
    # 分批生成订单，每批生成一定数量
    batch_size = 1000  # 减小批次大小，避免数据库锁等待超时
    max_retries = 3    # 每批次的最大重试次数
    total_created = 0
    
    print(f"总共需要生成{order_count}条订单数据")
    
    # 循环生成订单
    for i in range(0, order_count, batch_size):
        current_batch = min(batch_size, order_count - i)
        print(f"\n--- 正在生成第{i+1}-{i+current_batch}条订单 ---\n")
        
        batch_created = 0
        retries = 0
        
        # 尝试多次生成，直到成功或达到最大重试次数
        while batch_created < current_batch and retries < max_retries:
            retries += 1
            print(f"尝试第{retries}次生成...")
            
            try:
                batch_start = time.time()
                # 每次尝试生成剩余的订单数量
                to_create = current_batch - batch_created
                created = generator.generate_orders(to_create)
                batch_created += created
                
                batch_time = time.time() - batch_start
                
                if created > 0:
                    print(f"✅ 成功生成{created}条订单数据")
                    print(f"⏱️  本次尝试耗时: {batch_time:.2f}秒")
                    print(f"📊  平均每秒生成: {created/batch_time:.2f}条订单")
                    print(f"📈  本批次累计生成: {batch_created}/{current_batch}条订单")
                else:
                    print(f"❌ 本次尝试生成失败")
            except Exception as e:
                print(f"生成过程中发生错误: {str(e)}")
                print("将在短暂暂停后继续尝试...")
            
            # 每尝试一次后休息一下
            if batch_created < current_batch and retries < max_retries:
                # 随机等待时间，避免连续的压力
                wait_time = random.uniform(2, 5)
                print(f"休息{wait_time:.1f}秒后继续...")
                time.sleep(wait_time)
        
        # 累加总创建数量
        total_created += batch_created
        
        if batch_created < current_batch:
            print(f"⚠️  本批次仅成功生成{batch_created}/{current_batch}条订单，已达到最大重试次数")
        
        # 每完成一批次，短暂休息一下，避免数据库压力过大
        if i + current_batch < order_count:
            rest_time = random.uniform(2, 5)
            print(f"休息{rest_time:.2f}秒...")
            time.sleep(rest_time)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n订单数据生成完成！")
    print(f"成功生成: {total_created}条订单数据")
    print(f"总耗时: {elapsed_time:.2f}秒")
    print(f"平均每秒生成: {total_created/elapsed_time:.2f}条记录")


if __name__ == "__main__":
    main()
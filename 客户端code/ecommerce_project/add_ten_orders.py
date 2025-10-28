#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
向系统中添加10条订单的脚本
"""
import os
import sys
import random

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.order import Order
from src.models.product import Product


def add_ten_orders():
    """添加10条订单到系统中"""
    print("开始向系统中添加10条订单...")
    
    # 创建订单和商品实例
    order_model = Order()
    product_model = Product()
    
    # 有效的客户ID列表（从customers表查询结果中获取）
    valid_customer_ids = [30527, 71041, 80021, 80024, 80025, 80028, 80033, 80036, 80037, 80041]
    
    # 有效的订单状态
    valid_statuses = ['pending', 'paid', 'shipped']
    
    # 统计成功创建的订单数量
    success_count = 0
    
    # 获取所有可用的商品
    products = product_model.get_all_products()
    if not products:
        print("❌ 没有可用的商品数据，无法创建订单")
        return
    
    for i in range(10):
        try:
            # 随机选择一个客户ID
            customer_id = random.choice(valid_customer_ids)
            
            # 随机选择一个订单状态
            status = random.choice(valid_statuses)
            
            # 为订单创建订单项（1-3个商品）
            num_items = random.randint(1, 3)
            order_items = []
            total_amount = 0
            
            # 随机选择商品并创建订单项
            selected_products = random.sample(products, num_items)
            for product in selected_products:
                # 随机选择数量（1-5个），但不超过库存
                max_quantity = min(5, product['stock_quantity'])
                if max_quantity <= 0:
                    continue  # 跳过无库存的商品
                
                quantity = random.randint(1, max_quantity)
                unit_price = product['price']
                subtotal = quantity * unit_price
                
                order_items.append({
                    'product_id': product['product_id'],
                    'product_name': product['name'],
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'subtotal': subtotal
                })
                
                total_amount += subtotal
            
            # 如果没有有效的订单项，跳过此订单
            if not order_items:
                print(f"❌ 创建订单 #{i+1} 失败: 没有可用的商品")
                continue
            
            # 构建订单数据
            order_data = {
                'customer_id': customer_id,
                'status': status,
                'items': order_items
            }
            
            # 创建订单
            order_id = order_model.create_order(order_data)
            
            if order_id:
                print(f"✅ 成功创建订单 #{i+1}: 订单ID={order_id}, 客户ID={customer_id}, 金额={total_amount:.2f}, 状态={status}")
                print(f"  📦 包含 {len(order_items)} 个订单项")
                success_count += 1
            else:
                print(f"❌ 创建订单 #{i+1} 失败")
                
        except Exception as e:
            print(f"❌ 创建订单 #{i+1} 时发生错误: {str(e)}")
    
    print(f"\n订单添加完成！成功创建了 {success_count} 条订单。")
    
    # 显示当前系统中的订单总数
    total_orders = order_model.count_orders()
    print(f"系统中当前共有 {total_orders} 条订单。")


if __name__ == "__main__":
    add_ten_orders()
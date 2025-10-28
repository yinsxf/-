#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试重新编写的订单管理模块
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.order import Order


def test_order_module():
    """测试订单管理模块的基本功能"""
    print("开始测试订单管理模块...")
    
    # 创建订单实例
    order_model = Order()
    print(f"订单基本属性: {order_model.attributes}")
    
    try:
        # 测试1: 创建新订单
        print("\n测试1: 创建新订单")
        # 使用有效的客户ID（从customers表查询结果中获取）
        valid_customer_id = 30527  # 第一个有效的客户ID
        new_order_id = order_model.create_order(
            customer_id=valid_customer_id,
            total_amount=99.99,
            status='pending'
        )
        
        if new_order_id:
            print(f"✅ 成功创建订单，订单ID: {new_order_id}")
        else:
            print("❌ 创建订单失败")
            return
        
        # 测试2: 根据ID获取订单
        print("\n测试2: 根据ID获取订单")
        order = order_model.get_order_by_id(new_order_id)
        
        if order:
            print(f"✅ 成功获取订单信息:")
            for attr in order_model.attributes:
                print(f"  {attr}: {order.get(attr)}")
        else:
            print("❌ 无法获取订单信息")
        
        # 测试3: 更新订单状态
        print("\n测试3: 更新订单状态")
        new_status = 'paid'
        update_success = order_model.update_order_status(new_order_id, new_status)
        
        if update_success:
            print(f"✅ 成功将订单状态更新为: {new_status}")
            # 验证状态更新是否成功
            updated_order = order_model.get_order_by_id(new_order_id)
            print(f"  验证后订单状态: {updated_order.get('status')}")
        else:
            print("❌ 更新订单状态失败")
        
        # 测试4: 获取指定客户的订单
        print("\n测试4: 获取指定客户的订单")
        customer_orders = order_model.get_orders_by_customer_id(customer_id=1)
        
        if customer_orders:
            print(f"✅ 成功获取客户订单，共 {len(customer_orders)} 条订单")
        else:
            print("❌ 未找到客户订单")
        
        # 测试5: 获取所有订单
        print("\n测试5: 获取所有订单")
        all_orders = order_model.get_all_orders()
        
        if all_orders:
            print(f"✅ 成功获取所有订单，共 {len(all_orders)} 条订单")
        else:
            print("❌ 未找到任何订单")
        
        print("\n订单管理模块测试完成!")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")


if __name__ == "__main__":
    test_order_module()
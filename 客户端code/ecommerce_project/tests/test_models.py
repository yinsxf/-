import unittest
import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.models.customer import Customer
from src.models.product import Product
from src.models.order import Order
from src.models.database import Database

class TestModels(unittest.TestCase):
    """模型测试类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建模型实例
        self.customer_model = Customer()
        self.product_model = Product()
        self.order_model = Order()
        
        # 清理测试数据 - 确保测试环境是干净的
        # 1. 清理测试客户
        try:
            existing_customer = self.customer_model.get_customer_by_email("test@example.com")
            if existing_customer and hasattr(self.customer_model, 'delete_customer'):
                self.customer_model.delete_customer(existing_customer['customer_id'])
        except Exception as e:
            print(f"清理测试客户数据时出错: {str(e)}")
        
        # 2. 添加测试客户 - 注意数据库表只有name和email字段
        success = self.customer_model.add_customer(
            name="测试用户",
            email="test@example.com"
        )
        self.assertTrue(success)
        
        # 获取测试客户ID
        customer = self.customer_model.get_customer_by_email("test@example.com")
        self.test_customer_id = customer['customer_id'] if customer else None
        self.assertIsNotNone(self.test_customer_id, "测试客户ID获取失败")
        
        # 2. 添加测试商品 - 注意数据库表只有name, price, stock_quantity, category_id字段
        success = self.product_model.add_product(
            name="测试商品",
            price=99.99,
            stock_quantity=100,
            category_id=None  # 可以先设为None
        )
        self.assertTrue(success)
        
        # 获取测试商品ID
        products = self.product_model.get_all_products()
        test_product = None
        for p in products:
            if p['name'] == "测试商品":
                test_product = p
                break
        
        self.test_product_id = test_product['product_id'] if test_product else None
        self.assertIsNotNone(self.test_product_id, "测试商品ID获取失败")
        
        # 3. 创建测试订单
        self.test_order_items = [
            {'product_id': self.test_product_id, 'quantity': 2}
        ]
        
    def test_customer_model(self):
        """测试客户模型"""
        # 检查客户ID是否有效
        self.assertIsNotNone(self.test_customer_id, "测试客户ID无效")
        
        # 测试获取客户信息
        customer = self.customer_model.get_customer_by_id(self.test_customer_id)
        self.assertIsNotNone(customer)
        self.assertEqual(customer['email'], "test@example.com")
        
        # 测试更新客户信息 - 只更新name字段，避免邮箱冲突
        updated = self.customer_model.update_customer(
            self.test_customer_id,
            name="更新后用户"
        )
        self.assertTrue(updated)
        
        # 验证更新结果
        updated_customer = self.customer_model.get_customer_by_id(self.test_customer_id)
        self.assertEqual(updated_customer['name'], "更新后用户")
        
    def test_product_model(self):
        """测试商品模型"""
        # 检查商品ID是否有效
        self.assertIsNotNone(self.test_product_id, "测试商品ID无效")
        
        # 测试获取商品信息
        product = self.product_model.get_product_by_id(self.test_product_id)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "测试商品")
        self.assertEqual(product['stock_quantity'], 100)
        
        # 测试更新商品信息
        updated = self.product_model.update_product(
            self.test_product_id,
            price=129.99
        )
        self.assertTrue(updated)
        
        # 验证更新结果（注意：数据库返回的价格是Decimal类型）
        updated_product = self.product_model.get_product_by_id(self.test_product_id)
        from decimal import Decimal
        self.assertEqual(updated_product['price'], Decimal('129.99'))
        
        # 测试库存操作 - 如果decrease_stock和increase_stock方法存在
        # 先检查这些方法是否存在
        if hasattr(self.product_model, 'decrease_stock'):
            # 减少库存
            decreased = self.product_model.decrease_stock(self.test_product_id, 10)
            self.assertTrue(decreased)
            
            # 验证库存减少
            product_after_decrease = self.product_model.get_product_by_id(self.test_product_id)
            self.assertEqual(product_after_decrease['stock_quantity'], 90)
            
            # 增加库存
            if hasattr(self.product_model, 'increase_stock'):
                increased = self.product_model.increase_stock(self.test_product_id, 5)
                self.assertTrue(increased)
                
                # 验证库存增加
                product_after_increase = self.product_model.get_product_by_id(self.test_product_id)
                self.assertEqual(product_after_increase['stock_quantity'], 95)
        
    def test_order_model(self):
        """测试订单模型"""
        # 检查客户ID和商品ID是否有效
        self.assertIsNotNone(self.test_customer_id, "测试客户ID无效")
        self.assertIsNotNone(self.test_product_id, "测试商品ID无效")
        
        # 测试创建订单 - 适配新的方法签名（不再接受shipping_address和payment_method）
        order_id = self.order_model.create_order(
            customer_id=self.test_customer_id,
            items=self.test_order_items
        )
        self.assertIsNotNone(order_id)
        
        # 测试获取订单信息
        order = self.order_model.get_order_by_id(order_id)
        self.assertIsNotNone(order)
        self.assertEqual(order['customer_id'], self.test_customer_id)
        
        # 测试获取订单详情
        order_items = self.order_model.get_order_items(order_id)
        self.assertGreater(len(order_items), 0)
        
        # 测试获取客户订单
        customer_orders = self.order_model.get_orders_by_customer_id(self.test_customer_id)
        self.assertGreater(len(customer_orders), 0)
        
        # 测试取消订单
        cancelled = self.order_model.cancel_order(order_id)
        self.assertTrue(cancelled)
        
        # 验证订单状态
        cancelled_order = self.order_model.get_order_by_id(order_id)
        self.assertEqual(cancelled_order['status'], 'cancelled')
        
    def tearDown(self):
        """清理测试环境"""
        # 清理测试数据，确保测试之间互不影响
        try:
            # 1. 清理测试客户
            if hasattr(self.customer_model, 'delete_customer') and self.test_customer_id:
                try:
                    self.customer_model.delete_customer(self.test_customer_id)
                except Exception as e:
                    print(f"清理测试客户失败: {str(e)}")
            
            # 2. 清理测试商品
            if hasattr(self.product_model, 'delete_product') and self.test_product_id:
                try:
                    self.product_model.delete_product(self.test_product_id)
                except Exception as e:
                    print(f"清理测试商品失败: {str(e)}")
        except Exception as e:
            print(f"清理测试数据时出错: {str(e)}")

if __name__ == '__main__':
    unittest.main()
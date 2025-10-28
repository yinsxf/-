import time
import random
from datetime import datetime
from faker import Faker
from ..models.customer import Customer
from ..models.product import Product
from ..models.order import Order

class BulkDataGenerator:
    """批量数据生成器 - 与现有模型类接口兼容"""
    
    def __init__(self):
        """初始化数据生成器"""
        self.customer_model = Customer()
        self.product_model = Product()
        self.order_model = Order()
        self.faker = Faker('zh_CN')
        
        # 商品类别和品牌
        self.product_categories = [
            '手机', '笔记本电脑', '平板电脑', '智能穿戴', '音频设备',
            '存储设备', '网络设备', '办公设备', '游戏设备', '摄影设备'
        ]
        
        self.product_brands = [
            'Apple', 'Samsung', 'Huawei', 'Xiaomi', 'OPPO', 'Vivo',
            'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Sony',
            'Bose', 'JBL', 'Logitech', 'Canon', 'Nikon', 'TP-Link'
        ]
        
        # 记录生成的ID，用于生成订单
        self.generated_customer_ids = []
        self.generated_product_ids = []
    
    def generate_customers(self, count=1000):
        """生成指定数量的客户数据"""
        print(f"开始生成{count}个客户数据...")
        start_time = time.time()
        created_count = 0
        
        for i in range(count):
            # 生成客户姓名
            name = self.faker.name()
            
            # 生成唯一邮箱
            email = f"{name.lower().replace(' ', '_')}_{i}@{self.faker.free_email_domain()}"
            
            # 确保邮箱唯一
            existing_customer = self.customer_model.get_customer_by_email(email)
            while existing_customer:
                email = f"{name.lower().replace(' ', '_')}_{i}_{random.randint(1000, 9999)}@{self.faker.free_email_domain()}"
                existing_customer = self.customer_model.get_customer_by_email(email)
            
            # 注意：根据表结构检查结果，数据库只接受name和email字段
            # 这里我们通过修改模型调用方式来适应实际表结构
            # 由于BulkDataGenerator是为了生成大量测试数据，我们暂时使用name和email两个字段
            # 注意：这种方式可能与模型定义不匹配，但能适应现有表结构
            
            # 直接使用name和email字段插入数据
            query = "INSERT INTO customers (name, email) VALUES (%s, %s)"
            params = (name, email)
            # 直接使用数据库连接执行SQL
            affected_rows = self.customer_model.db.execute_update(query, params)
            
            if affected_rows > 0:
                created_count += 1
                # 获取刚添加的客户ID
                new_customer = self.customer_model.get_customer_by_email(email)
                if new_customer:
                    self.generated_customer_ids.append(new_customer['customer_id'])
            
            # 打印进度
            if (i + 1) % 100 == 0:
                elapsed_time = time.time() - start_time
                rate = (i + 1) / elapsed_time if elapsed_time > 0 else 0
                print(f"已生成{i + 1}/{count}个客户，速度: {rate:.2f}个/秒")
        
        total_time = time.time() - start_time
        print(f"成功生成{created_count}个客户数据，耗时: {total_time:.2f}秒")
        return created_count
    
    def generate_products(self, count=1000):
        """生成指定数量的商品数据"""
        print(f"开始生成{count}个商品数据...")
        start_time = time.time()
        created_count = 0
        
        # 按品牌和类别准备更合理的商品描述词
        product_descriptions = {
            '手机': ['Pro', 'Max', 'Mini', '青春版', '旗舰版', '尊享版', '标准版'],
            '笔记本电脑': ['超薄本', '游戏本', '商务本', '触控本', '二合一', '工作站', '学生本'],
            '平板电脑': ['Pro', 'Air', 'Mini', '青春版', '教育版', '游戏平板', '商务平板'],
            '智能穿戴': ['智能手表', '运动手环', '智能眼镜', '蓝牙耳机', '智能耳机', '健康监测器'],
            '音频设备': ['无线耳机', '头戴式耳机', '入耳式耳机', '音箱', '音响', '蓝牙音箱', '家庭影院'],
            '存储设备': ['移动硬盘', '固态硬盘', 'U盘', '内存卡', '存储卡', '网盘服务'],
            '网络设备': ['路由器', '交换机', '网卡', '调制解调器', 'WiFi放大器', '网络摄像头'],
            '办公设备': ['打印机', '扫描仪', '传真机', '投影仪', '电子白板', '一体机'],
            '游戏设备': ['游戏手柄', '游戏鼠标', '游戏键盘', '游戏耳机', '电竞显示器', '游戏主机'],
            '摄影设备': ['单反相机', '微单相机', '数码相机', '镜头', '三脚架', '相机包', '闪光灯']
        }
        
        for i in range(count):
            try:
                # 生成商品名称 - 直接使用品牌 类别 数字的格式
                category = random.choice(self.product_categories)
                brand = random.choice(self.product_brands)
                
                # 70%的概率添加一个随机数字型号
                if random.random() > 0.3:  # 70%的概率有型号
                    model_num = random.randint(100, 999)
                    product_name = f"{brand} {category} {model_num}"
                else:
                    product_name = f"{brand} {category}"
                
                # 生成价格和库存
                price = round(random.uniform(99.99, 9999.99), 2)
                stock_quantity = random.randint(10, 200)
                
                # 添加商品 - 不传递category_id参数，因为数据库中没有categories表
                product_id = self.product_model.add_product(product_name, price, stock_quantity)
                if product_id:
                    created_count += 1
                    self.generated_product_ids.append(product_id)
                
            except Exception as e:
                print(f"生成商品时出错: {str(e)}")
                continue
            
            # 打印进度
            if (i + 1) % 100 == 0:
                elapsed_time = time.time() - start_time
                rate = (i + 1) / elapsed_time if elapsed_time > 0 else 0
                print(f"已生成{i + 1}/{count}个商品，速度: {rate:.2f}个/秒")
        
        total_time = time.time() - start_time
        print(f"成功生成{created_count}个商品数据，耗时: {total_time:.2f}秒")
        return created_count
    
    def generate_orders(self, count=1000):
        """生成指定数量的订单数据"""
        print(f"开始生成{count}个订单数据...")
        
        # 确保有足够的客户和商品数据
        if not self.generated_customer_ids:
            print("正在获取现有客户数据...")
            customers = self.customer_model.get_all_customers()
            if not customers:
                print("没有客户数据，需要先生成客户数据")
                return 0
            self.generated_customer_ids = [c['customer_id'] for c in customers]
        
        if not self.generated_product_ids:
            print("正在获取现有商品数据...")
            products = self.product_model.get_all_products()
            if not products:
                print("没有商品数据，需要先生成商品数据")
                return 0
            self.generated_product_ids = [p['product_id'] for p in products]
        
        start_time = time.time()
        created_count = 0
        
        for i in range(count):
            try:
                # 随机选择客户
                customer_id = random.choice(self.generated_customer_ids)
                
                # 随机生成订单项数量（1-5个商品）
                num_items = random.randint(1, 5)
                
                # 随机选择商品并生成订单项
                order_items = []
                # 确保有足够的商品可选
                available_products = self.generated_product_ids.copy()
                if len(available_products) < num_items:
                    num_items = len(available_products)
                
                if num_items > 0:
                    # 随机选择商品ID
                    selected_product_ids = random.sample(available_products, num_items)
                    
                    for product_id in selected_product_ids:
                        # 获取商品信息
                        product = self.product_model.get_product_by_id(product_id)
                        if product and product['stock_quantity'] > 0:
                            # 生成数量，不超过库存
                            quantity = random.randint(1, min(5, product['stock_quantity']))
                            order_items.append({
                                'product_id': product_id,
                                'quantity': quantity
                            })
                
                # 只有当订单项不为空时才创建订单
                if order_items:
                    # 创建订单 - 添加更健壮的错误处理
                    try:
                        if self.order_model.create_order(customer_id, order_items):
                            created_count += 1
                    except Exception as order_error:
                        # 如果是锁等待超时错误，尝试重试一次
                        if "1205" in str(order_error):  # 1205是锁等待超时错误码
                            print(f"订单锁等待超时，尝试重试...")
                            # 等待一小段随机时间后重试
                            time.sleep(random.uniform(0.5, 2.0))
                            if self.order_model.create_order(customer_id, order_items):
                                created_count += 1
                        else:
                            print(f"创建订单时出错: {str(order_error)}")
                
                # 打印进度
                if (i + 1) % 100 == 0:
                    elapsed_time = time.time() - start_time
                    rate = (i + 1) / elapsed_time if elapsed_time > 0 else 0
                    print(f"已生成{i + 1}/{count}个订单，速度: {rate:.2f}个/秒")
            except Exception as e:
                print(f"生成订单时出错: {str(e)}")
                continue
        
        total_time = time.time() - start_time
        print(f"成功生成{created_count}个订单数据，耗时: {total_time:.2f}秒")
        return created_count
    
    def generate_all_data(self, customers_count=1000, products_count=1000, orders_count=1000):
        """生成所有测试数据"""
        result = {}
        
        # 生成客户数据
        result['customers'] = self.generate_customers(customers_count)
        
        # 生成商品数据
        result['products'] = self.generate_products(products_count)
        
        # 生成订单数据
        result['orders'] = self.generate_orders(orders_count)
        
        print("\n批量数据生成完成！")
        print(f"生成的客户数量: {result['customers']}")
        print(f"生成的商品数量: {result['products']}")
        print(f"生成的订单数量: {result['orders']}")
        
        return result

# 如果直接运行此脚本，则执行数据生成
def main():
    """主函数"""
    generator = BulkDataGenerator()
    
    print("===== 批量数据生成工具 =====")
    print("此工具将生成大量测试数据插入到数据库中。")
    print("请确保您的数据库连接配置正确。")
    
    # 询问用户要生成的数据量
    try:
        customers_count = int(input("请输入要生成的客户数量 (默认: 1000): ") or "1000")
        products_count = int(input("请输入要生成的商品数量 (默认: 1000): ") or "1000")
        orders_count = int(input("请输入要生成的订单数量 (默认: 1000): ") or "1000")
        
        # 开始生成数据
        generator.generate_all_data(customers_count, products_count, orders_count)
    except ValueError:
        print("输入错误，请输入有效的数字。")

if __name__ == "__main__":
    main()
import random
import string
from datetime import datetime, timedelta
from ..models.customer import Customer
from ..models.product import Product
from ..models.order import Order

class DataGenerator:
    """测试数据生成器"""
    
    def __init__(self):
        """初始化数据生成器"""
        self.customer_model = Customer()
        self.product_model = Product()
        self.order_model = Order()
        
        # 用于生成随机数据的数据源
        self.first_names = [
            '张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴',
            '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗'
        ]
        
        self.last_names = [
            '伟', '芳', '娜', '秀英', '敏', '静', '强', '磊', '军', '洋',
            '勇', '杰', '丽', '涛', '艳', '超', '明', '刚', '娟', '涛'
        ]
        
        self.cities = [
            '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都',
            '西安', '重庆', '青岛', '大连', '宁波', '厦门', '苏州', '无锡'
        ]
        
        self.states = [
            '北京市', '上海市', '广东省', '江苏省', '浙江省', '湖北省',
            '四川省', '陕西省', '重庆市', '山东省', '辽宁省'
        ]
        
        self.countries = ['中国', '美国', '日本', '韩国', '英国', '法国', '德国']
        
        self.product_names = [
            '智能手机', '笔记本电脑', '平板电脑', '智能手表', '蓝牙耳机',
            '无线充电器', '移动电源', '智能音箱', '游戏手柄', '摄像头',
            '机械键盘', '鼠标', '显示器', '打印机', '扫描仪',
            '路由器', '交换机', '硬盘', 'U盘', '内存卡'
        ]
        
        self.categories = [
            '手机', '笔记本电脑', '平板电脑', '智能穿戴', '音频设备',
            '存储设备', '网络设备', '办公设备', '游戏设备', '摄影设备'
        ]
        
        self.brands = [
            'Apple', 'Samsung', 'Huawei', 'Xiaomi', 'OPPO', 'Vivo',
            'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Sony',
            'Bose', 'JBL', 'Logitech', 'Canon', 'Nikon', 'TP-Link'
        ]
    
    def _generate_random_string(self, length=10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    def _generate_random_email(self):
        """生成随机邮箱"""
        username = self._generate_random_string(8)
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com'])
        return f"{username}@{domain}"
    
    def _generate_random_phone(self):
        """生成随机手机号码"""
        prefix = random.choice(['13', '14', '15', '16', '17', '18', '19'])
        suffix = ''.join(random.choices(string.digits, k=9))
        return prefix + suffix
    
    def _generate_random_address(self):
        """生成随机地址"""
        street = f"{self._generate_random_string(5)}路{random.randint(1, 999)}号"
        city = random.choice(self.cities)
        state = random.choice(self.states)
        zip_code = ''.join(random.choices(string.digits, k=6))
        return street, city, state, zip_code
    
    def generate_customers(self, count=10):
        """生成指定数量的客户数据"""
        created_count = 0
        
        # 用于生成随机性别的选项
        genders = ['male', 'female']
        
        # 批量处理数据，提高性能
        batch_size = 1000  # 每批次处理1000条
        for i in range(0, count, batch_size):
            current_batch = min(batch_size, count - i)
            
            # 准备批量插入的数据
            values = []
            for _ in range(current_batch):
                # 生成客户姓名
                first_name = random.choice(self.first_names)
                last_name = random.choice(self.last_names)
                name = first_name + last_name
                
                email = self._generate_random_email()
                phone = self._generate_random_phone()
                gender = random.choice(genders)
                
                values.extend([name, email, phone, gender])
            
            # 构建批量插入SQL
            placeholders = ', '.join(["(%s, %s, %s, %s)" for _ in range(current_batch)])
            query = f"INSERT INTO customers (name, email, phone, gender) VALUES {placeholders}"
            
            try:
                affected_rows = self.customer_model.db.execute_update(query, values)
                created_count += affected_rows
            except Exception as e:
                print(f"批量插入失败: {str(e)}")
                # 尝试单条插入作为备选方案
                for j in range(current_batch):
                    try:
                        idx = j * 4
                        name, email, phone, gender = values[idx:idx+4]
                        query = "INSERT INTO customers (name, email, phone, gender) VALUES (%s, %s, %s, %s)"
                        if self.customer_model.db.execute_update(query, (name, email, phone, gender)) > 0:
                            created_count += 1
                    except Exception as single_e:
                        print(f"单条插入失败: {str(single_e)}")
        
        return created_count
    
    def generate_products(self, count=20):
        """生成指定数量的商品数据"""
        created_count = 0
        
        for _ in range(count):
            # 生成更真实的商品名称
            base_name = random.choice(self.product_names)
            model_number = f"{self._generate_random_string(3).upper()}-{random.randint(100, 999)}"
            product_name = f"{random.choice(self.brands)} {base_name} {model_number}"
            
            description = f"这是一款高性能的{base_name}，具有出色的功能和质量。"
            price = round(random.uniform(99.99, 9999.99), 2)
            stock_quantity = random.randint(10, 200)
            category = random.choice(self.categories)
            brand = random.choice(self.brands)
            image_url = f"https://example.com/images/{self._generate_random_string(10)}.jpg"
            
            if self.product_model.add_product(
                product_name, description, price, stock_quantity, category, brand, image_url
            ):
                created_count += 1
        
        return created_count
    
    def generate_orders(self, count=50, batch_size=100):
        """生成指定数量的订单数据，支持批量处理"""
        # 获取所有客户和商品
        customers = self.customer_model.get_all_customers()
        products = self.product_model.get_all_products()
        
        if not customers or not products:
            print("没有足够的客户或商品数据生成订单")
            return 0
        
        # 确保商品有足够库存
        self._ensure_product_stock(products, count)
        
        created_count = 0
        
        # 批量处理订单
        for i in range(0, count, batch_size):
            current_batch = min(batch_size, count - i)
            print(f"正在生成第{i+1}-{i+current_batch}条订单...")
            
            # 一次性处理一批订单
            batch_created = self._generate_orders_batch(current_batch, customers, products)
            created_count += batch_created
            
            print(f"已完成批次：成功生成{batch_created}条订单")
        
        return created_count
        
    def _ensure_product_stock(self, products, order_count):
        """确保商品有足够的库存来生成指定数量的订单"""
        # 计算所需的最低库存量
        max_items_per_order = 5  # 每个订单最多5个商品
        needed_per_product = order_count * max_items_per_order // len(products) + 10
        
        for product in products:
            if product['stock_quantity'] < needed_per_product:
                # 增加库存
                self.product_model.update_product(
                    product['product_id'],
                    stock_quantity=needed_per_product
                )
        
    def _generate_orders_batch(self, count, customers, products):
        """批量生成订单数据"""
        created_count = 0
        
        for _ in range(count):
            try:
                # 随机选择客户
                customer = random.choice(customers)
                
                # 随机生成订单项数量（1-5个商品）
                num_items = random.randint(1, 5)
                
                # 随机选择商品并生成订单项
                order_items = []
                selected_products = random.sample(products, min(num_items, len(products)))
                
                for product in selected_products:
                    # 确保库存足够
                    quantity = random.randint(1, min(5, product['stock_quantity']))
                    order_items.append({
                        'product_id': product['product_id'],
                        'quantity': quantity
                    })
                
                # 创建订单（只传递必要的参数）
                order_id = self.order_model.create_order(
                    customer['customer_id'], order_items
                )
                
                if order_id:
                    created_count += 1
                    
                    # 随机更新订单状态（确保使用合法的状态值）
                    status = random.choice(['pending', 'paid', 'shipped', 'cancelled'])
                    self.order_model.update_order_status(order_id, status)
            except Exception as e:
                print(f"生成订单时出错: {str(e)}")
                # 继续处理下一个订单
                continue
        
        return created_count
    
    def generate_all_data(self, customers_count=10, products_count=20, orders_count=50):
        """生成所有测试数据"""
        print(f"开始生成{customers_count}个客户数据...")
        customers_created = self.generate_customers(customers_count)
        print(f"成功生成{customers_created}个客户数据")
        
        print(f"开始生成{products_count}个商品数据...")
        products_created = self.generate_products(products_count)
        print(f"成功生成{products_created}个商品数据")
        
        print(f"开始生成{orders_count}个订单数据...")
        orders_created = self.generate_orders(orders_count)
        print(f"成功生成{orders_created}个订单数据")
        
        return {
            'customers': customers_created,
            'products': products_created,
            'orders': orders_created
        }
    
    def clear_all_data(self):
        """清空所有数据（谨慎使用）"""
        # 注意：这里需要按照外键依赖顺序删除数据
        try:
            # 删除订单详情
            self.customer_model.db.execute_update("DELETE FROM order_items")
            print("已删除所有订单详情数据")
            
            # 删除购物车数据
            self.customer_model.db.execute_update("DELETE FROM cart")
            print("已删除所有购物车数据")
            
            # 删除订单
            self.customer_model.db.execute_update("DELETE FROM orders")
            print("已删除所有订单数据")
            
            # 删除库存日志
            self.customer_model.db.execute_update("DELETE FROM inventory_logs")
            print("已删除所有库存日志数据")
            
            # 删除商品
            self.customer_model.db.execute_update("DELETE FROM products")
            print("已删除所有商品数据")
            
            # 删除客户
            self.customer_model.db.execute_update("DELETE FROM customers")
            print("已删除所有客户数据")
            
            return True
        except Exception as e:
            print(f"清空数据失败: {str(e)}")
            return False
from .database import Database
from .product import Product

class Order:
    """订单模型类，提供完整的订单管理功能"""
    
    def __init__(self):
        """初始化订单模型，创建数据库连接"""
        self.db = Database()
        self.product_model = Product()
        # 定义订单的属性
        self.attributes = ['order_id', 'customer_id', 'total_amount', 'status', 'order_date']
    
    def create_order(self, order_data):
        """创建新订单（兼容GUI和数据生成器）
        参数:
            order_data: 订单数据字典，包含客户ID、订单项等信息
        返回:
            新创建的订单ID，失败则返回None
        """
        try:
            # 处理不同格式的参数
            if isinstance(order_data, dict):
                # GUI格式 - 接受完整的订单数据字典
                customer_id = order_data.get('customer_id')
                status = order_data.get('status', 'pending')
                items = order_data.get('items', [])
            else:
                # 兼容旧格式的调用
                # 第一个参数是customer_id，第二个参数是订单项列表
                customer_id = order_data
                status = 'pending'
                items = None
                # 检查第二个参数是否是订单项列表
                if len(locals()) > 1 and isinstance(list(locals().values())[1], list):
                    items = list(locals().values())[1]
            
            # 验证参数
            if not isinstance(customer_id, int) or customer_id <= 0:
                raise ValueError("客户ID必须是正整数")
            
            if not items or len(items) == 0:
                raise ValueError("订单必须包含至少一个订单项")
            
            # 确保状态值合法
            valid_statuses = ['pending', 'paid', 'shipped', 'cancelled']
            if status not in valid_statuses:
                status = 'pending'
            
            # 使用数据库连接池获取连接
            connection = self.db.get_connection()
            if not connection:
                raise Exception("无法获取数据库连接")
            
            try:
                # 开始事务
                cursor = connection.cursor()
                
                # 计算订单总金额并验证库存
                total_amount = 0
                for item in items:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity', 0)
                    
                    # 获取商品信息
                    product = self.product_model.get_product_by_id(product_id)
                    if not product:
                        raise ValueError(f"商品ID {product_id} 不存在")
                    
                    # 验证库存
                    if product['stock_quantity'] < quantity:
                        raise ValueError(f"商品 {product_id} 库存不足，当前库存: {product['stock_quantity']}")
                    
                    unit_price = item.get('unit_price', product['price'])
                    subtotal = quantity * unit_price
                    total_amount += subtotal
                    
                    # 保存单价和小计，以便后续插入订单项
                    item['unit_price'] = unit_price
                    item['subtotal'] = subtotal
                
                # 插入订单数据
                order_query = """
                INSERT INTO orders (customer_id, total_amount, status)
                VALUES (%s, %s, %s)
                """
                cursor.execute(order_query, (customer_id, float(total_amount), status))
                order_id = cursor.lastrowid
                
                # 插入订单项
                item_query = """
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """
                
                for item in items:
                    cursor.execute(
                        item_query,
                        (
                            order_id,
                            item['product_id'],
                            item['quantity'],
                            float(item['unit_price']),
                            float(item['subtotal'])
                        )
                    )
                    
                    # 减少商品库存
                    self.product_model.decrease_stock(item['product_id'], item['quantity'])
                
                # 提交事务
                connection.commit()
                return order_id
            except Exception as e:
                # 回滚事务
                connection.rollback()
                print(f"创建订单失败: {str(e)}")
                return None
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        except Exception as e:
            print(f"创建订单失败: {str(e)}")
            return None
    
    def get_order_by_id(self, order_id):
        """根据ID获取订单信息
        参数:
            order_id: 订单ID
        返回:
            订单信息字典，不存在则返回None
        """
        try:
            query = "SELECT * FROM orders WHERE order_id = %s"
            result = self.db.execute_query(query, (order_id,))
            return result[0] if result else None
        except Exception as e:
            print(f"获取订单失败: {str(e)}")
            return None
    
    def update_order_status(self, order_id, status):
        """更新订单状态
        参数:
            order_id: 订单ID
            status: 新的订单状态
        返回:
            更新成功返回True，否则返回False
        """
        try:
            # 确保状态值合法
            valid_statuses = ['pending', 'paid', 'shipped', 'cancelled']
            if status not in valid_statuses:
                raise ValueError(f"不合法的订单状态: {status}")
            
            query = "UPDATE orders SET status = %s WHERE order_id = %s"
            affected_rows = self.db.execute_update(query, (status, order_id))
            return affected_rows > 0
        except Exception as e:
            print(f"更新订单状态失败: {str(e)}")
            return False
    
    def get_orders_by_customer_id(self, customer_id):
        """获取指定客户的所有订单
        参数:
            customer_id: 客户ID
        返回:
            订单列表
        """
        try:
            query = "SELECT * FROM orders WHERE customer_id = %s ORDER BY order_date DESC"
            return self.db.execute_query(query, (customer_id,)) or []
        except Exception as e:
            print(f"获取客户订单失败: {str(e)}")
            return []
    
    def get_order_items(self, order_id):
        """获取指定订单的所有订单项
        参数:
            order_id: 订单ID
        返回:
            订单项列表
        """
        try:
            query = """
            SELECT oi.*, p.name as product_name 
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.product_id 
            WHERE oi.order_id = %s
            """
            return self.db.execute_query(query, (order_id,)) or []
        except Exception as e:
            print(f"获取订单项失败: {str(e)}")
            return []
    
    def get_all_orders(self):
        """获取所有订单
        返回:
            订单列表
        """
        try:
            query = "SELECT * FROM orders ORDER BY order_date DESC"
            return self.db.execute_query(query) or []
        except Exception as e:
            print(f"获取所有订单失败: {str(e)}")
            return []
    
    def count_orders(self, status=None):
        """获取订单总数，可以按状态筛选
        参数:
            status: 订单状态，可选
        返回:
            订单总数
        """
        try:
            if status:
                query = "SELECT COUNT(*) as count FROM orders WHERE status = %s"
                result = self.db.execute_query(query, (status,))
            else:
                query = "SELECT COUNT(*) as count FROM orders"
                result = self.db.execute_query(query)
            
            return result[0]['count'] if result else 0
        except Exception as e:
            print(f"获取订单总数失败: {str(e)}")
            return 0
    
    def get_customer_order_count(self, customer_id):
        """获取指定客户的订单数量
        参数:
            customer_id: 客户ID
        返回:
            客户的订单数量
        """
        try:
            query = "SELECT COUNT(*) as count FROM orders WHERE customer_id = %s AND status != 'cancelled'"
            result = self.db.execute_query(query, (customer_id,))
            return result[0]['count'] if result else 0
        except Exception as e:
            print(f"获取客户订单数量失败: {str(e)}")
            return 0
    
    def get_customer_order_statistics(self, customer_id):
        """获取客户的订单统计信息
        参数:
            customer_id: 客户ID
        返回:
            包含订单总数和总消费金额的字典
        """
        try:
            query = """
            SELECT COUNT(*) as order_count, SUM(total_amount) as total_spent 
            FROM orders 
            WHERE customer_id = %s AND status != 'cancelled'
            """
            result = self.db.execute_query(query, (customer_id,))
            
            if result and len(result) > 0:
                stats = result[0]
                return {
                    'order_count': stats['order_count'] or 0,
                    'total_spent': stats['total_spent'] or 0.0
                }
            return {
                'order_count': 0,
                'total_spent': 0.0
            }
        except Exception as e:
            print(f"获取客户订单统计失败: {str(e)}")
            return {
                'order_count': 0,
                'total_spent': 0.0
            }
    
    def search_orders(self, keyword):
        """根据关键字搜索订单
        参数:
            keyword: 搜索关键字
        返回:
            订单列表
        """
        try:
            query = """
            SELECT * FROM orders 
            WHERE order_id LIKE %s OR customer_id LIKE %s
            ORDER BY order_date DESC
            """
            search_keyword = f"%{keyword}%"
            params = (search_keyword, search_keyword)
            return self.db.execute_query(query, params) or []
        except Exception as e:
            print(f"搜索订单失败: {str(e)}")
            return []
    
    def get_orders_by_status(self, status):
        """根据订单状态获取订单
        参数:
            status: 订单状态
        返回:
            订单列表
        """
        try:
            query = "SELECT * FROM orders WHERE status = %s ORDER BY order_date DESC"
            return self.db.execute_query(query, (status,)) or []
        except Exception as e:
            print(f"按状态获取订单失败: {str(e)}")
            return []
from .database import Database

class Customer:
    """客户模型类，用于处理客户相关的数据库操作"""
    
    def __init__(self):
        """初始化客户模型，创建数据库连接"""
        self.db = Database()
    
    def get_all_customers(self):
        """获取所有客户信息"""
        query = "SELECT * FROM customers"
        return self.db.execute_query(query)

    def get_customer_by_id(self, customer_id):
        """根据ID获取客户信息"""
        query = "SELECT * FROM customers WHERE customer_id = %s"
        result = self.db.execute_query(query, (customer_id,))
        return result[0] if result else None
    
    def get_customer_by_email(self, email):
        """根据邮箱获取客户信息"""
        query = "SELECT * FROM customers WHERE email = %s"
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None

    def add_customer(self, customer_data):
        """添加新客户，支持手机号和性别字段"""
        query = """
        INSERT INTO customers (name, email, phone, gender) 
        VALUES (%s, %s, %s, %s)
        """
        params = (
            customer_data['name'],
            customer_data['email'],
            customer_data.get('phone', ''),
            customer_data.get('gender', None)
        )
        
        # 先检查邮箱是否已存在
        if self.check_email_exists(customer_data['email']):
            return None
        
        # 执行插入操作
        affected_rows = self.db.execute_update(query, params)
        
        if affected_rows > 0:
            # 获取新插入的客户ID
            last_id_query = "SELECT LAST_INSERT_ID() as customer_id"
            result = self.db.execute_query(last_id_query)
            return result[0]['customer_id'] if result else None
        
        return None

    def update_customer(self, customer_id, update_data):
        """更新客户信息，适应现有的数据库表结构，支持手机号和性别字段"""
        # 构建更新语句
        set_clause = []
        params = []
        
        if 'name' in update_data:
            set_clause.append("name = %s")
            params.append(update_data['name'])
        if 'email' in update_data:
            set_clause.append("email = %s")
            params.append(update_data['email'])
        if 'phone' in update_data:
            set_clause.append("phone = %s")
            params.append(update_data['phone'])
        if 'gender' in update_data:
            set_clause.append("gender = %s")
            params.append(update_data['gender'] or None)
        
        # 如果没有要更新的字段，直接返回
        if not set_clause:
            return True
        
        # 添加WHERE条件
        set_clause_str = ", ".join(set_clause)
        params.append(customer_id)
        
        query = f"UPDATE customers SET {set_clause_str} WHERE customer_id = %s"
        affected_rows = self.db.execute_update(query, params)
        return affected_rows > 0
    
    def delete_customer(self, customer_id):
        """删除客户"""
        query = "DELETE FROM customers WHERE customer_id = %s"
        affected_rows = self.db.execute_update(query, (customer_id,))
        return affected_rows > 0
    
    def check_email_exists(self, email, exclude_id=None):
        """检查邮箱是否已存在，可选择排除特定客户ID"""
        if exclude_id:
            query = "SELECT * FROM customers WHERE email = %s AND customer_id != %s"
            params = (email, exclude_id)
        else:
            query = "SELECT * FROM customers WHERE email = %s"
            params = (email,)
        
        result = self.db.execute_query(query, params)
        return bool(result)
    
    def search_customers(self, keyword):
        """根据关键字搜索客户，适应现有的数据库表结构"""
        query = """
        SELECT * FROM customers 
        WHERE name LIKE %s OR email LIKE %s
        """
        search_keyword = f"%{keyword}%"
        params = (search_keyword, search_keyword)
        return self.db.execute_query(query, params)
    
    def count_customers(self):
        """获取客户总数"""
        query = "SELECT COUNT(*) as count FROM customers"
        result = self.db.execute_query(query)
        return result[0]['count'] if result else 0
    
    def clear_all_customers(self):
        """清除所有客户数据
        注意：由于外键约束，需要先删除相关的订单数据
        """
        try:
            # 开始事务
            self.db.execute_update("START TRANSACTION")
            
            # 先删除所有订单数据
            self.db.execute_update("DELETE FROM orders")
            
            # 然后删除所有客户数据
            affected_rows = self.db.execute_update("DELETE FROM customers")
            
            # 提交事务
            self.db.execute_update("COMMIT")
            
            return affected_rows >= 0
        except Exception as e:
            # 发生错误时回滚事务
            self.db.execute_update("ROLLBACK")
            print(f"清除客户数据时发生错误: {str(e)}")
            return False
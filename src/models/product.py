from .database import Database

class Product:
    """商品模型类，用于处理商品相关的数据库操作"""
    
    def __init__(self):
        """初始化商品模型，创建数据库连接"""
        self.db = Database()
    
    def get_all_products(self):
        """获取所有商品信息"""
        query = "SELECT * FROM products"
        return self.db.execute_query(query)

    def get_product_by_id(self, product_id):
        """根据ID获取商品信息"""
        query = "SELECT * FROM products WHERE product_id = %s"
        result = self.db.execute_query(query, (product_id,))
        return result[0] if result else None
    
    def add_product(self, product_name, price, stock_quantity):
        """添加新商品 - 与数据库表结构保持一致，不使用category_id参数"""
        query = """
        INSERT INTO products (name, price, stock_quantity)
        VALUES (%s, %s, %s)
        """
        params = (product_name, price, stock_quantity)
        
        try:
            # 使用数据库连接池获取连接
            connection = self.db.get_connection()
            if not connection:
                print("无法获取数据库连接")
                return None
            
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            
            # 获取最后插入的商品ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            product_id = result[0] if result else None
            
            cursor.close()
            connection.close()
            
            # 暂时注释掉库存日志记录，因为inventory_logs表不存在
            # 记录库存日志(如果存在inventory_logs表)
            # if product_id:
            #     try:
            #         self._log_inventory_change(product_id, 0, stock_quantity, stock_quantity, "新增商品")
            #     except Exception as e:
            #         print(f"库存日志记录失败: {str(e)}")
            #         # 不影响主流程，继续返回成功
            
            return product_id
        except Exception as e:
            print(f"添加商品时出错: {str(e)}")
            # 如果有连接，尝试回滚
            if 'connection' in locals() and connection:
                try:
                    connection.rollback()
                except:
                    pass
            return None

    def update_product(self, product_id, product_name=None, price=None, stock_quantity=None):
        """更新商品信息 - 与数据库表结构保持一致，不使用category_id参数"""
        try:
            # 构建更新语句
            set_clause = []
            params = []
            
            if product_name is not None:
                set_clause.append("name = %s")
                params.append(product_name)
            if price is not None:
                set_clause.append("price = %s")
                params.append(price)
            
            # 特殊处理库存数量变更
            old_stock = None
            if stock_quantity is not None:
                # 获取当前库存
                current_product = self.get_product_by_id(product_id)
                if current_product:
                    old_stock = current_product['stock_quantity']
                    set_clause.append("stock_quantity = %s")
                    params.append(stock_quantity)
            
            # 如果没有要更新的字段，直接返回
            if not set_clause:
                return True
            
            # 添加WHERE条件
            set_clause_str = ", ".join(set_clause)
            params.append(product_id)
            
            query = f"UPDATE products SET {set_clause_str} WHERE product_id = %s"
            
            # 使用数据库连接池获取连接
            connection = self.db.get_connection()
            if not connection:
                print("无法获取数据库连接")
                return False
            
            try:
                cursor = connection.cursor()
                cursor.execute(query, params)
                affected_rows = cursor.rowcount
                connection.commit()
                
                # 暂时注释掉库存日志记录，因为inventory_logs表不存在
                # 记录库存变更日志
                # if stock_quantity is not None and old_stock is not None:
                #     change_amount = stock_quantity - old_stock
                #     if change_amount != 0:
                #         change_type = "库存调整"
                #         try:
                #             self._log_inventory_change(product_id, old_stock, stock_quantity, change_amount, change_type)
                #         except Exception as log_error:
                #             print(f"记录库存日志失败: {str(log_error)}")
                #             # 不影响主流程，继续返回成功
                
                return affected_rows > 0
            except Exception as e:
                print(f"执行更新操作失败: {str(e)}")
                # 尝试回滚
                try:
                    connection.rollback()
                except:
                    pass
                return False
            finally:
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'connection' in locals() and connection:
                    connection.close()
        except Exception as e:
            print(f"更新商品失败: {str(e)}")
            return False
    
    def delete_product(self, product_id):
        """删除商品"""
        query = "DELETE FROM products WHERE product_id = %s"
        affected_rows = self.db.execute_update(query, (product_id,))
        return affected_rows > 0
    
    def search_products(self, keyword):
        """根据关键字搜索商品"""
        query = """
        SELECT * FROM products 
        WHERE name LIKE %s OR description LIKE %s OR category LIKE %s OR brand LIKE %s
        """
        search_keyword = f"%{keyword}%"
        params = (search_keyword, search_keyword, search_keyword, search_keyword)
        return self.db.execute_query(query, params)
    
    def get_products_by_category(self, category):
        """根据分类获取商品"""
        query = "SELECT * FROM products WHERE category = %s"
        return self.db.execute_query(query, (category,))
    
    def get_products_by_brand(self, brand):
        """根据品牌获取商品"""
        query = "SELECT * FROM products WHERE brand = %s"
        return self.db.execute_query(query, (brand,))
    
    def decrease_stock(self, product_id, quantity):
        """减少商品库存"""
        try:
            # 获取当前库存
            current_product = self.get_product_by_id(product_id)
            if not current_product:
                return False
            
            current_stock = current_product['stock_quantity']
            if current_stock < quantity:
                return False  # 库存不足
            
            new_stock = current_stock - quantity
            query = "UPDATE products SET stock_quantity = %s WHERE product_id = %s"
            affected_rows = self.db.execute_update(query, (new_stock, product_id))
            
            # 暂时注释掉库存日志记录，因为inventory_logs表不存在
            # 记录库存变更日志 - 即使日志失败也不影响核心业务
            # if affected_rows > 0:
            #     try:
            #         self._log_inventory_change(product_id, current_stock, new_stock, -quantity, "销售出库")
            #     except Exception as log_error:
            #         print(f"记录库存日志失败: {str(log_error)}")
            
            return affected_rows > 0
        except Exception as e:
            print(f"减少库存失败: {str(e)}")
            return False

    def increase_stock(self, product_id, quantity):
        """增加商品库存"""
        try:
            # 获取当前库存
            current_product = self.get_product_by_id(product_id)
            if not current_product:
                return False
            
            current_stock = current_product['stock_quantity']
            new_stock = current_stock + quantity
            
            query = "UPDATE products SET stock_quantity = %s WHERE product_id = %s"
            affected_rows = self.db.execute_update(query, (new_stock, product_id))
            
            # 暂时注释掉库存日志记录，因为inventory_logs表不存在
            # 记录库存变更日志 - 即使日志失败也不影响核心业务
            # if affected_rows > 0:
            #     try:
            #         self._log_inventory_change(product_id, current_stock, new_stock, quantity, "采购入库")
            #     except Exception as log_error:
            #         print(f"记录库存日志失败: {str(log_error)}")
            
            return affected_rows > 0
        except Exception as e:
            print(f"增加库存失败: {str(e)}")
            return False

    def _log_inventory_change(self, product_id, previous_quantity, current_quantity, change_amount, change_type, changed_by="系统"):
        """记录库存变更日志"""
        query = """
        INSERT INTO inventory_logs (product_id, previous_quantity, current_quantity, change_amount, change_type, changed_by)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (product_id, previous_quantity, current_quantity, change_amount, change_type, changed_by)
        self.db.execute_update(query, params)
    
    def get_inventory_logs(self, product_id=None):
        """获取库存变更日志"""
        if product_id:
            query = "SELECT * FROM inventory_logs WHERE product_id = %s ORDER BY changed_at DESC"
            return self.db.execute_query(query, (product_id,))
        else:
            query = "SELECT * FROM inventory_logs ORDER BY changed_at DESC"
            return self.db.execute_query(query)
    
    def count_products(self):
        """获取商品总数"""
        query = "SELECT COUNT(*) as count FROM products"
        result = self.db.execute_query(query)
        return result[0]['count'] if result else 0
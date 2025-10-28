import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.models.database import Database

class TestDatabase(unittest.TestCase):
    """数据库操作测试类"""
    
    def setUp(self):
        """每个测试方法执行前的设置"""
        # 创建数据库连接实例
        self.db = Database()
    
    def tearDown(self):
        """每个测试方法执行后的清理"""
        # 关闭连接资源
        self.db.close()
    
    def test_connection(self):
        """测试数据库连接"""
        # 检查连接池是否初始化成功
        self.assertIsNotNone(self.db.connection_pool)
    
    def test_execute_query(self):
        """测试执行查询操作"""
        # 执行一个简单的查询
        result = self.db.execute_query("SELECT 1 + 1 AS result")
        
        # 检查结果是否正确
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['result'], 2)
    
    def test_execute_update(self):
        """测试执行更新操作"""
        # 创建一个测试表
        self.db.execute_update("DROP TABLE IF EXISTS test_table")
        self.db.execute_update("CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(100))")
        
        # 插入测试数据
        affected_rows = self.db.execute_update("INSERT INTO test_table (id, name) VALUES (1, 'test')")
        
        # 检查影响的行数
        self.assertEqual(affected_rows, 1)
        
        # 验证数据是否插入成功
        result = self.db.execute_query("SELECT * FROM test_table WHERE id = 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'test')
        
        # 清理测试表
        self.db.execute_update("DROP TABLE test_table")
    
    def test_transaction(self):
        """测试事务操作"""
        try:
            # 开始事务
            self.db.execute_update("START TRANSACTION")
            
            # 创建测试表
            self.db.execute_update("DROP TABLE IF EXISTS test_transaction")
            self.db.execute_update("CREATE TABLE test_transaction (id INT PRIMARY KEY, value INT)")
            
            # 插入测试数据
            self.db.execute_update("INSERT INTO test_transaction (id, value) VALUES (1, 100)")
            self.db.execute_update("UPDATE test_transaction SET value = 200 WHERE id = 1")
            
            # 提交事务
            self.db.execute_update("COMMIT")
            
            # 验证数据是否正确
            result = self.db.execute_query("SELECT value FROM test_transaction WHERE id = 1")
            self.assertEqual(result[0]['value'], 200)
            
        except Exception as e:
            # 回滚事务
            self.db.execute_update("ROLLBACK")
            self.fail(f"事务测试失败: {str(e)}")
        finally:
            # 清理测试表
            self.db.execute_update("DROP TABLE IF EXISTS test_transaction")

if __name__ == '__main__':
    unittest.main()
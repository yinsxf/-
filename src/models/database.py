import os
from configparser import ConfigParser
import mysql.connector
import mysql.connector.pooling

class Database:
    """数据库连接和基础操作类"""
    
    def __init__(self):
        """初始化数据库连接池"""
        self.connection_pool = None
        self.init_connection_pool()
    
    def init_connection_pool(self):
        """初始化数据库连接池"""
        try:
            # 读取配置文件
            config = ConfigParser()
            config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'database.ini')
            
            if os.path.exists(config_file):
                config.read(config_file)
                host = config.get('database', 'host')
                user = config.get('database', 'user')
                password = config.get('database', 'password')
                database = config.get('database', 'dbname')  # 注意这里修改为dbname
                port = config.getint('database', 'port')
                charset = config.get('database', 'charset')
            else:
                # 如果配置文件不存在，使用默认值
                host = '192.168.214.128'  # 注意这里修改为服务器IP
                user = 'dev_user'
                password = 'AQ815X&aq815x'
                database = 'ecommerce'
                port = 3306
                charset = 'utf8mb4'
            
            # 创建连接池配置
            db_config = {
                'host': host,
                'port': port,
                'database': database,
                'user': user,
                'password': password,
                'charset': charset,
                'autocommit': False  # 建议关闭自动提交以支持事务
            }
            
            # 初始化连接池
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="ecommerce_pool",
                pool_size=5,
                **db_config
            )
            
            print("数据库连接池初始化成功")
            
            # 测试连接
            self.test_connection()
            
        except Exception as e:
            print(f"数据库连接池初始化失败: {str(e)}")
            self.connection_pool = None
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            conn = self.get_connection()
            if conn and conn.is_connected():
                print("✅ 数据库连接成功")
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"MySQL服务器版本: {version[0]}")
                cursor.close()
                conn.close()
                return True
            return False
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False
    
    def get_connection(self):
        """从连接池获取连接"""
        if not self.connection_pool:
            self.init_connection_pool()
        
        if self.connection_pool:
            try:
                return self.connection_pool.get_connection()
            except Exception as e:
                print(f"获取数据库连接失败: {str(e)}")
                # 尝试重新初始化连接池
                self.init_connection_pool()
                if self.connection_pool:
                    return self.connection_pool.get_connection()
        
        return None
    
    def execute_query(self, query, params=None):
        """执行查询语句并返回结果"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"查询执行失败: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_update(self, query, params=None):
        """执行更新语句（插入、更新、删除）并提交"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            if not connection:
                return 0
            
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            affected_rows = cursor.rowcount
            connection.commit()
            return affected_rows
        except Exception as e:
            print(f"更新执行失败: {str(e)}")
            if connection:
                try:
                    connection.rollback()
                except:
                    pass
            return 0
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def close(self):
        """关闭连接池"""
        # 连接池会自动管理连接的生命周期
        # 这里可以添加一些清理操作
        print("数据库连接资源已释放")
    
    def __del__(self):
        """析构函数"""
        self.close()
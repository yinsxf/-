import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ecommerce_project.src.models.database import Database

# 创建数据库连接
db = Database()

# 测试连接
connection = db.get_connection()
if connection:
    print("✅ 数据库连接成功")
    
    try:
        # 检查products表结构
        cursor = connection.cursor()
        cursor.execute("DESCRIBE products")
        columns = cursor.fetchall()
        
        print("\nproducts表结构:")
        for column in columns:
            print(f"- {column[0]}: {column[1]}")
        
        # 尝试简单查询
        cursor.execute("SELECT COUNT(*) as count FROM products")
        result = cursor.fetchone()
        print(f"\n当前商品数量: {result[0]}")
        
        # 尝试插入一条简单数据
        test_product = "测试商品" 
        test_price = 99.99
        test_stock = 10
        
        cursor.execute(
            "INSERT INTO products (name, price, stock_quantity) VALUES (%s, %s, %s)",
            (test_product, test_price, test_stock)
        )
        connection.commit()
        print(f"\n✅ 成功插入测试商品")
        
        # 查询刚插入的商品
        cursor.execute("SELECT * FROM products WHERE name = %s", (test_product,))
        new_product = cursor.fetchone()
        print(f"插入的商品信息: {new_product}")
        
    except Exception as e:
        print(f"❌ 数据库操作错误: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        connection.close()
else:
    print("❌ 无法获取数据库连接")

print("\n测试完成")
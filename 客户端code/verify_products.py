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
        # 查询前20个商品名称
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM products LIMIT 20")
        products = cursor.fetchall()
        
        print("\n前20个商品名称:")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product[0]}")
        
        # 查询商品总数
        cursor.execute("SELECT COUNT(*) as count FROM products")
        total_count = cursor.fetchone()[0]
        print(f"\n商品总数: {total_count}")
        
    except Exception as e:
        print(f"❌ 数据库操作错误: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        connection.close()
else:
    print("❌ 无法获取数据库连接")

print("\n验证完成")
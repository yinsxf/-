import os
import sys
import random

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
        cursor = connection.cursor()
        
        print("开始更新现有商品名称格式...")
        
        # 获取所有商品ID
        cursor.execute("SELECT product_id FROM products")
        product_ids = cursor.fetchall()
        
        # 定义品牌和类别列表
        brands = ['Apple', 'Samsung', 'Sony', 'Xiaomi', 'Huawei', 'Lenovo', 'HP', 'Dell', 'Acer', 'Asus', 'Bose', 'Canon', 'Nikon', 'TP-Link', 'Vivo', 'OPPO', 'OnePlus', 'Logitech', 'JBL']
        categories = ['手机', '笔记本电脑', '平板电脑', '智能穿戴', '音频设备', '存储设备', '网络设备', '办公设备', '游戏设备', '摄影设备']
        
        total_count = len(product_ids)
        updated_count = 0
        
        for i, (product_id,) in enumerate(product_ids, 1):
            try:
                # 生成新的商品名称 - 品牌 类别 数字格式
                category = random.choice(categories)
                brand = random.choice(brands)
                
                # 70%的概率添加一个随机数字型号
                if random.random() > 0.3:  # 70%的概率有型号
                    model_num = random.randint(100, 999)
                    new_name = f"{brand} {category} {model_num}"
                else:
                    new_name = f"{brand} {category}"
                
                # 更新商品名称
                cursor.execute("UPDATE products SET name = %s WHERE product_id = %s", (new_name, product_id))
                connection.commit()
                updated_count += 1
                
                # 打印进度
                if i % 100 == 0 or i == total_count:
                    print(f"已更新{i}/{total_count}个商品")
                
            except Exception as e:
                print(f"更新商品ID {product_id}失败: {str(e)}")
                # 继续处理下一个商品
                continue
        
        print(f"✅ 成功更新了{updated_count}/{total_count}个商品的名称")
        
    except Exception as e:
        print(f"❌ 数据库操作错误: {str(e)}")
        # 尝试回滚
        try:
            connection.rollback()
        except:
            pass
    finally:
        if cursor:
            cursor.close()
        connection.close()
else:
    print("❌ 无法获取数据库连接")

print("\n操作完成")
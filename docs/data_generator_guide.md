# 批量数据生成工具使用说明

这个工具可以帮助您快速生成大量的测试数据并插入到电子商务系统的数据库中。

## 工具组成

1. **bulk_data_generator.py**: 核心数据生成器类，负责生成客户、商品和订单数据
2. **generate_test_data.py**: 方便用户运行的入口脚本

## 使用方法

### 基本使用

1. 确保您已经安装了项目依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 确保数据库连接配置正确（在`config/database.ini`文件中）

3. 运行数据生成脚本：
   ```bash
   python generate_test_data.py
   ```

4. 按照提示输入要生成的数据量，默认情况下会生成1000条客户、1000条商品和1000条订单数据

### 直接使用生成器类

您也可以在自己的代码中直接使用`BulkDataGenerator`类：

```python
from src.utils.bulk_data_generator import BulkDataGenerator

# 创建生成器实例
generator = BulkDataGenerator()

# 生成指定数量的数据
result = generator.generate_all_data(
    customers_count=1000,  # 生成1000个客户
    products_count=1000,   # 生成1000个商品
    orders_count=1000      # 生成1000个订单
)

# 查看结果
print(f"生成了{result['customers']}个客户")
print(f"生成了{result['products']}个商品")
print(f"生成了{result['orders']}个订单")
```

## 生成的数据说明

### 客户数据
- 生成随机的中文姓名
- 生成唯一的邮箱地址
- 所有数据都符合`Customer`模型类的接口要求

### 商品数据
- 生成包含品牌、类别和型号的商品名称
- 生成随机的价格（99.99-9999.99元）
- 生成随机的库存数量（10-200个）
- 所有数据都符合`Product`模型类的接口要求

### 订单数据
- 随机选择现有客户
- 随机选择1-5个商品作为订单项
- 确保订单项的数量不超过商品库存
- 所有数据都符合`Order`模型类的接口要求

## 注意事项

1. 生成大量数据可能需要一定的时间，请耐心等待
2. 生成过程中会显示进度信息和统计数据
3. 如果数据库连接失败，工具会显示错误信息
4. 订单数据依赖于客户和商品数据，请确保先有足够的客户和商品数据
5. 工具会自动处理邮箱唯一性检查

## 扩展方法

如果您需要自定义生成的数据，可以修改`bulk_data_generator.py`文件中的以下内容：
- `product_categories`: 商品类别列表
- `product_brands`: 商品品牌列表
- 各种生成随机数据的方法

## 常见问题

**Q: 为什么生成的订单数量少于请求的数量？**
A: 可能是因为某些订单在创建过程中失败，比如库存不足或数据库错误。工具会忽略这些失败的订单并继续生成。

**Q: 如何调整生成数据的速度？**
A: 可以减少每次生成的数据量，或者优化数据库连接配置。
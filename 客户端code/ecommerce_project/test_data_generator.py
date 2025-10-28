# -*- coding: utf-8 -*-
"""
简单的测试脚本，用于验证数据生成器的导入和基本功能
"""

from src.utils.bulk_data_generator import BulkDataGenerator

if __name__ == "__main__":
    try:
        # 尝试导入并实例化生成器
        generator = BulkDataGenerator()
        print("✅ 数据生成器导入成功")
        
        # 验证客户生成方法存在
        if hasattr(generator, 'generate_customers'):
            print("✅ generate_customers方法存在")
            # 尝试生成少量客户数据进行测试
            print("开始生成少量测试数据...")
            count = generator.generate_customers(3)  # 只生成3个客户进行测试
            print(f"✅ 成功生成{count}个测试客户")
        else:
            print("❌ generate_customers方法不存在")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
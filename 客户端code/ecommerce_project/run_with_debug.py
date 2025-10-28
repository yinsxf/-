import sys
import traceback
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # 导入并运行主程序
    from src.main import main
    print("开始运行主程序...")
    main()
except Exception as e:
    print(f"程序运行出错: {type(e).__name__}: {str(e)}")
    print("\n详细错误栈:")
    traceback.print_exc()
    sys.exit(1)
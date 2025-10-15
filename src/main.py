import tkinter as tk
from tkinter import messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.gui.main_window import MainWindow

def main():
    """程序主入口"""
    # 设置中文字体支持
    if sys.platform == 'win32':
        # Windows系统设置
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    # 创建主窗口
    root = tk.Tk()
    
    # 捕获异常
    def handle_exception(exc_type, exc_value, exc_traceback):
        """处理未捕获的异常"""
        error_message = f"{exc_type.__name__}: {exc_value}\n\n请联系系统管理员"
        messagebox.showerror("程序错误", error_message)
    
    # 设置全局异常处理器
    sys.excepthook = handle_exception
    
    # 创建应用程序
    app = MainWindow(root)
    
    # 启动主循环
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("程序被用户中断")
    except Exception as e:
        messagebox.showerror("程序崩溃", f"程序遇到未预期的错误:\n{str(e)}")

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.gui.customer_tab import CustomerTab
from src.gui.product_tab import ProductTab
from src.gui.order_tab import OrderTab

class MainWindow:
    """应用程序主窗口类"""
    
    def __init__(self, root):
        """初始化主窗口"""
        self.root = root
        self.root.title("电子商务管理系统")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # 设置中文字体
        self.style = ttk.Style()
        self.style.configure(
            "TLabel", 
            font=("SimHei", 10)
        )
        self.style.configure(
            "TButton", 
            font=("SimHei", 10)
        )
        self.style.configure(
            "TNotebook.Tab", 
            font=("SimHei", 10)
        )
        
        # 创建标签页控件
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建各个功能标签页
        self.create_tabs()
        
        # 添加菜单栏
        self.create_menu()
        
        # 添加状态栏
        self.create_status_bar()
    
    def create_tabs(self):
        """创建各个功能标签页"""
        # 创建标签页容器
        self.customer_frame = ttk.Frame(self.notebook)
        self.product_frame = ttk.Frame(self.notebook)
        self.order_frame = ttk.Frame(self.notebook)
        
        # 添加标签页到笔记本控件
        self.notebook.add(self.customer_frame, text="客户管理")
        self.notebook.add(self.product_frame, text="商品管理")
        self.notebook.add(self.order_frame, text="订单管理")
        
        # 初始化各个标签页内容
        self.customer_tab = CustomerTab(self.customer_frame)
        self.product_tab = ProductTab(self.product_frame)
        self.order_tab = OrderTab(self.order_frame)
    
    def create_menu(self):
        """创建菜单栏"""
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        
        # 创建文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="退出", command=self.exit_app)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 创建数据菜单
        data_menu = tk.Menu(menubar, tearoff=0)
        data_menu.add_command(label="刷新客户数据", command=self.refresh_customer_data)
        data_menu.add_command(label="刷新商品数据", command=self.refresh_product_data)
        data_menu.add_command(label="刷新订单数据", command=self.refresh_order_data)
        menubar.add_cascade(label="数据", menu=data_menu)
        
        # 创建帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        # 配置主窗口的菜单栏
        self.root.config(menu=menubar)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        """更新状态栏消息"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def refresh_customer_data(self):
        """刷新客户数据"""
        self.update_status("正在刷新客户数据...")
        self.customer_tab.refresh_data()
        self.update_status("客户数据刷新完成")
    
    def refresh_product_data(self):
        """刷新商品数据"""
        self.update_status("正在刷新商品数据...")
        self.product_tab.refresh_data()
        self.update_status("商品数据刷新完成")
    
    def refresh_order_data(self):
        """刷新订单数据"""
        self.update_status("正在刷新订单数据...")
        self.order_tab.refresh_data()
        self.update_status("订单数据刷新完成")
    
    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo(
            "关于电子商务管理系统",
            "电子商务管理系统\n版本: 1.0\n\n功能特点:\n- 客户信息管理\n- 商品库存管理\n- 订单处理\n\n© 2023 电子商务管理系统"
        )
    
    def exit_app(self):
        """退出应用程序"""
        if messagebox.askyesno("确认退出", "确定要退出电子商务管理系统吗？"):
            self.root.destroy()

# 应用程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.order import Order
from src.models.customer import Customer
from src.models.product import Product

class OrderTab:
    """订单管理标签页"""
    
    def __init__(self, parent):
        """初始化订单管理标签页"""
        self.parent = parent
        self.order_model = Order()
        self.customer_model = Customer()
        self.product_model = Product()
        self.current_order_id = None
        
        # 创建界面布局
        self.create_widgets()
        
        # 加载订单数据
        self.refresh_data()
    
    def create_widgets(self):
        """创建界面控件"""
        # 创建顶部搜索和操作区域
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 搜索框
        ttk.Label(top_frame, text="搜索: ").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(top_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="搜索", command=self.search_orders).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="显示全部", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        
        # 状态筛选
        ttk.Label(top_frame, text="订单状态: ").pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(
            top_frame, 
            textvariable=self.status_var,
            values=["全部", "pending", "completed", "shipping", "cancelled"],
            width=10
        )
        self.status_combobox.current(0)
        self.status_combobox.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="筛选", command=self.filter_orders_by_status).pack(side=tk.LEFT, padx=5)
        
        # 刷新和创建订单按钮
        ttk.Button(top_frame, text="创建订单", command=self.create_order).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="刷新", command=self.refresh_data).pack(side=tk.RIGHT, padx=5)
        
        # 创建订单统计区域
        stats_frame = ttk.LabelFrame(self.parent, text="订单统计")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 统计标签
        self.total_orders_label = ttk.Label(stats_frame, text="订单总数: 0")
        self.total_orders_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # 创建订单表格
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview表格
        self.order_tree = ttk.Treeview(
            table_frame, 
            columns=("id", "customer_id", "order_date", "total_amount", "status", "payment_status"),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # 设置列标题
        self.order_tree.heading("id", text="订单ID")
        self.order_tree.heading("customer_id", text="客户ID")
        self.order_tree.heading("order_date", text="订单日期")
        self.order_tree.heading("total_amount", text="总金额")
        self.order_tree.heading("status", text="订单状态")
        self.order_tree.heading("payment_status", text="支付状态")
        
        # 设置列宽
        self.order_tree.column("id", width=100)
        self.order_tree.column("customer_id", width=100)
        self.order_tree.column("order_date", width=150)
        self.order_tree.column("total_amount", width=100)
        self.order_tree.column("status", width=100)
        self.order_tree.column("payment_status", width=100)
        
        # 隐藏第一列
        self.order_tree.column("#0", width=0, stretch=tk.NO)
        
        # 绑定滚动条
        scrollbar_y.config(command=self.order_tree.yview)
        scrollbar_x.config(command=self.order_tree.xview)
        
        # 绑定选中事件
        self.order_tree.bind("<<TreeviewSelect>>", self.on_order_select)
        
        # 包装表格
        self.order_tree.pack(fill=tk.BOTH, expand=True)
        
        # 创建底部操作按钮
        bottom_frame = ttk.Frame(self.parent)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(bottom_frame, text="查看订单详情", command=self.view_order_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="更新订单状态", command=self.update_order_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="取消订单", command=self.cancel_order).pack(side=tk.LEFT, padx=5)
    
    def refresh_data(self):
        """刷新订单数据"""
        # 清空表格
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # 加载所有订单数据
        orders = self.order_model.get_all_orders()
        
        if orders:
            for order in orders:
                # 格式化日期
                order_date = order['order_date'].strftime("%Y-%m-%d %H:%M:%S") if order['order_date'] else "-"
                
                # 安全获取订单状态和支付状态
                status = order.get('status', 'unknown')
                payment_status = order.get('payment_status', 'unknown')
                
                self.order_tree.insert("", tk.END, values=(
                    order['order_id'],
                    order['customer_id'],
                    order_date,
                    f"¥{order['total_amount']:.2f}",
                    status,
                    payment_status
                ))
        
        # 更新订单总数
        total_orders = self.order_model.count_orders()
        self.total_orders_label.config(text=f"订单总数: {total_orders}")
        
        # 重置当前选择
        self.current_order_id = None
    
    def search_orders(self):
        """搜索订单"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("提示", "请输入搜索关键词")
            return
        
        # 清空表格
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # 搜索订单
        orders = self.order_model.search_orders(keyword)
        
        if orders:
            for order in orders:
                # 格式化日期
                order_date = order['order_date'].strftime("%Y-%m-%d %H:%M:%S") if order['order_date'] else "-"
                
                # 安全获取订单状态和支付状态
                status = order.get('status', 'unknown')
                payment_status = order.get('payment_status', 'unknown')
                
                self.order_tree.insert("", tk.END, values=(
                    order['order_id'],
                    order['customer_id'],
                    order_date,
                    f"¥{order['total_amount']:.2f}",
                    status,
                    payment_status
                ))
        else:
            messagebox.showinfo("提示", f"没有找到包含 '{keyword}' 的订单")
        
        # 重置当前选择
        self.current_order_id = None
    
    def filter_orders_by_status(self):
        """按状态筛选订单"""
        status = self.status_var.get()
        
        if status == "全部":
            self.refresh_data()
            return
        
        # 清空表格
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # 按状态筛选订单
        orders = self.order_model.get_orders_by_status(status)
        
        if orders:
            for order in orders:
                # 格式化日期
                order_date = order['order_date'].strftime("%Y-%m-%d %H:%M:%S") if order['order_date'] else "-"
                
                # 安全获取订单状态和支付状态
                status_value = order.get('status', 'unknown')
                payment_status = order.get('payment_status', 'unknown')
                
                self.order_tree.insert("", tk.END, values=(
                    order['order_id'],
                    order['customer_id'],
                    order_date,
                    f"¥{order['total_amount']:.2f}",
                    status_value,
                    payment_status
                ))
        else:
            messagebox.showinfo("提示", f"没有找到状态为 '{status}' 的订单")
        
        # 重置当前选择
        self.current_order_id = None
    
    def on_order_select(self, event):
        """处理订单选择事件"""
        selected_items = self.order_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            order_data = self.order_tree.item(selected_item, "values")
            self.current_order_id = int(order_data[0])
        else:
            self.current_order_id = None
    
    def view_order_details(self):
        """查看订单详情"""
        if not self.current_order_id:
            messagebox.showinfo("提示", "请先选择一个订单")
            return
        
        # 获取订单详情
        order_summary = self.order_model.get_order_summary(self.current_order_id)
        if not order_summary:
            messagebox.showerror("错误", "无法获取订单详情")
            return
        
        order = order_summary['order']
        items = order_summary['items']
        
        # 获取客户信息
        customer = self.customer_model.get_customer_by_id(order['customer_id'])
        
        # 创建订单详情对话框
        detail_window = tk.Toplevel(self.parent)
        detail_window.title(f"订单详情 - ID: {order['order_id']}")
        detail_window.geometry("700x500")
        detail_window.resizable(True, True)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        
        # 创建订单基本信息区域
        order_info_frame = ttk.LabelFrame(detail_window, text="订单基本信息")
        order_info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 订单信息网格
        info_grid = ttk.Frame(order_info_frame)
        info_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # 订单ID
        ttk.Label(info_grid, text="订单ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(info_grid, text=order['order_id']).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 客户信息
        ttk.Label(info_grid, text="客户信息:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        customer_info = f"{customer.get('name', '未知客户')} (ID: {order['customer_id']})" if customer else f"ID: {order['customer_id']}"
        ttk.Label(info_grid, text=customer_info).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # 订单日期
        ttk.Label(info_grid, text="订单日期:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        order_date = order['order_date'].strftime("%Y-%m-%d %H:%M:%S") if order['order_date'] else "-"
        ttk.Label(info_grid, text=order_date).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 订单状态
        ttk.Label(info_grid, text="订单状态:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        status = order.get('status', 'unknown')
        ttk.Label(info_grid, text=status).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # 支付状态
        ttk.Label(info_grid, text="支付状态:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        payment_status = order.get('payment_status', 'unknown')
        ttk.Label(info_grid, text=payment_status).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 订单总金额
        ttk.Label(info_grid, text="总金额:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(info_grid, text=f"¥{order['total_amount']:.2f}").grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)
        
        # 创建订单项表格区域
        items_frame = ttk.LabelFrame(detail_window, text="订单项")
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(items_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(items_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建订单项表格
        items_tree = ttk.Treeview(
            items_frame,
            columns=("product_id", "product_name", "quantity", "unit_price", "subtotal"),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # 设置列标题
        items_tree.heading("product_id", text="商品ID")
        items_tree.heading("product_name", text="商品名称")
        items_tree.heading("quantity", text="数量")
        items_tree.heading("unit_price", text="单价")
        items_tree.heading("subtotal", text="小计")
        
        # 设置列宽
        items_tree.column("product_id", width=80)
        items_tree.column("product_name", width=200)
        items_tree.column("quantity", width=80)
        items_tree.column("unit_price", width=100)
        items_tree.column("subtotal", width=100)
        
        # 隐藏第一列
        items_tree.column("#0", width=0, stretch=tk.NO)
        
        # 绑定滚动条
        scrollbar_y.config(command=items_tree.yview)
        scrollbar_x.config(command=items_tree.xview)
        
        # 包装表格
        items_tree.pack(fill=tk.BOTH, expand=True)
        
        # 填充订单项数据
        if items:
            for item in items:
                # 尝试获取商品名称，如果没有则使用商品ID
                product_name = item.get('product_name', f'商品ID {item.get('product_id', '未知')}')
                
                items_tree.insert("", tk.END, values=(
                    item.get('product_id', '未知'),
                    product_name,
                    item.get('quantity', 0),
                    f"¥{item.get('unit_price', 0):.2f}",
                    f"¥{item.get('quantity', 0) * item.get('unit_price', 0):.2f}"
                ))
        
        # 关闭按钮
        ttk.Button(detail_window, text="关闭", command=detail_window.destroy).pack(pady=10)
        
        # 使对话框模态
        detail_window.grab_set()
        self.parent.wait_window(detail_window)
    
    def update_order_status(self):
        """更新订单状态"""
        if not self.current_order_id:
            messagebox.showinfo("提示", "请先选择一个订单")
            return
        
        # 获取当前订单
        order = self.order_model.get_order_by_id(self.current_order_id)
        if not order:
            messagebox.showerror("错误", "订单不存在")
            return
        
        # 创建更新状态对话框
        update_window = tk.Toplevel(self.parent)
        update_window.title(f"更新订单状态 - ID: {order['order_id']}")
        update_window.geometry("400x200")
        update_window.resizable(False, False)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        
        # 安全获取当前状态
        current_status = order.get('status', 'unknown')
        current_payment_status = order.get('payment_status', 'unknown')
        
        # 当前状态显示
        ttk.Label(update_window, text=f"当前状态: {current_status}").pack(pady=10)
        
        # 新状态选择
        ttk.Label(update_window, text="新状态:").pack(pady=5)
        status_var = tk.StringVar(value=current_status)
        
        # 状态选项，根据当前状态过滤不可用的选项
        available_statuses = []
        if current_status == 'pending':
            available_statuses = ['pending', 'shipping', 'completed', 'cancelled']
        elif current_status == 'shipping':
            available_statuses = ['shipping', 'completed', 'cancelled']
        elif current_status == 'completed':
            available_statuses = ['completed']  # 已完成订单不能再修改状态
        elif current_status == 'cancelled':
            available_statuses = ['cancelled']  # 已取消订单不能再修改状态
        else:
            available_statuses = ['pending', 'shipping', 'completed', 'cancelled']  # 未知状态时显示所有选项
        
        status_combobox = ttk.Combobox(
            update_window,
            textvariable=status_var,
            values=available_statuses,
            state="readonly",
            width=20
        )
        status_combobox.pack(pady=10)
        
        # 确认按钮
        def confirm_update():
            new_status = status_var.get()
            if new_status == current_status:
                messagebox.showinfo("提示", "订单状态未改变")
                update_window.destroy()
                return
            
            # 更新订单状态
            if self.order_model.update_order_status(self.current_order_id, new_status):
                # 如果订单完成，更新支付状态为已支付
                if new_status == 'completed' and current_payment_status != 'paid':
                    self.order_model.update_payment_status(self.current_order_id, 'paid')
                
                messagebox.showinfo("成功", f"订单状态已更新为: {new_status}")
                self.refresh_data()
                update_window.destroy()
            else:
                messagebox.showerror("错误", "更新订单状态失败")
        
        # 按钮区域
        button_frame = ttk.Frame(update_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="确认", command=confirm_update).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=update_window.destroy).pack(side=tk.LEFT, padx=10)
        
        # 使对话框模态
        update_window.grab_set()
        self.parent.wait_window(update_window)
    
    def cancel_order(self):
        """取消订单"""
        if not self.current_order_id:
            messagebox.showinfo("提示", "请先选择一个订单")
            return
        
        # 获取当前订单
        order = self.order_model.get_order_by_id(self.current_order_id)
        if not order:
            messagebox.showerror("错误", "订单不存在")
            return
        
        # 安全获取当前状态
        current_status = order.get('status', 'unknown')
        
        # 检查订单状态是否可以取消
        if current_status == 'completed':
            messagebox.showinfo("提示", "已完成的订单无法取消")
            return
        
        if current_status == 'cancelled':
            messagebox.showinfo("提示", "订单已经被取消")
            return
        
        if messagebox.askyesno("确认取消", "确定要取消选中的订单吗？取消后库存将被恢复。"):
            if self.order_model.cancel_order(self.current_order_id):
                messagebox.showinfo("成功", "订单已成功取消")
                self.refresh_data()
            else:
                messagebox.showerror("错误", "取消订单失败")
    
    def create_order(self):
        """创建新订单"""
        # 创建订单对话框
        create_window = tk.Toplevel(self.parent)
        create_window.title("创建新订单")
        create_window.geometry("800x600")
        create_window.resizable(True, True)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        
        # 创建客户选择区域
        customer_frame = ttk.LabelFrame(create_window, text="客户信息")
        customer_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 客户ID输入
        ttk.Label(customer_frame, text="客户ID:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        customer_id_var = tk.StringVar()
        ttk.Entry(customer_frame, textvariable=customer_id_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 客户信息显示
        customer_info_var = tk.StringVar(value="未选择客户")
        ttk.Label(customer_frame, textvariable=customer_info_var).grid(row=0, column=2, sticky=tk.W, padx=10, pady=10)
        
        # 验证客户按钮
        def validate_customer():
            try:
                customer_id = int(customer_id_var.get().strip())
                customer = self.customer_model.get_customer_by_id(customer_id)
                if customer:
                    customer_info_var.set(f"{customer['name']} ({customer['email']})")
                    messagebox.showinfo("成功", "客户信息验证成功")
                else:
                    messagebox.showerror("错误", "未找到该客户")
                    customer_info_var.set("未选择客户")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的客户ID")
                customer_info_var.set("未选择客户")
        
        ttk.Button(customer_frame, text="验证客户", command=validate_customer).grid(row=0, column=3, padx=10, pady=10)
        
        # 创建订单项区域
        items_frame = ttk.LabelFrame(create_window, text="订单项")
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 订单项选择和添加
        add_item_frame = ttk.Frame(items_frame)
        add_item_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(add_item_frame, text="商品ID:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        product_id_var = tk.StringVar()
        ttk.Entry(add_item_frame, textvariable=product_id_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        ttk.Label(add_item_frame, text="数量:").grid(row=0, column=2, sticky=tk.W, padx=10, pady=10)
        quantity_var = tk.StringVar(value="1")
        ttk.Entry(add_item_frame, textvariable=quantity_var, width=5).grid(row=0, column=3, sticky=tk.W, padx=10, pady=10)
        
        # 商品信息显示
        product_info_var = tk.StringVar(value="")
        ttk.Label(add_item_frame, textvariable=product_info_var).grid(row=0, column=4, sticky=tk.W, padx=10, pady=10)
        
        # 验证商品按钮
        current_product = None
        
        def validate_product():
            nonlocal current_product
            try:
                product_id = int(product_id_var.get().strip())
                current_product = self.product_model.get_product_by_id(product_id)
                if current_product:
                    product_name = current_product.get('product_name', f'商品ID {product_id}')
                    price = current_product.get('price', 0)
                    stock = current_product.get('stock_quantity', 0)
                    product_info_var.set(f"{product_name} - ¥{price:.2f} (库存: {stock})")
                else:
                    messagebox.showerror("错误", "未找到该商品")
                    product_info_var.set("")
                    current_product = None
            except ValueError:
                messagebox.showerror("错误", "请输入有效的商品ID")
                product_info_var.set("")
                current_product = None
        
        ttk.Button(add_item_frame, text="验证商品", command=validate_product).grid(row=0, column=5, padx=10, pady=10)
        
        # 创建订单项表格
        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(items_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(items_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建订单项表格
        order_items_tree = ttk.Treeview(
            items_frame,
            columns=("product_id", "product_name", "quantity", "unit_price", "subtotal"),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # 设置列标题
        order_items_tree.heading("product_id", text="商品ID")
        order_items_tree.heading("product_name", text="商品名称")
        order_items_tree.heading("quantity", text="数量")
        order_items_tree.heading("unit_price", text="单价")
        order_items_tree.heading("subtotal", text="小计")
        
        # 设置列宽
        order_items_tree.column("product_id", width=80)
        order_items_tree.column("product_name", width=200)
        order_items_tree.column("quantity", width=80)
        order_items_tree.column("unit_price", width=100)
        order_items_tree.column("subtotal", width=100)
        
        # 隐藏第一列
        order_items_tree.column("#0", width=0, stretch=tk.NO)
        
        # 绑定滚动条
        scrollbar_y.config(command=order_items_tree.yview)
        scrollbar_x.config(command=order_items_tree.xview)
        
        # 包装表格
        order_items_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 订单总金额
        total_amount_var = tk.StringVar(value="¥0.00")
        total_frame = ttk.Frame(items_frame)
        total_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
        
        ttk.Label(total_frame, text="订单总金额: ", font=("SimHei", 12, "bold")).pack(side=tk.RIGHT, padx=20)
        ttk.Label(total_frame, textvariable=total_amount_var, font=("SimHei", 12, "bold")).pack(side=tk.RIGHT, padx=5)
        
        # 添加订单项
        order_items = []
        
        def add_order_item():
            nonlocal current_product
            if not current_product:
                messagebox.showinfo("提示", "请先输入并验证商品ID")
                return
            
            try:
                quantity = int(quantity_var.get().strip())
                if quantity <= 0:
                    messagebox.showerror("错误", "数量必须大于0")
                    return
                
                # 检查库存
                product_id = current_product.get('product_id', 0)
                product_name = current_product.get('product_name', f'商品ID {product_id}')
                price = current_product.get('price', 0)
                stock = current_product.get('stock_quantity', 0)
                
                if quantity > stock:
                    messagebox.showerror("错误", f"库存不足，当前库存: {stock}")
                    return
                
                # 计算小计
                subtotal = quantity * price
                
                # 添加到订单项列表
                order_items.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'quantity': quantity,
                    'unit_price': price,
                    'subtotal': subtotal
                })
                
                # 更新表格
                order_items_tree.insert("", tk.END, values=(
                    product_id,
                    product_name,
                    quantity,
                    f"¥{price:.2f}",
                    f"¥{subtotal:.2f}"
                ))
                
                # 更新总金额
                total_amount = sum(item['subtotal'] for item in order_items)
                total_amount_var.set(f"¥{total_amount:.2f}")
                
                # 清空输入
                product_id_var.set("")
                quantity_var.set("1")
                product_info_var.set("")
                current_product = None
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数量")
        
        ttk.Button(add_item_frame, text="添加商品", command=add_order_item).grid(row=0, column=6, padx=10, pady=10)
        
        # 移除订单项
        def remove_order_item():
            selected_items = order_items_tree.selection()
            if not selected_items:
                messagebox.showinfo("提示", "请选择要移除的订单项")
                return
            
            # 获取选中项的索引
            selected_idx = order_items_tree.index(selected_items[0])
            
            # 从列表和表格中移除
            order_items.pop(selected_idx)
            order_items_tree.delete(selected_items[0])
            
            # 更新总金额
            total_amount = sum(item['subtotal'] for item in order_items)
            total_amount_var.set(f"¥{total_amount:.2f}")
        
        ttk.Button(add_item_frame, text="移除商品", command=remove_order_item).grid(row=0, column=7, padx=10, pady=10)
        
        # 保存订单
        def save_order():
            # 验证客户ID
            if not customer_id_var.get().strip():
                messagebox.showerror("错误", "请输入客户ID")
                return
            
            try:
                customer_id = int(customer_id_var.get().strip())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的客户ID")
                return
            
            # 验证客户是否存在
            customer = self.customer_model.get_customer_by_id(customer_id)
            if not customer:
                messagebox.showerror("错误", "客户不存在")
                return
            
            # 验证订单项
            if not order_items:
                messagebox.showerror("错误", "请至少添加一个订单项")
                return
            
            # 准备订单数据
            order_data = {
                'customer_id': customer_id,
                'status': 'pending',
                'payment_status': 'unpaid',
                'total_amount': sum(item['subtotal'] for item in order_items),
                'items': [
                    {
                        'product_id': item['product_id'],
                        'quantity': item['quantity'],
                        'unit_price': item['unit_price']
                    } for item in order_items
                ]
            }
            
            # 创建订单
            try:
                order_id = self.order_model.create_order(order_data)
                if order_id:
                    messagebox.showinfo("成功", f"订单创建成功！订单ID: {order_id}")
                    self.refresh_data()
                    create_window.destroy()
                else:
                    messagebox.showerror("错误", "订单创建失败")
            except Exception as e:
                messagebox.showerror("错误", f"订单创建失败: {str(e)}")
        
        # 按钮区域
        button_frame = ttk.Frame(create_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="创建订单", command=save_order).pack(side=tk.RIGHT, padx=10)
        ttk.Button(button_frame, text="取消", command=create_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        create_window.grab_set()
        self.parent.wait_window(create_window)
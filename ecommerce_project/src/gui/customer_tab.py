import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import re

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.customer import Customer
from src.models.order import Order

class CustomerTab:
    """客户管理标签页"""
    
    def __init__(self, parent):
        """初始化客户管理标签页"""
        self.parent = parent
        self.customer_model = Customer()
        self.order_model = Order()
        self.current_customer_id = None
        
        # 创建界面布局
        self.create_widgets()
        
        # 加载客户数据
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
        ttk.Button(top_frame, text="搜索", command=self.search_customers).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="显示全部", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        
        # 添加客户按钮
        ttk.Button(top_frame, text="添加客户", command=self.add_customer).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="刷新", command=self.refresh_data).pack(side=tk.RIGHT, padx=5)
        
        # 创建客户统计区域
        self.stats_frame = ttk.LabelFrame(self.parent, text="客户订单统计")
        self.stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 统计标签
        self.order_count_label = ttk.Label(self.stats_frame, text="订单总数: 0")
        self.order_count_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.total_spent_label = ttk.Label(self.stats_frame, text="总消费金额: ¥0.00")
        self.total_spent_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # 创建客户表格
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview表格 - 更新列定义以匹配实际数据库结构
        self.customer_tree = ttk.Treeview(
            table_frame, 
            columns=("id", "name", "gender", "phone", "email"),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # 设置列标题
        self.customer_tree.heading("id", text="客户ID")
        self.customer_tree.heading("name", text="客户名称")
        self.customer_tree.heading("gender", text="性别")
        self.customer_tree.heading("phone", text="手机号")
        self.customer_tree.heading("email", text="邮箱")
        
        # 设置列宽
        self.customer_tree.column("id", width=80)
        self.customer_tree.column("name", width=150)
        self.customer_tree.column("gender", width=80)
        self.customer_tree.column("phone", width=150)
        self.customer_tree.column("email", width=200)
        
        # 隐藏第一列
        self.customer_tree.column("#0", width=0, stretch=tk.NO)
        
        # 绑定滚动条
        scrollbar_y.config(command=self.customer_tree.yview)
        scrollbar_x.config(command=self.customer_tree.xview)
        
        # 绑定选中事件
        self.customer_tree.bind("<<TreeviewSelect>>", self.on_customer_select)
        
        # 包装表格
        self.customer_tree.pack(fill=tk.BOTH, expand=True)
        
        # 创建底部操作按钮
        bottom_frame = ttk.Frame(self.parent)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(bottom_frame, text="查看详情", command=self.view_customer_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="编辑客户", command=self.edit_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="删除客户", command=self.delete_customer).pack(side=tk.LEFT, padx=5)
    
    def refresh_data(self):
        """刷新客户数据，适应实际的数据库表结构"""
        # 清空表格
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # 加载所有客户数据
        customers = self.customer_model.get_all_customers()
        
        if customers:
            for customer in customers:
                # 使用get方法安全访问字段，提供默认值
                # 直接使用name字段
                name = customer.get('name', '')
                
                self.customer_tree.insert("", tk.END, values=(
                    customer.get('customer_id', ''),
                    name,
                    customer.get('gender', ''),
                    customer.get('phone', ''),
                    customer.get('email', '')
                ))
        
        # 清空统计信息
        self.update_order_statistics(None)
    
    def search_customers(self):
        """搜索客户，适应实际的数据库表结构"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("提示", "请输入搜索关键词")
            return
        
        # 清空表格
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # 搜索客户
        customers = self.customer_model.search_customers(keyword)
        
        if customers:
            for customer in customers:
                # 使用get方法安全访问字段，提供默认值
                # 直接使用name字段
                name = customer.get('name', '')
                
                self.customer_tree.insert("", tk.END, values=(
                    customer.get('customer_id', ''),
                    name,
                    customer.get('gender', ''),
                    customer.get('phone', ''),
                    customer.get('email', '')
                ))
        else:
            messagebox.showinfo("提示", f"没有找到包含 '{keyword}' 的客户")
        
        # 清空统计信息
        self.update_order_statistics(None)
    
    def on_customer_select(self, event):
        """处理客户选择事件"""
        selected_items = self.customer_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            customer_data = self.customer_tree.item(selected_item, "values")
            try:
                self.current_customer_id = int(customer_data[0])
                # 更新订单统计
                self.update_order_statistics(self.current_customer_id)
            except (IndexError, ValueError):
                self.current_customer_id = None
                self.update_order_statistics(None)
        else:
            self.current_customer_id = None
            self.update_order_statistics(None)
    
    def update_order_statistics(self, customer_id):
        """更新客户订单统计信息"""
        if customer_id:
            try:
                # 调用Order类的get_customer_order_statistics方法获取统计数据
                statistics = self.order_model.get_customer_order_statistics(customer_id)
                
                # 更新标签显示
                order_count = statistics.get('order_count', 0)
                total_spent = statistics.get('total_spent', 0.0)
                self.order_count_label.config(text=f"订单总数: {order_count}")
                self.total_spent_label.config(text=f"总消费金额: ¥{total_spent:.2f}")
            except Exception as e:
                print(f"更新统计信息出错: {str(e)}")
                self.order_count_label.config(text="订单总数: 0")
                self.total_spent_label.config(text="总消费金额: ¥0.00")
        else:
            # 清空统计信息
            self.order_count_label.config(text="订单总数: 0")
            self.total_spent_label.config(text="总消费金额: ¥0.00")
    
    def add_customer(self):
        """添加新客户，适应实际的数据库表结构"""
        # 创建添加客户对话框
        add_window = tk.Toplevel(self.parent)
        add_window.title("添加新客户")
        add_window.geometry("500x250")
        add_window.resizable(False, False)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        style.configure("TEntry", font=("SimHei", 10))
        
        # 创建内容框架
        content_frame = ttk.Frame(add_window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建客户信息表单
        form_frame = ttk.LabelFrame(content_frame, text="客户信息", padding=(10, 10))
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 客户名称
        ttk.Label(form_frame, text="客户名称: *", width=10).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar(value="")
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 客户邮箱
        ttk.Label(form_frame, text="邮箱: *", width=10).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        email_var = tk.StringVar(value="")
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 客户手机号
        ttk.Label(form_frame, text="手机号: ", width=10).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        phone_var = tk.StringVar()
        phone_entry = ttk.Entry(form_frame, textvariable=phone_var, width=30)
        phone_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 客户性别
        ttk.Label(form_frame, text="性别: ", width=10).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        gender_var = tk.StringVar(value="")
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 性别单选按钮
        ttk.Radiobutton(gender_frame, text="男", variable=gender_var, value="男").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="女", variable=gender_var, value="女").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="保密", variable=gender_var, value="保密").pack(side=tk.LEFT, padx=5)
        
        # 表单验证
        def validate_form():
            errors = []
            
            # 验证姓名
            name = name_var.get().strip()
            if not name:
                errors.append("客户名称不能为空")
            
            # 验证邮箱
            email = email_var.get().strip()
            if not email:
                errors.append("邮箱不能为空")
            elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$", email):
                errors.append("邮箱格式不正确")
            else:
                # 检查邮箱是否已存在
                if self.customer_model.check_email_exists(email):
                    errors.append("该邮箱已被使用")
            
            return errors
        
        # 保存新客户
        def save_customer():
            # 验证表单
            errors = validate_form()
            if errors:
                messagebox.showerror("验证错误", "\n".join(errors))
                return
            
            # 准备客户数据
            customer_data = {
                'name': name_var.get().strip(),
                'email': email_var.get().strip(),
                'phone': phone_var.get().strip(),
                'gender': gender_var.get() if gender_var.get() else None
            }
            
            # 添加客户
            new_customer_id = self.customer_model.add_customer(customer_data)
            if new_customer_id:
                messagebox.showinfo("成功", f"客户添加成功，客户ID: {new_customer_id}")
                self.refresh_data()
                add_window.destroy()
            else:
                messagebox.showerror("错误", "客户添加失败")
        
        # 底部按钮区域
        button_frame = ttk.Frame(add_window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 保存按钮
        ttk.Button(button_frame, text="添加", command=save_customer).pack(side=tk.RIGHT, padx=10)
        # 取消按钮
        ttk.Button(button_frame, text="取消", command=add_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        add_window.grab_set()
        self.parent.wait_window(add_window)
    
    def view_customer_details(self):
        """查看客户详情"""
        if not self.current_customer_id:
            messagebox.showinfo("提示", "请先选择一个客户")
            return
        
        # 获取客户详情
        customer = self.customer_model.get_customer_by_id(self.current_customer_id)
        if not customer:
            messagebox.showerror("错误", "无法获取客户信息")
            return
        
        # 创建详情对话框
        detail_window = tk.Toplevel(self.parent)
        detail_window.title(f"客户详情 - {customer['name']}")
        detail_window.geometry("500x400")
        detail_window.resizable(False, False)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        
        # 创建内容框架
        content_frame = ttk.Frame(detail_window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建客户信息标签
        info_frame = ttk.LabelFrame(content_frame, text="基本信息", padding=(10, 10))
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 显示客户ID
        ttk.Label(info_frame, text="客户ID: ", width=10).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_frame, text=customer['id']).grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 显示客户姓名
        ttk.Label(info_frame, text="姓名: ", width=10).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_frame, text=customer['name']).grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 显示客户邮箱
        ttk.Label(info_frame, text="邮箱: ", width=10).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_frame, text=customer['email']).grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 显示客户手机号
        ttk.Label(info_frame, text="手机号: ", width=10).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_frame, text=customer.get('phone', '')).grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 显示客户性别
        ttk.Label(info_frame, text="性别: ", width=10).grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_frame, text=customer.get('gender', '')).grid(row=4, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 订单信息区域
        order_frame = ttk.LabelFrame(content_frame, text="订单信息", padding=(10, 10))
        order_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 获取客户的订单数量
        order_count = self.order_model.get_customer_order_count(customer['id'])
        ttk.Label(order_frame, text=f"订单总数: {order_count}", font=("SimHei", 10, "bold")).pack(anchor=tk.W, padx=10, pady=10)
        
        # 底部按钮区域
        button_frame = ttk.Frame(detail_window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 关闭按钮
        ttk.Button(button_frame, text="关闭", command=detail_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        detail_window.grab_set()
        self.parent.wait_window(detail_window)
    
    def edit_customer(self):
        """编辑客户信息"""
        if not self.current_customer_id:
            messagebox.showinfo("提示", "请先选择一个客户")
            return
        
        # 获取客户详情
        customer = self.customer_model.get_customer_by_id(self.current_customer_id)
        if not customer:
            messagebox.showerror("错误", "无法获取客户信息")
            return
        
        # 创建编辑对话框
        edit_window = tk.Toplevel(self.parent)
        edit_window.title(f"编辑客户 - {customer['name']}")
        edit_window.geometry("500x250")
        edit_window.resizable(False, False)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        style.configure("TEntry", font=("SimHei", 10))
        
        # 创建内容框架
        content_frame = ttk.Frame(edit_window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建客户信息表单
        form_frame = ttk.LabelFrame(content_frame, text="编辑客户信息", padding=(10, 10))
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 客户姓名
        ttk.Label(form_frame, text="姓名: *", width=10).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar(value=customer['name'])
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 客户邮箱
        ttk.Label(form_frame, text="邮箱: *", width=10).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        email_var = tk.StringVar(value=customer['email'])
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 客户手机号
        ttk.Label(form_frame, text="手机号: ", width=10).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        phone_var = tk.StringVar(value=customer.get('phone', ''))
        phone_entry = ttk.Entry(form_frame, textvariable=phone_var, width=30)
        phone_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 客户性别
        ttk.Label(form_frame, text="性别: ", width=10).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        gender_var = tk.StringVar(value=customer.get('gender', ''))
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 性别单选按钮
        ttk.Radiobutton(gender_frame, text="男", variable=gender_var, value="男").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="女", variable=gender_var, value="女").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="保密", variable=gender_var, value="保密").pack(side=tk.LEFT, padx=5)
        
        # 表单验证
        def validate_form():
            errors = []
            
            # 验证姓名
            name = name_var.get().strip()
            if not name:
                errors.append("姓名不能为空")
            
            # 验证邮箱
            email = email_var.get().strip()
            if not email:
                errors.append("邮箱不能为空")
            elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$", email):
                errors.append("邮箱格式不正确")
            else:
                # 检查邮箱是否已存在（排除当前客户）
                if self.customer_model.check_email_exists(email, exclude_id=customer['id']):
                    errors.append("该邮箱已被使用")
            
            return errors
        
        # 保存客户信息
        def save_customer():
            # 验证表单
            errors = validate_form()
            if errors:
                messagebox.showerror("验证错误", "\n".join(errors))
                return
            
            # 准备更新数据
            update_data = {
                'name': name_var.get().strip(),
                'email': email_var.get().strip(),
                'phone': phone_var.get().strip(),
                'gender': gender_var.get() if gender_var.get() else None
            }
            
            # 更新客户信息
            if self.customer_model.update_customer(customer['id'], update_data):
                messagebox.showinfo("成功", "客户信息已更新")
                self.refresh_data()
                edit_window.destroy()
            else:
                messagebox.showerror("错误", "客户信息更新失败")
        
        # 底部按钮区域
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 保存按钮
        ttk.Button(button_frame, text="保存", command=save_customer).pack(side=tk.RIGHT, padx=10)
        # 取消按钮
        ttk.Button(button_frame, text="取消", command=edit_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        edit_window.grab_set()
        self.parent.wait_window(edit_window)
    
    def delete_customer(self):
        """删除客户"""
        if not self.current_customer_id:
            messagebox.showinfo("提示", "请先选择一个客户")
            return
        
        if messagebox.askyesno("确认删除", "确定要删除选中的客户吗？"):
            if self.customer_model.delete_customer(self.current_customer_id):
                messagebox.showinfo("成功", "客户已成功删除")
                self.refresh_data()
            else:
                messagebox.showerror("错误", "删除客户失败")
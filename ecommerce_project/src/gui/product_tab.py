import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.product import Product

class ProductTab:
    """商品管理标签页"""
    
    def __init__(self, parent):
        """初始化商品管理标签页"""
        self.parent = parent
        self.product_model = Product()
        self.current_product_id = None
        
        # 创建界面布局
        self.create_widgets()
        
        # 加载商品数据
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
        ttk.Button(top_frame, text="搜索", command=self.search_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="显示全部", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        
        # 添加商品按钮
        ttk.Button(top_frame, text="添加商品", command=self.add_product).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="刷新", command=self.refresh_data).pack(side=tk.RIGHT, padx=5)
        
        # 创建商品统计区域
        stats_frame = ttk.LabelFrame(self.parent, text="商品统计")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 统计标签
        self.total_products_label = ttk.Label(stats_frame, text="商品总数: 0")
        self.total_products_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # 创建商品表格
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview表格 - 调整列定义以匹配实际数据库结构
        self.product_tree = ttk.Treeview(
            table_frame, 
            columns=('id', 'name', 'price', 'stock'),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # 设置列标题
        self.product_tree.heading('id', text="商品ID")
        self.product_tree.heading('name', text="商品名称")
        self.product_tree.heading('price', text="价格")
        self.product_tree.heading('stock', text="库存")
        
        # 设置列宽
        self.product_tree.column('id', width=80)
        self.product_tree.column('name', width=350)
        self.product_tree.column('price', width=100)
        self.product_tree.column('stock', width=80)
        
        # 隐藏第一列
        self.product_tree.column('#0', width=0, stretch=tk.NO)
        
        # 绑定滚动条
        scrollbar_y.config(command=self.product_tree.yview)
        scrollbar_x.config(command=self.product_tree.xview)
        
        # 绑定选中事件
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # 包装表格
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # 创建底部操作按钮
        bottom_frame = ttk.Frame(self.parent)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(bottom_frame, text="查看详情", command=self.view_product_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="编辑商品", command=self.edit_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="删除商品", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="库存调整", command=self.adjust_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="查看库存日志", command=self.view_inventory_logs).pack(side=tk.LEFT, padx=5)
    
    def refresh_data(self):
        """刷新商品数据"""
        # 清空表格
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # 加载所有商品数据
        products = self.product_model.get_all_products()
        
        if products:
            for product in products:
                # 使用get方法安全访问字段，提供默认值
                self.product_tree.insert("", tk.END, values=(
                    product.get('product_id', ''),
                    product.get('name', ''),
                    f"¥{product.get('price', 0.0):.2f}",
                    product.get('stock_quantity', 0)
                ))
        
        # 更新商品总数
        try:
            total_products = self.product_model.count_products()
            self.total_products_label.config(text=f"商品总数: {total_products}")
        except Exception as e:
            print(f"更新商品总数出错: {str(e)}")
            self.total_products_label.config(text="商品总数: 0")
        
        # 重置当前选择
        self.current_product_id = None
    
    def search_products(self):
        """搜索商品"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("提示", "请输入搜索关键词")
            return
        
        # 清空表格
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        try:
            # 搜索商品
            products = self.product_model.search_products(keyword)
            
            if products:
                for product in products:
                    # 使用get方法安全访问字段，提供默认值
                    self.product_tree.insert("", tk.END, values=(
                        product.get('product_id', ''),
                        product.get('name', ''),
                        f"¥{product.get('price', 0.0):.2f}",
                        product.get('stock_quantity', 0)
                    ))
            else:
                messagebox.showinfo("提示", f"没有找到包含 '{keyword}' 的商品")
        except Exception as e:
            print(f"搜索商品出错: {str(e)}")
            messagebox.showerror("错误", f"搜索失败: {str(e)}")
        
        # 重置当前选择
        self.current_product_id = None
    
    def on_product_select(self, event):
        """处理商品选择事件"""
        try:
            selected_items = self.product_tree.selection()
            if selected_items:
                selected_item = selected_items[0]
                product_data = self.product_tree.item(selected_item, "values")
                if product_data and product_data[0]:
                    self.current_product_id = int(product_data[0])
                else:
                    self.current_product_id = None
            else:
                self.current_product_id = None
        except (IndexError, ValueError) as e:
            print(f"选择商品出错: {str(e)}")
            self.current_product_id = None
    
    def add_product(self):
        """添加新商品"""
        # 创建添加商品对话框
        add_window = tk.Toplevel(self.parent)
        add_window.title("添加新商品")
        add_window.geometry("500x400")
        add_window.resizable(False, False)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        
        # 创建表单框架
        form_frame = ttk.Frame(add_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 商品名称
        ttk.Label(form_frame, text="商品名称: *").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, width=40).grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品描述
        ttk.Label(form_frame, text="商品描述: ").grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
        description_var = tk.StringVar()
        description_entry = tk.Text(form_frame, height=5, width=30)
        description_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品价格
        ttk.Label(form_frame, text="商品价格: *").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        price_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=price_var, width=15).grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品库存
        ttk.Label(form_frame, text="商品库存: *").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        stock_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=stock_var, width=15).grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 保存商品
        def save_product():
            # 获取表单数据
            name = name_var.get().strip()
            description = description_entry.get("1.0", tk.END).strip()
            price_str = price_var.get().strip()
            stock_str = stock_var.get().strip()
            
            # 验证必填字段
            if not name:
                messagebox.showerror("错误", "请输入商品名称")
                return
            
            if not price_str:
                messagebox.showerror("错误", "请输入商品价格")
                return
            
            if not stock_str:
                messagebox.showerror("错误", "请输入商品库存")
                return
            
            # 验证价格和库存为数字
            try:
                price = float(price_str)
                if price < 0:
                    messagebox.showerror("错误", "商品价格不能为负数")
                    return
            except ValueError:
                messagebox.showerror("错误", "请输入有效的商品价格")
                return
            
            try:
                stock = int(stock_str)
                if stock < 0:
                    messagebox.showerror("错误", "商品库存不能为负数")
                    return
            except ValueError:
                messagebox.showerror("错误", "请输入有效的商品库存")
                return
            
            # 准备商品数据
            product_data = {
                'name': name,
                'description': description,
                'price': price,
                'stock': stock
            }
            
            # 创建商品
            try:
                # 修改调用方式，从传递字典改为传递单独的参数
                success = self.product_model.add_product(
                    name=product_data['name'],
                    price=product_data['price'],
                    stock_quantity=product_data['stock']
                )
                if success:
                    # 查询最后插入的商品ID
                    products = self.product_model.get_all_products()
                    new_product = max(products, key=lambda x: x['product_id']) if products else None
                    product_id = new_product['product_id'] if new_product else '未知'
                    messagebox.showinfo("成功", f"商品添加成功！商品ID: {product_id}")
                    self.refresh_data()
                    add_window.destroy()
                else:
                    messagebox.showerror("错误", "商品添加失败")
            except Exception as e:
                messagebox.showerror("错误", f"商品添加失败: {str(e)}")
        
        # 按钮区域
        button_frame = ttk.Frame(add_window)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="添加商品", command=save_product).pack(side=tk.RIGHT, padx=10)
        ttk.Button(button_frame, text="取消", command=add_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        add_window.grab_set()
        self.parent.wait_window(add_window)
    
    def view_product_details(self):
        """查看商品详情"""
        if not self.current_product_id:
            messagebox.showinfo("提示", "请先选择一个商品")
            return
        
        # 获取商品详情
        product = self.product_model.get_product_by_id(self.current_product_id)
        if not product:
            messagebox.showerror("错误", "无法获取商品详情")
            return
        
        # 创建商品详情对话框
        detail_window = tk.Toplevel(self.parent)
        detail_window.title(f"商品详情 - ID: {product['product_id']}")
        detail_window.geometry("600x500")
        detail_window.resizable(True, True)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        
        # 创建商品基本信息区域
        product_info_frame = ttk.LabelFrame(detail_window, text="商品信息")
        product_info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 商品信息网格
        info_grid = ttk.Frame(product_info_frame)
        info_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # 商品ID
        ttk.Label(info_grid, text="商品ID:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_grid, text=product['product_id']).grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品名称
        ttk.Label(info_grid, text="商品名称:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_grid, text=product['name']).grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品价格
        ttk.Label(info_grid, text="商品价格:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_grid, text=f"¥{product['price']:.2f}").grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品库存
        ttk.Label(info_grid, text="商品库存:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(info_grid, text=product['stock_quantity']).grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 创建商品描述区域
        description_frame = ttk.LabelFrame(detail_window, text="商品描述")
        description_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 商品描述文本框（只读）
        description_text = tk.Text(description_frame, wrap=tk.WORD, height=10, width=60)
        description_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        description_text.insert(tk.END, product.get('description', '无描述'))
        description_text.config(state=tk.DISABLED)
        
        # 关闭按钮
        ttk.Button(detail_window, text="关闭", command=detail_window.destroy).pack(pady=10)
        
        # 使对话框模态
        detail_window.grab_set()
        self.parent.wait_window(detail_window)
    
    def edit_product(self):
        """编辑商品信息"""
        if not self.current_product_id:
            messagebox.showinfo("提示", "请先选择一个商品")
            return
        
        # 获取当前商品信息
        product = self.product_model.get_product_by_id(self.current_product_id)
        if not product:
            messagebox.showerror("错误", "无法获取商品信息")
            return
        
        # 创建编辑商品对话框
        edit_window = tk.Toplevel(self.parent)
        edit_window.title(f"编辑商品 - ID: {product['product_id']}")
        edit_window.geometry("500x400")
        edit_window.resizable(False, False)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        
        # 创建表单框架
        form_frame = ttk.Frame(edit_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 商品ID（只读显示）
        ttk.Label(form_frame, text="商品ID:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        ttk.Label(form_frame, text=product['product_id']).grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品名称
        ttk.Label(form_frame, text="商品名称: *").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar(value=product['name'])
        ttk.Entry(form_frame, textvariable=name_var, width=40).grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品描述
        ttk.Label(form_frame, text="商品描述: ").grid(row=2, column=0, sticky=tk.NW, padx=10, pady=10)
        description_entry = tk.Text(form_frame, height=5, width=30)
        description_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        description_entry.insert(tk.END, product.get('description', ''))
        
        # 商品价格
        ttk.Label(form_frame, text="商品价格: *").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        price_var = tk.StringVar(value=str(product['price']))
        ttk.Entry(form_frame, textvariable=price_var, width=15).grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 商品库存
        ttk.Label(form_frame, text="商品库存: *").grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        stock_var = tk.StringVar(value=str(product['stock_quantity']))
        ttk.Entry(form_frame, textvariable=stock_var, width=15).grid(row=4, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 保存商品编辑
        def save_edit():
            # 获取表单数据
            name = name_var.get().strip()
            description = description_entry.get("1.0", tk.END).strip()
            price_str = price_var.get().strip()
            stock_str = stock_var.get().strip()
            
            # 验证必填字段
            if not name:
                messagebox.showerror("错误", "请输入商品名称")
                return
            
            if not price_str:
                messagebox.showerror("错误", "请输入商品价格")
                return
            
            if not stock_str:
                messagebox.showerror("错误", "请输入商品库存")
                return
            
            # 验证价格和库存为数字
            try:
                price = float(price_str)
                if price < 0:
                    messagebox.showerror("错误", "商品价格不能为负数")
                    return
            except ValueError:
                messagebox.showerror("错误", "请输入有效的商品价格")
                return
            
            try:
                stock = int(stock_str)
                if stock < 0:
                    messagebox.showerror("错误", "商品库存不能为负数")
                    return
            except ValueError:
                messagebox.showerror("错误", "请输入有效的商品库存")
                return
            
            # 准备商品数据
            
            # 更新商品
            try:
                if self.product_model.update_product(
                    product_id=product['product_id'],
                    product_name=name,
                    price=price,
                    stock_quantity=stock
                ):
                    messagebox.showinfo("成功", "商品信息已更新")
                    self.refresh_data()
                    edit_window.destroy()
                else:
                    messagebox.showerror("错误", "商品信息更新失败")
            except Exception as e:
                messagebox.showerror("错误", f"商品信息更新失败: {str(e)}")
        
        # 按钮区域
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="保存", command=save_edit).pack(side=tk.RIGHT, padx=10)
        ttk.Button(button_frame, text="取消", command=edit_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        edit_window.grab_set()
        self.parent.wait_window(edit_window)
    
    def delete_product(self):
        """删除商品"""
        if not self.current_product_id:
            messagebox.showinfo("提示", "请先选择一个商品")
            return
        
        if messagebox.askyesno("确认删除", "确定要删除选中的商品吗？"):
            try:
                if self.product_model.delete_product(self.current_product_id):
                    messagebox.showinfo("成功", "商品已成功删除")
                    self.refresh_data()
                else:
                    messagebox.showerror("错误", "删除商品失败")
            except Exception as e:
                messagebox.showerror("错误", f"删除商品失败: {str(e)}")
    
    def adjust_stock(self):
        """调整商品库存"""
        if not self.current_product_id:
            messagebox.showinfo("提示", "请先选择一个商品")
            return
        
        # 获取当前商品信息
        product = self.product_model.get_product_by_id(self.current_product_id)
        if not product:
            messagebox.showerror("错误", "无法获取商品信息")
            return
        
        # 创建调整库存对话框
        adjust_window = tk.Toplevel(self.parent)
        adjust_window.title(f"调整库存 - {product['name']}")
        adjust_window.geometry("400x300")
        adjust_window.resizable(False, False)
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        
        # 创建内容框架
        content_frame = ttk.Frame(adjust_window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 当前库存显示
        ttk.Label(content_frame, text="当前库存: ", font=("SimHei", 12)).grid(row=0, column=0, sticky=tk.W, padx=10, pady=20)
        current_stock_var = tk.StringVar(value=str(product['stock']))
        ttk.Label(content_frame, textvariable=current_stock_var, font=("SimHei", 12, "bold"), foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=10, pady=20)
        
        # 调整数量输入
        ttk.Label(content_frame, text="调整数量: ").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        adjust_var = tk.StringVar(value="")
        ttk.Entry(content_frame, textvariable=adjust_var, width=15).grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        ttk.Label(content_frame, text="(正数增加，负数减少)").grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        # 调整后库存预览
        ttk.Label(content_frame, text="调整后库存: ").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        new_stock_var = tk.StringVar(value=str(product['stock']))
        ttk.Label(content_frame, textvariable=new_stock_var, font=("SimHei", 10), foreground="green").grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 实时计算调整后库存
        def update_preview(event=None):
            try:
                adjust_value = int(adjust_var.get().strip())
                new_stock = product['stock'] + adjust_value
                new_stock_var.set(str(new_stock))
                # 库存为负时显示红色警告
                if new_stock < 0:
                    new_stock_var.set(f"{new_stock} (警告: 库存不足)")
                    new_stock_label.config(foreground="red")
                else:
                    new_stock_label.config(foreground="green")
            except ValueError:
                new_stock_var.set(str(product['stock']))
                new_stock_label.config(foreground="green")
        
        # 绑定输入事件
        adjust_var.trace_add("write", lambda *args: update_preview())
        
        # 重新获取标签引用以修改样式
        new_stock_label = ttk.Label(content_frame, textvariable=new_stock_var, font=("SimHei", 10), foreground="green")
        new_stock_label.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        
        # 确认调整
        def confirm_adjustment():
            try:
                adjust_value = int(adjust_var.get().strip())
                if adjust_value == 0:
                    messagebox.showinfo("提示", "调整数量为0，无需操作")
                    return
                
                new_stock = product['stock'] + adjust_value
                if new_stock < 0:
                    if not messagebox.askyesno("确认", f"调整后库存将为负数({new_stock})，确定继续吗？"):
                        return
                
                # 更新库存
                if self.product_model.adjust_product_stock(product['id'], adjust_value):
                    # 添加库存调整日志
                    action = "增加" if adjust_value > 0 else "减少"
                    self.product_model.add_inventory_log(product['id'], adjust_value, f"手动{action}库存")
                    
                    messagebox.showinfo("成功", f"库存已{action}{abs(adjust_value)}个，当前库存: {new_stock}")
                    self.refresh_data()
                    adjust_window.destroy()
                else:
                    messagebox.showerror("错误", "库存调整失败")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的调整数量")
        
        # 按钮区域
        button_frame = ttk.Frame(adjust_window)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="确认调整", command=confirm_adjustment).pack(side=tk.RIGHT, padx=10)
        ttk.Button(button_frame, text="取消", command=adjust_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        adjust_window.grab_set()
        self.parent.wait_window(adjust_window)
    
    def view_inventory_logs(self):
        """查看商品库存日志"""
        if not self.current_product_id:
            messagebox.showinfo("提示", "请先选择一个商品")
            return
        
        # 获取当前商品信息
        product = self.product_model.get_product_by_id(self.current_product_id)
        if not product:
            messagebox.showerror("错误", "无法获取商品信息")
            return
        
        # 创建库存日志查看对话框
        log_window = tk.Toplevel(self.parent)
        log_window.title(f"库存日志 - {product['name']}")
        log_window.geometry("700x500")
        
        # 设置中文字体
        style = ttk.Style()
        style.configure("TLabel", font=("SimHei", 10))
        style.configure("TButton", font=("SimHei", 10))
        style.configure("Treeview", font=("SimHei", 10))
        style.configure("Treeview.Heading", font=("SimHei", 10, "bold"))
        
        # 创建框架
        top_frame = ttk.Frame(log_window)
        top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 显示商品基本信息
        product_info = f"商品: {product['name']} (ID: {product['id']})  当前库存: {product['stock']}"
        ttk.Label(top_frame, text=product_info, font=("SimHei", 11)).pack(anchor=tk.W)
        
        # 创建滚动条和表格
        table_frame = ttk.Frame(log_window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建垂直滚动条
        y_scrollbar = ttk.Scrollbar(table_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建水平滚动条
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建表格
        log_tree = ttk.Treeview(table_frame, columns=("id", "timestamp", "change", "new_stock", "reason"), 
                              show="headings", yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # 配置列
        log_tree.column("id", width=50, anchor=tk.CENTER)
        log_tree.column("timestamp", width=180, anchor=tk.CENTER)
        log_tree.column("change", width=100, anchor=tk.CENTER)
        log_tree.column("new_stock", width=100, anchor=tk.CENTER)
        log_tree.column("reason", width=250, anchor=tk.W)
        
        # 设置列标题
        log_tree.heading("id", text="ID")
        log_tree.heading("timestamp", text="时间戳")
        log_tree.heading("change", text="数量变化")
        log_tree.heading("new_stock", text="调整后库存")
        log_tree.heading("reason", text="调整原因")
        
        # 绑定滚动条
        y_scrollbar.config(command=log_tree.yview)
        x_scrollbar.config(command=log_tree.xview)
        
        # 放置表格
        log_tree.pack(fill=tk.BOTH, expand=True)
        
        # 加载库存日志
        def load_logs():
            # 清空现有数据
            for item in log_tree.get_children():
                log_tree.delete(item)
            
            # 获取库存日志
            logs = self.product_model.get_inventory_logs(product['id'])
            
            if not logs:
                # 添加空行提示
                log_tree.insert("", tk.END, values=("", "", "", "", "暂无库存记录"), tags=("empty",))
                log_tree.tag_configure("empty", foreground="gray")
                return
            
            # 添加数据到表格
            for log in logs:
                # 格式化时间戳
                timestamp = log['timestamp']
                # 为数量变化添加颜色
                change_value = log['change']
                if change_value > 0:
                    change_text = f"+{change_value}"
                    tags = ("increase",)
                elif change_value < 0:
                    change_text = f"{change_value}"
                    tags = ("decrease",)
                else:
                    change_text = f"{change_value}"
                    tags = ()
                
                log_tree.insert("", tk.END, values=(log['id'], timestamp, change_text, log['new_stock'], log['reason']), tags=tags)
                
            # 设置标签样式
            log_tree.tag_configure("increase", foreground="green")
            log_tree.tag_configure("decrease", foreground="red")
        
        # 加载日志数据
        load_logs()
        
        # 底部按钮区域
        button_frame = ttk.Frame(log_window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 刷新按钮
        ttk.Button(button_frame, text="刷新", command=load_logs).pack(side=tk.RIGHT, padx=10)
        # 关闭按钮
        ttk.Button(button_frame, text="关闭", command=log_window.destroy).pack(side=tk.RIGHT, padx=10)
        
        # 使对话框模态
        log_window.grab_set()
        self.parent.wait_window(log_window)
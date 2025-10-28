# 电子商务管理系统

## 项目介绍

这是一个基于Python和MySQL开发的电子商务管理系统，提供客户管理、商品管理、订单管理等核心功能，适用于中小型电商企业的日常运营管理。

## 系统架构

- **前端**：使用Python Tkinter库开发图形用户界面
- **后端**：Python实现业务逻辑
- **数据库**：MySQL存储系统数据

## 目录结构

```
ecommerce_project/
 ├── database/                     # 数据库相关文件
 │   ├── schema/                   # 数据库结构文件
 │   │   ├── 01_tables_ddl.sql     # 表创建DDL语句
 │   │   ├── 02_indexes_fk.sql     # 索引和外键设置
 │   │   └── 03_sample_data.sql    # 示例数据插入
 │   └── migrations/               # 数据库迁移脚本（可选）
 ├── src/                          # 源代码目录
 │   ├── models/                   # 数据模型
 │   │   ├── database.py           # 数据库连接和基础操作类
 │   │   ├── customer.py           # 客户模型类
 │   │   ├── product.py            # 商品模型类
 │   │   └── order.py              # 订单模型类
 │   ├── utils/                    # 工具函数
 │   │   ├── data_generator.py     # 测试数据生成器
 │   │   └── helpers.py            # 辅助函数
 │   ├── gui/                      # 图形界面
 │   │   ├── main_window.py        # 主窗口类
 │   │   ├── customer_tab.py       # 客户管理标签页
 │   │   ├── product_tab.py        # 商品管理标签页
 │   │   └── order_tab.py          # 订单管理标签页
 │   └── main.py                   # 程序入口点
 ├── config/                       # 配置文件
 │   ├── database.ini              # 数据库连接配置
 │   └── settings.json             # 应用设置
 ├── tests/                        # 测试文件
 │   ├── test_database.py          # 数据库操作测试
 │   └── test_models.py            # 模型测试
 ├── docs/                         # 项目文档
 │   ├── ER_diagram.svg            # 实体关系图
 │   ├── requirements.md           # 需求分析
 │   └── manual.md                 # 用户手册
 └── README.md                     # 项目说明文件
```

## 环境要求

- **操作系统**：Windows 7/8/10/11
- **Python版本**：Python 3.8或更高版本
- **数据库**：MySQL 5.7或更高版本
- **依赖库**：pymysql

## 安装指南

### 1. 安装Python

访问[Python官方网站](https://www.python.org/)下载并安装最新版本的Python。

### 2. 安装MySQL

访问[MySQL官方网站](https://dev.mysql.com/downloads/)下载并安装MySQL数据库。

### 3. 创建数据库

使用MySQL客户端工具创建一个名为`ecommerce_db`的数据库。

### 4. 初始化数据库

执行`database/schema/`目录下的SQL脚本初始化数据库：

```sql
-- 1. 创建表结构
SOURCE database/schema/01_tables_ddl.sql;

-- 2. 创建索引和外键
SOURCE database/schema/02_indexes_fk.sql;

-- 3. 插入示例数据（可选）
SOURCE database/schema/03_sample_data.sql;
```

### 5. 安装依赖包

```bash
pip install pymysql
```

### 6. 配置数据库连接

编辑`config/database.ini`文件，设置您的MySQL连接参数：

```ini
[database]
host = localhost
port = 3306
user = root
password = 您的MySQL密码
dbname = ecommerce_db
charset = utf8mb4
```

## 运行系统

在项目根目录下执行以下命令启动系统：

```bash
python src/main.py
```

## 系统功能

### 客户管理
- 添加、查看、编辑和删除客户信息
- 搜索和筛选客户
- 客户统计分析

### 商品管理
- 添加、查看、编辑和删除商品信息
- 管理商品库存
- 搜索和筛选商品
- 商品统计分析

### 订单管理
- 查看和搜索订单
- 更新订单状态
- 取消订单
- 订单统计分析

## 测试

运行项目中的测试用例，确保系统功能正常：

```bash
python -m unittest discover tests
```

## 文档

- **需求分析**：`docs/requirements.md`
- **用户手册**：`docs/manual.md`
- **实体关系图**：`docs/ER_diagram.svg`

## 开发说明

### 代码规范
- 遵循PEP 8 Python代码风格指南
- 所有函数和类都应有清晰的文档字符串
- 使用有意义的变量和函数名

### 开发环境设置

1. 克隆项目仓库
2. 创建Python虚拟环境
3. 安装依赖包
4. 配置数据库连接
5. 运行测试确保环境正常

## 维护说明

- 定期备份数据库
- 定期清理日志文件
- 系统出现问题时，查看日志文件获取详细错误信息

## 版权信息

© 2023 电子商务管理系统. 保留所有权利.
-- 添加外键约束
-- 订单表的客户外键
alter table orders
add constraint fk_orders_customers
foreign key (customer_id) references customers(customer_id) on delete cascade;

-- 订单详情表的订单外键
alter table order_items
add constraint fk_order_items_orders
foreign key (order_id) references orders(order_id) on delete cascade;

-- 订单详情表的商品外键
alter table order_items
add constraint fk_order_items_products
foreign key (product_id) references products(product_id) on delete restrict;

-- 购物车表的客户外键
alter table cart
add constraint fk_cart_customers
foreign key (customer_id) references customers(customer_id) on delete cascade;

-- 购物车表的商品外键
alter table cart
add constraint fk_cart_products
foreign key (product_id) references products(product_id) on delete restrict;

-- 库存日志表的商品外键
alter table inventory_logs
add constraint fk_inventory_logs_products
foreign key (product_id) references products(product_id) on delete restrict;

-- 添加索引
-- 客户表的邮箱索引（用于登录和查询）
create index idx_customers_email on customers(email);

-- 客户表的姓名索引（用于搜索）
create index idx_customers_last_name on customers(last_name);

-- 商品表的分类索引（用于筛选）
create index idx_products_category on products(category);

-- 商品表的品牌索引（用于筛选）
create index idx_products_brand on products(brand);

-- 商品表的名称索引（用于搜索）
create index idx_products_name on products(product_name);

-- 订单表的客户和日期索引（用于历史订单查询）
create index idx_orders_customer_date on orders(customer_id, order_date);

-- 订单表的状态索引（用于订单管理）
create index idx_orders_status on orders(status);

-- 订单详情表的订单索引（用于订单详情查询）
create index idx_order_items_order on order_items(order_id);

-- 购物车表的客户索引（用于购物车查询）
create index idx_cart_customer on cart(customer_id);
-- 插入客户示例数据
insert into customers (first_name, last_name, email, phone, address, city, state, zip_code, country)
values
    ('张三', '张', 'zhangsan@example.com', '13800138001', '北京市朝阳区建国路88号', '北京', '北京市', '100022', '中国'),
    ('李四', '李', 'lisi@example.com', '13900139002', '上海市浦东新区陆家嘴环路1000号', '上海', '上海市', '200120', '中国'),
    ('王五', '王', 'wangwu@example.com', '13700137003', '广州市天河区天河路385号', '广州', '广东省', '510620', '中国'),
    ('赵六', '赵', 'zhaoliu@example.com', '13600136004', '深圳市南山区科技园南区', '深圳', '广东省', '518057', '中国'),
    ('钱七', '钱', 'qianqi@example.com', '13500135005', '杭州市西湖区文三路478号', '杭州', '浙江省', '310012', '中国'),
    ('孙八', '孙', 'sunba@example.com', '13400134006', '南京市玄武区珠江路435号', '南京', '江苏省', '210018', '中国'),
    ('周九', '周', 'zhoujiu@example.com', '13300133007', '武汉市江汉区解放大道686号', '武汉', '湖北省', '430022', '中国'),
    ('吴十', '吴', 'wushi@example.com', '13200132008', '成都市锦江区春熙路39号', '成都', '四川省', '610016', '中国');

-- 插入商品示例数据
insert into products (product_name, description, price, stock_quantity, category, brand, image_url)
values
    ('iPhone 14 Pro', '最新款智能手机，6.1英寸OLED显示屏，A16仿生芯片', 8999.00, 100, '手机', 'Apple', 'https://example.com/images/iphone14pro.jpg'),
    ('Samsung Galaxy S23', '高端Android手机，6.1英寸AMOLED显示屏，骁龙8 Gen 2处理器', 7999.00, 80, '手机', 'Samsung', 'https://example.com/images/s23.jpg'),
    ('MacBook Pro 14', '专业级笔记本电脑，M2 Pro芯片，16GB内存，512GB存储', 15999.00, 50, '笔记本电脑', 'Apple', 'https://example.com/images/macbookpro14.jpg'),
    ('Dell XPS 13', '轻薄笔记本电脑，第12代英特尔酷睿处理器，16GB内存，512GB SSD', 8999.00, 30, '笔记本电脑', 'Dell', 'https://example.com/images/xps13.jpg'),
    ('Sony WH-1000XM5', '高端降噪耳机，40小时续航，触控操作', 2999.00, 120, '耳机', 'Sony', 'https://example.com/images/wh1000xm5.jpg'),
    ('Bose QuietComfort 45', '舒适降噪耳机，30小时续航，有线/无线双模式', 2699.00, 90, '耳机', 'Bose', 'https://example.com/images/quietcomfort45.jpg'),
    ('iPad Air 5', '轻薄平板电脑，M1芯片，10.9英寸显示屏', 5999.00, 60, '平板电脑', 'Apple', 'https://example.com/images/ipadair5.jpg'),
    ('Surface Pro 9', '二合一平板电脑，第12代英特尔酷睿处理器，13英寸显示屏', 7999.00, 40, '平板电脑', 'Microsoft', 'https://example.com/images/surfacepro9.jpg'),
    ('Apple Watch Series 8', '智能手表，健康监测，GPS，防水', 3199.00, 70, '智能穿戴', 'Apple', 'https://example.com/images/watchs8.jpg'),
    ('Fitbit Charge 5', '健康追踪器，心率监测，睡眠分析，GPS', 1199.00, 150, '智能穿戴', 'Fitbit', 'https://example.com/images/charge5.jpg');

-- 插入订单示例数据
insert into orders (customer_id, order_date, total_amount, status, shipping_address, payment_method, payment_status)
values
    (1, '2023-09-10 10:30:00', 8999.00, 'completed', '北京市朝阳区建国路88号', '支付宝', 'paid'),
    (2, '2023-09-11 14:20:00', 7999.00, 'completed', '上海市浦东新区陆家嘴环路1000号', '微信支付', 'paid'),
    (3, '2023-09-12 09:15:00', 15999.00, 'pending', '广州市天河区天河路385号', '银行卡', 'unpaid'),
    (4, '2023-09-13 16:45:00', 2999.00, 'completed', '深圳市南山区科技园南区', '支付宝', 'paid'),
    (5, '2023-09-14 11:50:00', 5999.00, 'shipping', '杭州市西湖区文三路478号', '微信支付', 'paid'),
    (6, '2023-09-15 13:25:00', 8999.00, 'cancelled', '南京市玄武区珠江路435号', '银行卡', 'refunded'),
    (7, '2023-09-16 15:40:00', 2699.00, 'completed', '武汉市江汉区解放大道686号', '支付宝', 'paid'),
    (8, '2023-09-17 10:10:00', 3199.00, 'pending', '成都市锦江区春熙路39号', '微信支付', 'unpaid');

-- 插入订单详情示例数据
insert into order_items (order_id, product_id, quantity, unit_price, subtotal)
values
    (1, 1, 1, 8999.00, 8999.00),
    (2, 2, 1, 7999.00, 7999.00),
    (3, 3, 1, 15999.00, 15999.00),
    (4, 5, 1, 2999.00, 2999.00),
    (5, 7, 1, 5999.00, 5999.00),
    (6, 4, 1, 8999.00, 8999.00),
    (7, 6, 1, 2699.00, 2699.00),
    (8, 9, 1, 3199.00, 3199.00);

-- 插入购物车示例数据
insert into cart (customer_id, product_id, quantity, added_at)
values
    (1, 5, 1, '2023-09-18 09:30:00'),
    (2, 8, 1, '2023-09-18 10:15:00'),
    (3, 10, 1, '2023-09-18 11:20:00'),
    (4, 6, 1, '2023-09-18 13:45:00'),
    (5, 2, 1, '2023-09-18 14:30:00');

-- 插入库存日志示例数据
insert into inventory_logs (product_id, previous_quantity, current_quantity, change_amount, change_type, changed_by)
values
    (1, 101, 100, -1, '销售出库', '系统'),
    (2, 81, 80, -1, '销售出库', '系统'),
    (3, 51, 50, -1, '销售出库', '系统'),
    (5, 121, 120, -1, '销售出库', '系统'),
    (7, 61, 60, -1, '销售出库', '系统'),
    (6, 91, 90, -1, '销售出库', '系统'),
    (9, 71, 70, -1, '销售出库', '系统'),
    (1, 100, 110, 10, '采购入库', '管理员');
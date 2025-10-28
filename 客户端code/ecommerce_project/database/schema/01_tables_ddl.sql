-- 创建客户表
drop table if exists customers;
create table customers (
    customer_id int primary key auto_increment,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(100) unique not null,
    phone varchar(20),
    gender enum('male', 'female', 'other'),
    address varchar(255),
    city varchar(50),
    state varchar(50),
    zip_code varchar(20),
    country varchar(50),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);

-- 创建商品表
drop table if exists products;
create table products (
    product_id int primary key auto_increment,
    product_name varchar(100) not null,
    description text,
    price decimal(10, 2) not null check (price >= 0),
    stock_quantity int not null check (stock_quantity >= 0),
    category varchar(50),
    brand varchar(50),
    image_url varchar(255),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);

-- 创建订单表
drop table if exists orders;
create table orders (
    order_id int primary key auto_increment,
    customer_id int not null,
    order_date timestamp default current_timestamp,
    total_amount decimal(10, 2) not null check (total_amount >= 0),
    status varchar(20) not null default 'pending',
    shipping_address varchar(255),
    payment_method varchar(50),
    payment_status varchar(20) default 'unpaid',
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp
);

-- 创建订单详情表
drop table if exists order_items;
create table order_items (
    order_item_id int primary key auto_increment,
    order_id int not null,
    product_id int not null,
    quantity int not null check (quantity > 0),
    unit_price decimal(10, 2) not null check (unit_price >= 0),
    subtotal decimal(10, 2) not null check (subtotal >= 0)
);

-- 创建购物车表
drop table if exists cart;
create table cart (
    cart_id int primary key auto_increment,
    customer_id int not null,
    product_id int not null,
    quantity int not null check (quantity > 0),
    added_at timestamp default current_timestamp
);

-- 创建库存日志表
drop table if exists inventory_logs;
create table inventory_logs (
    log_id int primary key auto_increment,
    product_id int not null,
    previous_quantity int not null,
    current_quantity int not null,
    change_amount int not null,
    change_type varchar(50) not null,
    changed_by varchar(50),
    changed_at timestamp default current_timestamp
);
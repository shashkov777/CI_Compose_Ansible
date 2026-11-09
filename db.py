import sqlite3 

def create_tables():

    conn = sqlite3.connect("userfile.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT UNIQUE NOT NULL,
        user_name TEXT NOT NULL,
        user_tg_id INTEGER UNIQUE
    );

    CREATE TABLE IF NOT EXISTS place (
        place_id INTEGER PRIMARY KEY,
        place_name TEXT NOT NULL,
        address TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        photo_path TEXT NOT NULL,
        desc TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS product_variants (
        id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        variant_name TEXT NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );

    CREATE TABLE IF NOT EXISTS modifiers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        pickup_point_id INTEGER NOT NULL,
        pickup_type TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES users(user_tg_id),
        FOREIGN KEY (pickup_point_id) REFERENCES place(place_id)
    );

    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER NOT NULL,
        product_variant_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        item_price INTEGER NOT NULL,
        ratio_name TEXT NOT NULL,
        FOREIGN KEY (cart_id) REFERENCES carts(id),
        FOREIGN KEY (product_variant_id) REFERENCES product_variants(id)
    );

    CREATE TABLE IF NOT EXISTS cart_item_modifiers (
        cart_item_id INTEGER NOT NULL,
        modifier_id INTEGER NOT NULL,
        PRIMARY KEY (cart_item_id, modifier_id),
        FOREIGN KEY (cart_item_id) REFERENCES cart_items(id),
        FOREIGN KEY (modifier_id) REFERENCES modifiers(id)
    );

    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        pickup_point_id INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        status TEXT NOT NULL,
        pickup_type TEXT NOT NULL,
        take_time TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (customer_id) REFERENCES users(user_tg_id),
        FOREIGN KEY (pickup_point_id) REFERENCES place(place_id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        variant_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        item_price INTEGER NOT NULL,
        ratio_name TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    );

    CREATE TABLE IF NOT EXISTS order_item_modifiers (
        order_item_id INTEGER NOT NULL,
        modifier_name TEXT NOT NULL,
        price INTEGER NOT NULL,
        PRIMARY KEY (order_item_id, modifier_name),
        FOREIGN KEY (order_item_id) REFERENCES order_items(id)
    );
                      
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    );
                      
    CREATE TABLE IF NOT EXISTS current_product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_tg_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        FOREIGN KEY (user_tg_id) REFERENCES users(user_tg_id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );

    CREATE TABLE IF NOT EXISTS current_modifiers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_tg_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        modifier_id INTEGER NOT NULL,
        FOREIGN KEY (user_tg_id) REFERENCES users(user_tg_id),
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (modifier_id) REFERENCES modifiers(id)
    );

    CREATE TABLE IF NOT EXISTS current_quantity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_tg_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (user_tg_id) REFERENCES users(user_tg_id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );

    """)

    conn.commit()
    conn.close()

def products_in():
    conn = sqlite3.connect("userfile.db")
    cur = conn.cursor()

    cur.executescript("""
        INSERT OR IGNORE INTO products (id, product_name, category, photo_path, desc) 
        VALUES 
        (1, 'Американо', 'drinks', './photo2.jpg', 'Классический чёрный кофе'), (2, 'Эспрессо', 'drinks', './photo.jpg', 'Насыщенный вкус'), 
        (3, 'Фильтр-кофе', 'drinks', './photo.jpg', 'Классический фильтр'), (4, 'Капучино', 'drinks', './photo.jpg', 'С молочной пеной'), 
        (5, 'Латте', 'drinks', './photo.jpg', 'Нежный и сливочный'), (6, 'Флэт Уайт', 'drinks', './photo.jpg', 'Микровспенка молока'), 
        (7, 'Раф', 'drinks', './photo.jpg', 'Эспрессо с сливками'), (8, 'Матча', 'drinks', './photo.jpg', 'Зелёный чай'), 
        (9, 'Какао', 'drinks', './photo.jpg', 'Горячее какао'),(10, 'Бабка с шоколадом и вишней', 'food', './photo2.jpg', 'Сладкая выпечка с шоколадом и вишней'), 
        (11, 'Сэндвич с мясом', 'food', './photo2.jpg', 'Сытный мясной сэндвич'), (12, 'Краффин с соленой карамелью', 'food', './photo2.jpg', 'Хрустящий краффин с карамелью'), 
        (13, 'Канеле', 'food', './photo2.jpg', 'Французская выпечка с ромом'), (14, 'Ржаной даниш с брынзой', 'food', './photo2.jpg', 'Даниш с ржаной мукой и сыром'), 
        (15, 'Круассан с сыром', 'food', './photo2.jpg', 'Классический круассан с плавленым сыром'), (16, 'Пан шоколя', 'food', './photo2.jpg', 'Мягкая булочка с шоколадом'), 
        (17, 'Проще не бывает! термокружка', 'merch', './photo2.jpg', 'Термокружка 350мл'), (18, 'Матча-зона футболка', 'merch', './photo2.jpg', 'Футболка М-XL'), 
        (19, 'Coffee Starter Kit', 'merch', './photo2.jpg', 'Стартовый набор любителей кофе'), (20, 'Персональная подставка', 'merch', './photo2.jpg', 'Подставка имя'); 

        INSERT OR IGNORE INTO place (place_id, place_name, address)
        VALUES (101, 'ЛЕНПОЛИГРАФМАШ', 'Санкт-Петербург, Аптекарский просп., 2'), (102, 'У КАРАНДАША', 'Санкт-Петербург, Большой Сампсониевский просп., 76');

        INSERT OR IGNORE INTO modifiers (id, name, price)
        VALUES (1001, 'Сироп карамель', 20), (1002, 'Сироп ваниль', 30), (1003, 'Сироп орех', 50), (1004, 'Овсяное молоко', 50), (1005, 'Миндальное молоко', 20), (1006, 'Кокосовое молоко', 31), (1007, 'Без добавок', 0);
                      
        INSERT OR IGNORE INTO product_variants (id, product_id, variant_name, price)
        VALUES 
            -- drinks
            (1, 1, 'Small', 180), (2, 1, 'Big', 220), -- американо
            (3, 2, 'onesize', 150), -- эспрессо
            (4, 3, 'Small', 180), (5, 3, 'Big', 220), -- фильтр кофе
            (6, 4, 'Small', 220), (7, 4, 'Big', 280), -- капучино
            (8, 5, 'Small', 210), (9, 5, 'Big', 260), -- латте
            (10, 6, 'onesize', 240), -- флэт вайт 
            (11, 7, 'Small', 250), (12, 7, 'Big', 310), -- Раф
            (13, 8, 'Small', 240), (14, 8, 'Big', 280), -- Матча
            (15, 9, 'onesize', 300),  -- Какао
                      
            -- food
            (16, 10, 'onesize', 270), -- Бабка           
            (17, 11, 'onesize', 350), -- Сэндвич с мясом
            (18, 12, 'onesize', 270), -- Крафин 
            (19, 13, 'onesize', 150), -- Канеле       
            (20, 14, 'onesize', 250), -- Даниш
            (21, 15, 'onesize', 250), -- круасан с сыром
            (22, 16, 'onesize', 250), -- Пан шоколя
            
            --merch
            (23, 17, 'onesize', 500), -- термокружка      
            (24, 18, 'onesize', 700), -- футболка
            (25, 19, 'onesize', 300), -- набор
            (26, 20, 'onesize', 250); -- подставка            
                      
""")


    conn.commit()
    conn.close()


def data_in(table_name, **data):
    conn = sqlite3.connect("userfile.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    
    columns = list(data.keys())
    values = list(data.values())
    placeholders = ','.join('?' * len(values))
    query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
    
    cur.execute(query, values)

    conn.commit()
    last_id = cur.lastrowid
    conn.close()

    return last_id


def get_callback(table_name, back, id_name, extra_back=None, extra_id_name=None, **data):
    conn = sqlite3.connect("userfile.db")
    conn.row_factory = sqlite3.Row 

    cur = conn.cursor()

    if data: 
        columns = list(data.keys())
        query = f"SELECT {','.join(columns)} FROM {table_name} WHERE {id_name} = ?"
        cur.execute(query, (back,))
    else: 
        if extra_back is not None and extra_id_name is not None:
            query = f"SELECT * FROM {table_name} WHERE {id_name} = ? AND {extra_id_name} = ?"
            cur.execute(query, (back, extra_back,))
        else: 
            query = f"SELECT * FROM {table_name} WHERE {id_name} = ?"
            cur.execute(query, (back,))

    
    row = cur.fetchone()
    conn.close()
    
    return dict(row) if row else None


def get_callback_last1(table_name, back, id_name, extra_back=None, extra_id_name=None, **data):
    conn = sqlite3.connect("userfile.db")
    conn.row_factory = sqlite3.Row 

    cur = conn.cursor()

    if data: 
        columns = list(data.keys())
        query = f"SELECT {','.join(columns)} FROM {table_name} WHERE {id_name} = ? ORDER BY id DESC LIMIT 1"
        cur.execute(query, (back,))
    else: 
        if extra_back is not None and extra_id_name is not None:
            query = f"SELECT * FROM {table_name} WHERE {id_name} = ? AND {extra_id_name} = ? ORDER BY id DESC LIMIT 1"
            cur.execute(query, (back, extra_back,))
        else: 
            query = f"SELECT * FROM {table_name} WHERE {id_name} = ? ORDER BY id DESC LIMIT 1"
            cur.execute(query, (back,))

    
    row = cur.fetchone()
    conn.close()
    
    return dict(row) if row else None


def get_callback_last2(table_name, back, id_name, **data):
    conn = sqlite3.connect("userfile.db")
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor()

    if data: 
        columns = list(data.keys())
        query = f"SELECT {','.join(columns)} FROM {table_name} WHERE {id_name} = ? ORDER BY id DESC"
    else: 
        query = f"SELECT * FROM {table_name} WHERE {id_name} = ? ORDER BY id DESC"
    
    cur.execute(query, (back,))
    rows = cur.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
